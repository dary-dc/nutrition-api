#!/bin/bash
set -e

if [ "$1" == "prod" ]; then
    echo "🚀 Starting Nutrition API in PRODUCTION mode..."
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
elif [ "$1" == "dev" ]; then
    echo "⚙️ Starting Nutrition API in DEVELOPMENT mode..."
    docker-compose up --build
else
    echo "Usage: ./run.sh [dev|prod]"
    exit 1
fi
