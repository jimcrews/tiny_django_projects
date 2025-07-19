# Tiny Django Projects


Build and run Django apps using Poetry, and use Docker Compose for local development.

---

## Install Poetry

Use PipX (recommended):

```bash
# 1. Install PipX
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# 2. Install Poetry using PipX
pipx install poetry
```

## Create Application root

``` bash
# Create project root
poetry new --src django_compose
cd django_compose

# Poetry created a Python package called django_compose inside src/ by default. This is standard behavior for poetry new.
rm -rf src/django_compose

# Add Django
poetry add django
poetry add celery
poetry add redis

# Create the main Django project
poetry run django-admin startproject config src

# Create Django apps
cd src
# Create Django apps inside src/
poetry run python manage.py startapp todo
poetry run python manage.py startapp emailer # requires celery and redis
cd ..
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

*For local development, update your Django settings to allow all hosts to avoid DisallowedHost errors by adding this in src/config/settings.py:*

``` python
ALLOWED_HOSTS = ['*']
```


## Testing

``` bash
# Add pytest and pytest-django for testing
poetry add --dev pytest pytest-django

```

Add pytest.ini to the root folder

``` ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
pythonpath = src
```

Create a simple test example inside your app, e.g. src/todo/tests/test_sanity.py:

``` python
def test_basic_math():
    assert 1 + 1 == 2
```

Run tests:

``` bash
poetry run pytest
```


## Optional Docker Setup

Add dockerfile and docker-compose.


Run with Docker Compose

``` bash
# Build and start the container
docker-compose up --build

# Stop containers
docker-compose down

```