import os
import json
from celery import shared_task
from redis import Redis

from .models import Message

@shared_task
def say_hello(name="World"):
    print(f"Hello, {name} from Celery!")


@shared_task
def poll_echo_responses():
        
    redis_host = "localhost"
    redis_db = 0
    redis_stream = "echo_responses"

    if not redis_host or redis_db is None or not redis_stream:
        return
    
    redis_client = None
    # Each tenant gets its own isolated consumer group for message processing
    consumer_group_name = "echo_consumer_1"
    consumer_name = f"consumer_1_{os.getpid()}"
    
    try:
        # Create Redis connection with proper timeouts
        redis_client = Redis(
            host=redis_host,
            port=6399,
            db=redis_db,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=10,
            socket_keepalive=True,
            retry_on_timeout=True,
        )
        
        # Create consumer group if it doesn't exist
        try:
            redis_client.xgroup_create(redis_stream, consumer_group_name, id='0', mkstream=True)
        except Exception as group_error:
            if "BUSYGROUP" not in str(group_error):
                print(f"Failed to create consumer group for Echo Response: {str(group_error)}")
                return

        try:
            pending_data = redis_client.xreadgroup(
                groupname=consumer_group_name,
                consumername=consumer_name,
                streams={redis_stream: '0'},  # pending messages
                count=100
            )
            
            new_data = redis_client.xreadgroup(
                groupname=consumer_group_name,
                consumername=consumer_name,
                streams={redis_stream: '>'},  # new messages
                count=100
            )
            
            # Combine pending and new messages
            data = []
            if pending_data:
                data.extend(pending_data)
            if new_data:
                data.extend(new_data)
                
            if not data:
                return
                
        except Exception as redis_error:
            print(f"Failed to read from Echo Response Redis stream: {str(redis_error)}")
            return
        
        # Process all available messages
        successfully_processed_ids = []
        
        for stream, messages in data:
            for message in messages:
                message_id = message[0]
                message_data = message[1]
                
                try:
                    # Process the message data
                    print(f"Echo: Processing message with ID: {message_id}")
                    print(f"Echo: Message data: {message_data}")
                    
                    # Save to database
                    try:
                        raw_json = message_data.get("json", "{}")
                        parsed_json = json.loads(raw_json)

                        Message.objects.create(
                            message=parsed_json.get("message", ""),
                            json_body=parsed_json
                        )

                    except Exception as process_error:
                        print(f"Failed to process message {message_id}: {str(process_error)}")
                    
                    # Mark message as successfully processed
                    successfully_processed_ids.append(message_id)
                    
                except Exception as process_error:
                    print(f"Failed to process message {message_id}: {str(process_error)}", exc_info=True)
                    # Continue processing other messages even if one fails
                    continue
        
        # Acknowledge successfully processed messages
        if successfully_processed_ids:
            try:
                # Acknowledge messages to remove them from pending list
                redis_client.xack(redis_stream, consumer_group_name, *successfully_processed_ids)
            except Exception as ack_error:
                print(f"Failed to acknowledge messages for Echo Response: {str(ack_error)}")
        
    except Exception as e:
        print(f"Failed to poll for Echo Responses. {str(e)}", exc_info=True)
    
    finally:
        # Close the Redis connection
        if redis_client:
            try:
                redis_client.close()
            except Exception:
                pass  # Ignore errors during cleanup