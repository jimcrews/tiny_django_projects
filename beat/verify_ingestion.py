import os
import json
import time
from redis import Redis
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from echo.models import Message

# Redis config (check poll_echo_responses task)
REDIS_HOST = "localhost"
REDIS_PORT = 6399
REDIS_STREAM = "echo_responses"
REDIS_DB = 0

# Test data
test_messages = [
    {"message": "Testing message 1", "extra": "value 1"},
    {"message": "Testing message 2", "extra": "value 2"},
    {"message": "Testing message 3", "extra": "value 3"},
]

def push_test_messages():
    redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    print(f"Pushing {len(test_messages)} test messages to stream `{REDIS_STREAM}`")

    for msg in test_messages:
        redis_client.xadd(REDIS_STREAM, {"json": json.dumps(msg)})
        print(f"  → Sent: {msg}")

def wait_for_processing(timeout=20):
    print(f"Waiting up to {timeout} seconds for Celery to process messages...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        stored_messages = Message.objects.filter(
            message__in=[m["message"] for m in test_messages]
        )
        if stored_messages.count() >= len(test_messages):
            print("All messages processed and saved.")
            return stored_messages
        time.sleep(1)

    print("Timed out waiting for all messages.")
    return Message.objects.filter(message__in=[m["message"] for m in test_messages])

def main():
    push_test_messages()
    processed = wait_for_processing()

    print("\nSaved Messages:")
    for m in processed:
        print(f"  - {m.message} | {json.dumps(m.json_body)}")

if __name__ == "__main__":
    main()
