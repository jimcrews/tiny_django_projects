Sample docker application using Poetry and Docker Compose

## Local Development (Poetry)

### Install dependencies
poetry install

### Create migration files
poetry run python src/manage.py makemigrations

### Apply migrations
poetry run python src/manage.py migrate

### Create admin user
poetry run python src/manage.py createsuperuser

### Start dev server
poetry run python src/manage.py runserver

---

## Production Deployment (Docker)

### Build the Docker image
docker build -t my-django-app .

### Run with docker-compose
docker-compose up --build


To run DB migrations and create a superuser inside the container:


docker-compose exec web python src/manage.py migrate
docker-compose exec web python src/manage.py createsuperuser
