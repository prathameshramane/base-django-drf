# Django Scaffold

A modern, scalable Django scaffold built with Docker, Postgres, Redis, and Celery. This project is configured to help you start quickly with best practices, including reusable base models, swagger documentation, and dynamic environment toggling.

## Features

- **Latest Django & DRF**: Uses Django 5.x and Django REST Framework.
- **Dockerized**: Fully orchestrated via `docker-compose` for both development and production.
- **Services on Demand**: Toggle PostgreSQL, Redis, and Celery (with Beat) dynamically via environment variables and Docker profiles.
- **Dynamic Env Loader**: Combines public (committed) and private (ignored) YAML configs to dynamically generate `.env`.
- **Swagger Documentation**: Out-of-the-box API schema generation using `drf-spectacular`.
- **Reusable Core Models**: Includes `UUIDModel`, `TimeStampedModel`, `SoftDeleteModel`, and `VersionedModel` in the `core` app.
- **Sample App**: Includes a `sample` app to demonstrate best practices (Models, Views, Serializers, Services, URLs).

## Setup & Configuration

### 1. Configure the Stack

Run the interactive setup script to choose whether to enable PostgreSQL, Redis, and Celery. The script modifies `env.public.yaml`.

For Linux/Mac:
```bash
./setup.sh
```

For Windows (or cross-platform):
```bash
python setup.py
```

### 2. Generate `.env` File

Once configured (and after optionally adding secrets to `env.private.yaml`), generate your `.env` file:
```bash
python generate_env.py
```

## Running the Application

### Development (Docker)

To run the local development server (along with configured services like Postgres/Redis/Celery):
```bash
docker-compose -f docker-compose.dev.yml --profile web --profile postgres --profile redis --profile celery up --build
```
*(You only need to include the `--profile` flags for the services you enabled in setup).*

### Production (Docker)

To run in production using Gunicorn:
```bash
docker-compose -f docker-compose.prod.yml --profile web --profile postgres --profile redis --profile celery up --build -d
```

## Local Development (Without Docker)

You can also run the server without Docker (assuming you have dependencies installed in a virtual environment):
```bash
python manage.py runserver --settings=backend.settings.development
```

## API Documentation (Swagger)

When the server is running, you can access the Swagger UI documentation at:
- `http://localhost:8000/api/schema/swagger-ui/`
- Redoc is available at `http://localhost:8000/api/schema/redoc/`

## Reusable Models & The Sample App

- **`core/models.py`**: Contains base abstract models you can inherit from (e.g., `CoreModel`).
- **`sample/`**: A fully functional app showing how to inherit from `CoreModel`, create serializers, and expose endpoints via ViewSets. Check `sample/views.py` and `sample/serializers.py` for examples.
