# Django Backend using GraphQL

The back end of the blog will be built using Django, including an admin interface for managing blog content. The content data will then be exposed through a GraphQL API.

***TODO: Create front-end***

## Django Setup

Start by setting up the Django Manangement and Blog Apps

### Initial Setup Steps

``` bash
# Create project root
mkdir react_django
cd react_django

# Setup django backend using Poetry
poetry new --src backend
cd backend

rm -r src/backend # remove the default app here. We'll replace with Django

# Install Django and create the Django Management (config) App
poetry add django
poetry run django-admin startproject config src
```

Project Structure in place:

``` text
react_django/
├── backend/
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── README.md
│   ├── src/
│   │   ├── db.sqlite3
│   │   ├── manage.py
│   │   └── config/
│   │       ├── __init__.py
│   │       ├── asgi.py
│   │       ├── settings.py
│   │       ├── urls.py
│   │       └── wsgi.py
│   └── tests/
│       └── __init__.py
└── README.md
```

Update `pyproject.toml`:

``` toml
[tool.poetry]
packages = [{ include = "config", from = "src" }]
```

### Django Commands

Commands should be run in the `backend` folder

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


### Create the Blog Application

``` bash
# Create Django apps inside src/
cd src
poetry run python manage.py startapp blog
```

``` text
react_django/
├── README.md
├── backend/
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── README.md
│   ├── src/
│   │   ├── db.sqlite3
│   │   ├── manage.py
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   ├── asgi.py
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   └── wsgi.py
│   │   └── blog/
│   │       ├── __init__.py
│   │       ├── admin.py
│   │       ├── apps.py
│   │       ├── models.py
│   │       ├── tests.py
│   │       ├── views.py
│   │       └── migrations/
│   │           └── __init__.py
│   └── tests/
│       └── __init__.py
```

### Setup Blog

Add `blog.apps.BlogConfig` to `INSTALLED_APPS`. Update `backend/src/blog/models.py`, and `backend/src/blog/admin.py`

``` bash
poetry run python src/manage.py makemigrations
poetry run python src/manage.py migrate
```

***At this point, enough of the back end has been completed to proceed with Django’s URL routing and templates; however, it will be wrapped in a GraphQL API instead.***

## GraphQL

``` bash
poetry add graphene-django
```

 - Add `graphene_django` to `INSTALLED_APPS`
 - In `settings.py`, point use `GRAPHENE` to point `SCHEMA` to `blog.schema.schema`

### Graph URL

To enable Django to serve the GraphQL endpoint and the GraphiQL interface, a new URL pattern should be added to `backend/src/config/urls.py`. This URL will be directed to Graphene-Django’s GraphQLView. Since the Django template engine’s cross-site request forgery (CSRF) protection features are not being used, Django’s csrf_exempt decorator must be imported and applied to mark the view as exempt from CSRF protection.

The graphiql=True argument tells Graphene-Django to make the GraphiQL interface available.

Create the GraphQL schema - `backend/src/blog/schema.py`

### Test it

 - Add some blog posts here - `http://127.0.0.1:8000/admin`
 - Check graphiql here - `http://127.0.0.1:8000/graphql`

Try the following query:

``` graphql
{
  allPosts {
    title
    author {
      user {
        username
      }
    }
    tags {
      name
    }
  }
}
```

## CORS

Since the frontend and backend run on different ports locally—and possibly different domains in production - CORS must be configured to prevent the browser from blocking requests. The `django-cors-headers` package can be used to allow Django to accept requests from other origins, enabling frontend communication with the GraphQL API.

``` bash
poetry add django-cors-headers
```

### Update Settings for CORS

 - Add `corsheaders` to `INSTALLED_APPS`
 - Add `corsheaders.middleware.CorsMiddleware` to the beginning of the `MIDDLEWARE` list
 - Add `CORS_ALLOWED_ORIGINS`