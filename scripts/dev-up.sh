#!/usr/bin/env bash
set -euo pipefail

docker compose -f infra/docker-compose.yml up -d --build
echo "NexusHR stack is starting on http://localhost:3000 and http://localhost:8007"
