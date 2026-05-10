#!/bin/bash

echo "Welcome to the Django Scaffold Configuration Script!"
echo "This will configure your env.public.yaml."

read -p "Do you want to use PostgreSQL? [Y/n] " use_postgres
read -p "Do you want to use Redis? [Y/n] " use_redis
read -p "Do you want to use Celery? [Y/n] " use_celery

use_postgres=${use_postgres:-y}
use_redis=${use_redis:-y}
use_celery=${use_celery:-y}

cat <<EOF > env.public.yaml
debug: true
use:
EOF

if [[ $use_postgres =~ ^[Yy]$ ]]; then
    echo "  postgres: true" >> env.public.yaml
else
    echo "  postgres: false" >> env.public.yaml
fi

if [[ $use_redis =~ ^[Yy]$ ]]; then
    echo "  redis: true" >> env.public.yaml
else
    echo "  redis: false" >> env.public.yaml
fi

if [[ $use_celery =~ ^[Yy]$ ]]; then
    echo "  celery: true" >> env.public.yaml
else
    echo "  celery: false" >> env.public.yaml
fi

if [[ $use_postgres =~ ^[Yy]$ ]]; then
cat <<EOF >> env.public.yaml
postgres:
  db: postgres
  user: postgres
  password: postgres
  host: postgres
  port: 5432
EOF
fi

if [[ $use_redis =~ ^[Yy]$ ]]; then
cat <<EOF >> env.public.yaml
redis:
  url: redis://redis:6379/1
EOF
fi

if [[ $use_celery =~ ^[Yy]$ ]]; then
cat <<EOF >> env.public.yaml
celery:
  broker_url: redis://redis:6379/0
  result_backend: redis://redis:6379/0
EOF
fi

echo "Configuration saved to env.public.yaml."
echo "Run \`python generate_env.py\` to update your .env file."
