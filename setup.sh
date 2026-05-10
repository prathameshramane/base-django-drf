#!/bin/bash

echo "Welcome to the Django Scaffold Configuration Script!"
echo "This will configure your env.public.yaml."

read -p "Do you want to use PostgreSQL? [Y/n] " use_postgres
read -p "Do you want to use Redis? [Y/n] " use_redis
read -p "Do you want to use Celery? [Y/n] " use_celery

use_postgres=${use_postgres:-y}
use_redis=${use_redis:-y}
use_celery=${use_celery:-y}

echo "DEBUG: \"True\"" > env.public.yaml

if [[ $use_postgres =~ ^[Yy]$ ]]; then
    echo "USE_POSTGRES: \"True\"" >> env.public.yaml
    echo "POSTGRES_DB: \"postgres\"" >> env.public.yaml
    echo "POSTGRES_USER: \"postgres\"" >> env.public.yaml
    echo "POSTGRES_PASSWORD: \"postgres\"" >> env.public.yaml
    echo "POSTGRES_HOST: \"postgres\"" >> env.public.yaml
    echo "POSTGRES_PORT: \"5432\"" >> env.public.yaml
else
    echo "USE_POSTGRES: \"False\"" >> env.public.yaml
fi

if [[ $use_redis =~ ^[Yy]$ ]]; then
    echo "USE_REDIS: \"True\"" >> env.public.yaml
    echo "REDIS_URL: \"redis://redis:6379/1\"" >> env.public.yaml
else
    echo "USE_REDIS: \"False\"" >> env.public.yaml
fi

if [[ $use_celery =~ ^[Yy]$ ]]; then
    echo "USE_CELERY: \"True\"" >> env.public.yaml
    echo "CELERY_BROKER_URL: \"redis://redis:6379/0\"" >> env.public.yaml
    echo "CELERY_RESULT_BACKEND: \"redis://redis:6379/0\"" >> env.public.yaml
else
    echo "USE_CELERY: \"False\"" >> env.public.yaml
fi

echo "Configuration saved to env.public.yaml."
echo "Run \`python generate_env.py\` to update your .env file."
