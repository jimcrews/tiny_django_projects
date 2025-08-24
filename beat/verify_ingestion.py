import os
import json
import time
from redis import Redis
import django
import uuid

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from echo.models import Message

# Redis config (check poll_echo_responses task)
REDIS_HOST = "localhost"
REDIS_PORT = 6399
REDIS_STREAM = "echo_responses"
REDIS_DB = 0

RUN_ID_1 = str(uuid.uuid4())
RUN_ID_2 = str(uuid.uuid4())

# Test data
test_messages_1 = [
    {"message": "Testing message 1", "run_id": RUN_ID_1, "extra": "value 1"},
    {"message": "Testing message 2", "run_id": RUN_ID_1, "extra": "value 2"},
    {"message": "Testing message 3", "run_id": RUN_ID_1, "extra": "value 3"},
]
test_messages_2 = [
    {"message": "Testing message 4", "run_id": RUN_ID_2, "extra": "value 1"},
    {"message": "Testing message 5", "run_id": RUN_ID_2, "extra": "value 2"},
    {"message": "Testing message 6", "run_id": RUN_ID_2, "extra": "value 3"},
]

def push_initial_test_messages():
    redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    print(f"Pushing {len(test_messages_1)} test messages to stream `{REDIS_STREAM}`")

    for msg in test_messages_1:
        redis_client.xadd(REDIS_STREAM, {"json": json.dumps(msg)})
        print(f"  → Sent: {msg}")

def wait_for_processing(timeout, test_messages, run_id):
    print(f"Waiting up to {timeout} seconds for Celery to process messages...")
    start_time = time.time()

    expected_messages = set(m["message"] for m in test_messages)

    while time.time() - start_time < timeout:
        stored_messages = Message.objects.filter(
            json_body__run_id=run_id,
            message__in=expected_messages
        )
        found_messages = set(stored_messages.values_list("message", flat=True))

        if found_messages >= expected_messages:
            print("All messages processed and saved.")
            return stored_messages

        missing = expected_messages - found_messages
        print(f"⏳ Still waiting... Missing: {missing}")
        time.sleep(1)

    print("Timed out waiting for all messages.")
    return Message.objects.filter(
        json_body__run_id=run_id,
        message__in=expected_messages
    )

def push_second_test_messages():
    redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    print(f"Pushing {len(test_messages_2)} test messages to stream `{REDIS_STREAM}`")

    for msg in test_messages_2:
        redis_client.xadd(REDIS_STREAM, {"json": json.dumps(msg)})
        print(f"  → Sent: {msg}")

def main():
    push_initial_test_messages()
    wait_for_processing(timeout=20, test_messages=test_messages_1, run_id=RUN_ID_1)
    
    
    print("waiting 20 seconds. try killing celery and beat")
    time.sleep(20)
    
    # Now that Celery has stopped listening
    push_second_test_messages()
    
    print("waiting 20 seconds. start celery and beat again")
    time.sleep(20)
    
    wait_for_processing(timeout=20, test_messages=test_messages_2, run_id=RUN_ID_2)

if __name__ == "__main__":
    main()
