import os
import json
import time
import uuid
from redis import Redis
import django
import subprocess

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from echo.models import Message

# Redis config
REDIS_HOST = "localhost"
REDIS_PORT = 6399
REDIS_STREAM = "echo_responses"
REDIS_DB = 0
REDIS_CONTAINER_NAME = "redis-test"

# Generate unique run IDs
RUN_ID_1 = str(uuid.uuid4())
RUN_ID_2 = str(uuid.uuid4())

# Generate high volume test messages
def generate_test_messages(run_id, count=500):
    return [
        {
            "message": f"High Volume Message {i}",
            "run_id": run_id,
            "index": i
        }
        for i in range(count)
    ]

test_messages_1 = generate_test_messages(RUN_ID_1)
test_messages_2 = generate_test_messages(RUN_ID_2)

def push_messages(test_messages, label):
    redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    print(f"\n📤 Pushing {len(test_messages)} {label} messages to stream `{REDIS_STREAM}`")

    for msg in test_messages:
        redis_client.xadd(REDIS_STREAM, {"json": json.dumps(msg)})

    print(f"✅ {label} messages pushed.")

def wait_for_processing(timeout, test_messages, run_id):
    print(f"\n⏳ Waiting up to {timeout} seconds for Celery to process {len(test_messages)} messages...")
    start_time = time.time()

    expected = set(m["message"] for m in test_messages)

    while time.time() - start_time < timeout:
        found = set(
            Message.objects.filter(json_body__run_id=run_id)
            .values_list("message", flat=True)
        )

        if found >= expected:
            print(f"✅ All {len(test_messages)} messages processed.")
            return

        missing = expected - found
        print(f"Still waiting... {len(missing)} missing")
        time.sleep(2)

    print(f"Timeout. {len(expected - found)} messages still missing.")

def stop_redis():
    print("\nStopping Redis...")
    subprocess.run(["docker", "stop", REDIS_CONTAINER_NAME], check=True)
    print("Redis stopped.")

def start_redis():
    print("\nRestarting Redis...")
    subprocess.run(["docker", "start", REDIS_CONTAINER_NAME], check=True)
    print("Redis restarted.")

def main():
    # Push initial batch and verify
    push_messages(test_messages_1, label="initial")
    wait_for_processing(timeout=30, test_messages=test_messages_1, run_id=RUN_ID_1)

    # Simulate Redis downtime
    stop_redis()
    print("\nRedis is down for 10 seconds...")
    time.sleep(10)
    start_redis()

    # Push second batch while Redis is back up
    push_messages(test_messages_2, label="second")
    wait_for_processing(timeout=30, test_messages=test_messages_2, run_id=RUN_ID_2)

if __name__ == "__main__":
    main()
