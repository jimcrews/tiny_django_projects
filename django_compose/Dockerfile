FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (for caching)
COPY pyproject.toml poetry.lock /app/

# Pin Poetry to 1.8.5 to avoid --no-dev error
RUN pip install --upgrade pip --root-user-action=ignore \
 && pip install poetry==1.8.5 --root-user-action=ignore \
 && poetry config virtualenvs.create false \
 && poetry install --no-dev --no-interaction --no-ansi

# Copy app source code
COPY src /app/src

EXPOSE 8000

CMD ["poetry", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8000"]
