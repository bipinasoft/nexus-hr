$ErrorActionPreference = "Stop"

docker compose -f infra/docker-compose.yml down
Write-Host "NexusHR stack has been stopped."
