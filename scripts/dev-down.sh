#!/usr/bin/env bash
set -euo pipefail

docker compose -f infra/docker-compose.yml down
echo "NexusHR stack has been stopped."
