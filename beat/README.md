# Sample Celery Beat App

## Create Application root

``` bash
# Create project root
poetry new --src beat
cd beat

# Poetry created a Python package called beat inside src/ by default. This is standard behavior for poetry new.
rm -rf src/beat

# Add Django
poetry add django
poetry add celery
poetry add django-celery-beat
poetry add redis

# Create the main Django project
poetry run django-admin startproject config src
```

## Update `pyproject.toml`

First Update pyproject.toml so that poetry treats all packages inside src/ as source code

``` toml
packages = [{include = "*", from = "src"}]
```

## Django commands

``` bash
# Install dependencies

poetry install

# Apply database migrations
poetry run python src/manage.py migrate

# Create a superuser (admin / pass)
poetry run python src/manage.py createsuperuser

# Run the development server
poetry run python src/manage.py runserver
```

## Create Django App

This is the App that will run the Redis Messaging

``` bash
# Create Django apps inside src/
cd src

poetry run python manage.py startapp echo
cd ..
```

## Update Settings

``` python
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    
    ...
    'django_celery_beat',
    'echo.apps.EchoConfig'
]
```

## Add Celery Config

Update `src/config/celery.py` and `src/config/__init__.py`.

Update `settings.py`:

``` python
# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Change if using Docker or a different host
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'  # Optional, for storing results
CELERY_TIMEZONE = 'UTC'
```

Update `src/echo/tasks.py`


## Add a Periodic Task in Admin Panel

Task (custom): `echo.tasks.say_hello` or `echo.tasks.poll_echo_responses`
Interval Schedule: every 10 seconds

---

## Run App with Celery:

``` shell
# docker start redis and redis-test
# Redis Server (Celery Broker)
docker run -d -p 6379:6379 --name redis redis

# Redis Server (Message Queue)
docker run -d --name redis-test -p 6399:6379 redis:7-alpine

# Run Django App (optional)
poetry run python src/manage.py runserver

# Celery worker (required)
poetry run celery -A config worker --loglevel=info

# Celery Beat (periodic tasks)
poetry run celery -A config beat -l info -S django
```

---

## Run Test Script

Add messages manually
``` shell
# connect to redis
docker exec -it redis-test redis-cli

# Add messages

XADD echo_responses * json '{"message": "Testing", "something": "value 1", "another": "value 2"}'
```

Or run the test scripts

``` shell
poetry run python verify_ingestion.py
poetry run python high_volume_test.py
```


## Destroy and Clean

``` shell
rm src/db.sqlite3
poetry run python src/manage.py migrate
poetry run python src/manage.py createsuperuser
```
