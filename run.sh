#!/bin/bash

# Ensure .env exists
if [ ! -f .env ]; then
  echo "Error: .env file not found. Please run 'python generate_env.py' first."
  exit 1
fi

COMMAND=$1
shift

BUILD=""
NOCACHE=""

# Parse additional arguments
for arg in "$@"; do
    if [ "$arg" == "--build" ]; then
        BUILD="--build"
    fi
    if [ "$arg" == "--nocache" ]; then
        NOCACHE="--no-cache"
    fi
done

if [ -z "$COMMAND" ]; then
    # Default to dev server
    echo "Starting development server..."
    docker compose -f docker-compose.dev.yml up $BUILD $NOCACHE
elif [ "$COMMAND" == "prod" ]; then
    echo "Starting production server locally..."
    docker compose -f docker-compose.prod.yml up $BUILD $NOCACHE
elif [ "$COMMAND" == "restart" ]; then
    echo "Restarting containers..."
    docker compose -f docker-compose.dev.yml restart
    if [ -n "$BUILD" ]; then
        echo "Building and starting..."
        docker compose -f docker-compose.dev.yml up $BUILD $NOCACHE -d
    fi
elif [ "$COMMAND" == "rebuild" ]; then
    echo "Rebuilding containers completely..."
    docker compose -f docker-compose.dev.yml down -v
    docker image prune -a -f
    docker compose -f docker-compose.dev.yml build --no-cache
    docker compose -f docker-compose.dev.yml up -d
else
    echo "Unknown command: $COMMAND"
    echo "Available commands:"
    echo "  (none)      - Start dev server"
    echo "  prod        - Start prod server locally"
    echo "  restart     - Restart containers (supports --build, --nocache)"
    echo "  rebuild     - Down containers, prune images, build no-cache, and start"
fi
