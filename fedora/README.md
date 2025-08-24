## Create Application root

``` bash
# Create project root
poetry new --src fedora
cd fedora

# Poetry created a Python package called fedora inside src/ by default. This is standard behavior for poetry new.
rm -rf src/fedora

# Add Django
poetry add django
poetry add djangorestframework

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

``` bash
# Create Django apps inside src/
cd src

poetry run python manage.py startapp people
cd ..
```

## Update Settings

``` python
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    
    ...
    
    'rest_framework',
    'people.apps.PeopleConfig'
]
```

## Load People Fixture

``` bash
poetry run python src/manage.py loaddata people

# Test
curl http://127.0.0.1:8000/people/list | python -m json.tool # pretty print
```