$ErrorActionPreference = "Stop"

docker compose -f infra/docker-compose.yml up -d --build
Write-Host "NexusHR stack is starting on http://localhost:3000 and http://localhost:8007"
