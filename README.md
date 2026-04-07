# NexusHR

NexusHR is a next-generation HRMS platform scaffold with:

- A branded product website and polished login/create-account flows
- A logged-in employee dashboard with attendance calendar, leave markers, holidays, alerts, and notifications
- A unified FastAPI backend with JWT auth, RBAC, MFA, SSO launch hooks, Redis caching, Mongo-backed audit logging, and PostgreSQL/pgvector persistence
- LangGraph-based assistant flows with streaming responses and RAG-ready retrieval

## Repo structure

- `apps/web` - Next.js 16 + Tailwind CSS frontend
- `backend` - unified FastAPI backend
- `infra` - Docker Compose, Kubernetes manifests, and Helm chart
- `docs` - architecture, ERD, and RAG/cache documentation
- `scripts` - startup and shutdown helper scripts

## Prerequisites

Choose the setup path you want:

### For the fastest start

- Docker Desktop

### For local development without running everything in containers

- Node.js 22 recommended
- npm 10+
- Python 3.13+
- Docker Desktop for PostgreSQL, Redis, and MongoDB

## Demo credentials

Use these seeded credentials after startup:

- Email: `maya.rao@nexushr.example`
- Password: `NexusHR!2026`
- MFA code: `246810`

## Quick start with Docker Compose

This is the easiest way to run the full application.

### 1. Clone the repository

```bash
git clone https://github.com/bipinasoft/nexus-hr.git
cd nexus-hr
```

### 2. Start the full stack

```bash
docker compose -f infra/docker-compose.yml up -d --build
```

Windows PowerShell shortcut:

```powershell
.\scripts\dev-up.ps1
```

macOS/Linux shortcut:

```bash
./scripts/dev-up.sh
```

### 3. Open the application

- Website / login: `http://localhost:3000`
- Website / login: `http://127.0.0.1:3000`
- Backend API: `http://localhost:8007`
- OpenAPI docs: `http://localhost:8007/docs`
- Health endpoint: `http://localhost:8007/health`

### 4. Stop the stack

```bash
docker compose -f infra/docker-compose.yml down
```

Windows PowerShell shortcut:

```powershell
.\scripts\dev-down.ps1
```

macOS/Linux shortcut:

```bash
./scripts/dev-down.sh
```

## Local development

Use this when you want the frontend and backend running on your machine with live reload, while PostgreSQL, Redis, and MongoDB run in Docker.

### 1. Clone the repository

```bash
git clone https://github.com/bipinasoft/nexus-hr.git
cd nexus-hr
```

### 2. Install frontend dependencies

```bash
npm install
```

### 3. Create a Python virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

### 4. Start only the infrastructure services

```bash
docker compose -f infra/docker-compose.yml up -d postgres redis mongo
```

This starts:

- PostgreSQL with pgvector on `localhost:5433`
- Redis on `localhost:6380`
- MongoDB on `localhost:27017`

### 5. Start the backend

Windows PowerShell:

```powershell
.\scripts\backend-dev.ps1
```

This script sets the local defaults for:

- `NEXUSHR_DATABASE_URL=postgresql+asyncpg://nexushr:nexushr@localhost:5433/nexushr`
- `NEXUSHR_REDIS_URL=redis://localhost:6380/0`
- `NEXUSHR_MONGODB_AUDIT_URI=mongodb://localhost:27017`
- `NEXUSHR_AUTH_MODE=local`
- `NEXUSHR_JWT_SECRET=nexus-hr-local-secret`

macOS/Linux:

```bash
export NEXUSHR_DATABASE_URL=postgresql+asyncpg://nexushr:nexushr@localhost:5433/nexushr
export NEXUSHR_REDIS_URL=redis://localhost:6380/0
export NEXUSHR_MONGODB_AUDIT_URI=mongodb://localhost:27017
export NEXUSHR_AUTH_MODE=local
export NEXUSHR_JWT_SECRET=nexus-hr-local-secret
cd backend
python -m uvicorn app.main:app --reload --port 8007
```

### 6. Start the frontend

Open a new terminal in the repository root:

```bash
npm run dev:web
```

### 7. Open the application

- Frontend: `http://localhost:3000`
- Frontend: `http://127.0.0.1:3000`
- Backend: `http://localhost:8007`
- OpenAPI docs: `http://localhost:8007/docs`

