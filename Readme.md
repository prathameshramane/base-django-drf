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

Once configured, generate your `.env` file. You can also provide overrides or secrets by creating a `env.private.yaml` file (see `env.private.example.yaml` for guidance). Note that `.env` is NOT tracked by git.

```bash
python generate_env.py
```

## Running the Application

We have included `run.sh` and `run.py` to simplify Docker commands, as they automatically use the COMPOSE_PROFILES generated in your `.env`.

To run the local development server (along with configured services):
```bash
./run.sh
# or python run.py
```

To run in production locally using Gunicorn:
```bash
./run.sh prod
```

### Advanced Run Commands
You can append flags to `restart` to build images:
- `./run.sh restart` (Restarts all containers)
- `./run.sh restart --build` (Builds and restarts containers)
- `./run.sh restart --build --nocache` (Builds without cache and restarts)

To completely prune images and do a fresh start:
- `./run.sh rebuild`

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
