$ErrorActionPreference = "Stop"

if (-not $env:NEXUSHR_DATABASE_URL) {
  $env:NEXUSHR_DATABASE_URL = "postgresql+asyncpg://nexushr:nexushr@localhost:5433/nexushr"
}
if (-not $env:NEXUSHR_REDIS_URL) {
  $env:NEXUSHR_REDIS_URL = "redis://localhost:6380/0"
}
if (-not $env:NEXUSHR_MONGODB_AUDIT_URI) {
  $env:NEXUSHR_MONGODB_AUDIT_URI = "mongodb://localhost:27017"
}
if (-not $env:NEXUSHR_AUTH_MODE) {
  $env:NEXUSHR_AUTH_MODE = "local"
}
if (-not $env:NEXUSHR_JWT_SECRET) {
  $env:NEXUSHR_JWT_SECRET = "nexus-hr-local-secret"
}

Push-Location backend
try {
  python -m uvicorn app.main:app --reload --port 8007
} finally {
  Pop-Location
}