## Environment variables

An example environment file is available at [`.env.example`](./.env.example).

Important values:

- `NEXT_PUBLIC_API_BASE_URL` - frontend API base URL
- `NEXUSHR_DATABASE_URL` - PostgreSQL connection string
- `NEXUSHR_REDIS_URL` - Redis connection string
- `NEXUSHR_MONGODB_AUDIT_URI` - MongoDB connection string
- `NEXUSHR_AUTH_MODE` - `local` for seeded demo login
- `NEXUSHR_JWT_SECRET` - JWT signing secret
- `NEXUSHR_OPENAI_API_KEY` - optional OpenAI key for assistant fallback strategy

## Useful commands

From the repository root:

```bash
npm run compose:up
npm run compose:down
npm run dev:backend
npm run dev:web
npm run build:web
npm run lint:web
npm run build:backend
npm run test:backend
npm run test:e2e
```

## Main URLs

- Public website: `http://localhost:3000`
- Login page: `http://localhost:3000/login`
- Create account page: `http://localhost:3000/create-account`
- Employee dashboard: `http://localhost:3000/dashboard`
- Backend API docs: `http://localhost:8007/docs`

## Backend routes

The backend is a single FastAPI runtime with domain-based routers:

- `v1/auth/*`
- `v1/dashboard/*`
- `v1/attendance/*`
- `v1/leaves/*`
- `v1/notifications/*`
- `v1/assistant/*`
- `v1/employees/*`
- `v1/payroll/*`
- `v1/performance/*`
- `v1/audit/*`

## Key files

- Frontend landing page: [`apps/web/src/app/page.tsx`](./apps/web/src/app/page.tsx)
- Frontend login page: [`apps/web/src/app/login/page.tsx`](./apps/web/src/app/login/page.tsx)
- Login experience component: [`apps/web/src/components/auth/login-switcher.tsx`](./apps/web/src/components/auth/login-switcher.tsx)
- Employee dashboard shell: [`apps/web/src/components/dashboard/dashboard-shell.tsx`](./apps/web/src/components/dashboard/dashboard-shell.tsx)
- Backend entrypoint: [`backend/app/main.py`](./backend/app/main.py)
- Backend models: [`backend/app/db/models.py`](./backend/app/db/models.py)
- Shared auth and RBAC: [`backend/app/platform/security.py`](./backend/app/platform/security.py)
- Docker Compose: [`infra/docker-compose.yml`](./infra/docker-compose.yml)
- Helm chart: [`infra/helm/nexushr`](./infra/helm/nexushr)

## Verification

The project has been validated with:

```bash
npm run lint:web
npm run build:web
npm run test:backend
```

E2E login verification:

```bash
npm run test:e2e
```

Make sure the frontend and backend are already running before you execute the E2E test.

## Troubleshooting

### Login does not work on local machine

- Open the app using either `http://localhost:3000` or `http://127.0.0.1:3000`
- Make sure the backend is running on `http://localhost:8007`
- Make sure `NEXUSHR_AUTH_MODE=local`
- Use the seeded credentials shown above

### Database or cache connection errors

- Make sure PostgreSQL is running on port `5433`
- Make sure Redis is running on port `6380`
- Make sure MongoDB is running on port `27017`

### Port conflicts

NexusHR intentionally uses:

- PostgreSQL on `5433` instead of `5432`
- Redis on `6380` instead of `6379`
- Backend on `8007`

### pgvector note

The Docker PostgreSQL image already includes pgvector. If you connect NexusHR to your own PostgreSQL instance, install the `pgvector` extension there as well. Without it, vector features may fall back or degrade locally.

## Documentation

- Architecture: [`docs/architecture.md`](./docs/architecture.md)
- Core ERD: [`docs/core-erd.md`](./docs/core-erd.md)
- RAG, caching, and indexing: [`docs/rag-and-cache.md`](./docs/rag-and-cache.md)

## Security baseline

- GDPR-aware access scoping and auditability
- ISO 27001-aligned least-privilege and traceability patterns
- Immutable-style write audit trail with timestamp, IP address, user identifier, tenant, and route data
- Tenant-aware JWT and route-level RBAC for employees, managers, HR managers, and super admins
