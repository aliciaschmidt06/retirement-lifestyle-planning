#!/bin/bash

set -e

docker compose down

if [ ! -d "scenarios" ]; then
  echo "Creating scenarios directory..."
  mkdir -p "scenarios"
fi

docker compose up --build
