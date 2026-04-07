# NexusHR

NexusHR is a next-generation HRMS platform scaffold that now includes a branded public website, advanced login/create-account flows, and a logged-in employee dashboard with:

- Monthly attendance calendar with attendance, leave, holiday, and anomaly markers
- Alerts and notification center with tagged employee actions
- LangGraph-powered HR copilot with streaming responses and RAG retrieval
- Unified FastAPI backend with tenant-aware JWT auth, RBAC, SSO launch hooks, Redis caching, Mongo-backed audit logging, and PostgreSQL/pgvector persistence

## What is in this repo

- `apps/web`: Next.js 16 + Tailwind responsive branding site, auth flows, and employee dashboard
- `backend`: Unified FastAPI application for auth, dashboard, attendance, leave, payroll, performance, notifications, assistant, and audit
- `services/shared`: Shared security and audit middleware used across backend modules
- `infra`: Docker Compose, Kubernetes YAML, and Helm chart scaffolding
- `docs`: Architecture, ERD, and RAG/cache/indexing documentation
- `scripts`: Local startup and shutdown helpers for Docker and direct backend development

## Platform capabilities

- Employee lifecycle foundations: employee records, onboarding scaffolds, document-ready auth, role-aware employee APIs
- Attendance and leave: geofence-aware check-in, monthly attendance calendar API, leave approvals, leave balances, holiday visibility
- Payroll and compliance: payroll summary/preview endpoints, EPF/ESI/TDS-ready scaffolding, immutable audit coverage
- Performance management: OKRs, 360 feedback entry points, sentiment-ready workflows
- Security: local JWT mode, OIDC/SSO launch hooks, MFA challenge flow, RBAC, org isolation, and audit capture on every write
- AI: LangGraph state machine, pgvector-backed knowledge model, Redis-friendly caching, OpenAI to local-LLM fallback, and SSE streaming

## Demo access

Seeded local credentials:

- Email: `maya.rao@nexushr.example`
- Password: `NexusHR!2026`
- MFA code: `246810`

## Local development

### Option 1: Docker Compose

```bash
npm run compose:up
```

Endpoints:

- Web: `http://localhost:3000`
- Backend: `http://localhost:8007`
- OpenAPI: `http://localhost:8007/docs`
- PostgreSQL with pgvector: `localhost:5433`
- Redis: `localhost:6380`
- MongoDB: `localhost:27017`

Stop the stack:

```bash
npm run compose:down
```

### Option 2: Run web and backend separately

```bash
npm install
npm run dev:web
```

In another terminal:

```powershell
.\scripts\backend-dev.ps1
```

## Backend overview

The backend is a single FastAPI runtime for local simplicity, but it preserves domain-oriented boundaries:

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

Key implementation files:

- Unified app entrypoint: [backend/app/main.py](D:\coledra-code\nexus-hr\backend\app\main.py)
- SQLAlchemy + pgvector models: [backend/app/db/models.py](D:\coledra-code\nexus-hr\backend\app\db\models.py)
- DB bootstrap/session management: [backend/app/db/session.py](D:\coledra-code\nexus-hr\backend\app\db\session.py)
- Dashboard service: [backend/app/services/dashboard.py](D:\coledra-code\nexus-hr\backend\app\services\dashboard.py)
- LangGraph assistant: [backend/app/services/assistant.py](D:\coledra-code\nexus-hr\backend\app\services\assistant.py)
- Vector indexing and retrieval: [backend/app/services/vector_store.py](D:\coledra-code\nexus-hr\backend\app\services\vector_store.py)
- Shared JWT/RBAC/auth middleware: [services/shared/nexus_shared/security.py](D:\coledra-code\nexus-hr\services\shared\nexus_shared\security.py)

## Frontend overview

The frontend includes:

- Branded product landing page: [apps/web/src/app/page.tsx](D:\coledra-code\nexus-hr\apps\web\src\app\page.tsx)
- Advanced login flow wired to backend auth: [apps/web/src/components/auth/login-switcher.tsx](D:\coledra-code\nexus-hr\apps\web\src\components\auth\login-switcher.tsx)
- Employee dashboard with live calendar, alerts, and copilot: [apps/web/src/components/dashboard/dashboard-shell.tsx](D:\coledra-code\nexus-hr\apps\web\src\components\dashboard\dashboard-shell.tsx)

## Environment and scripts

- Example environment file: [.env.example](D:\coledra-code\nexus-hr\.env.example)
- Docker startup: [scripts/dev-up.ps1](D:\coledra-code\nexus-hr\scripts\dev-up.ps1)
- Docker shutdown: [scripts/dev-down.ps1](D:\coledra-code\nexus-hr\scripts\dev-down.ps1)
- Direct backend run: [scripts/backend-dev.ps1](D:\coledra-code\nexus-hr\scripts\backend-dev.ps1)

## CI/CD and deployment

- GitHub Actions CI: [.github/workflows/ci.yml](D:\coledra-code\nexus-hr\.github\workflows\ci.yml)
- Docker publish workflow: [.github/workflows/docker-release.yml](D:\coledra-code\nexus-hr\.github\workflows\docker-release.yml)
- Helm chart: [infra/helm/nexushr/Chart.yaml](D:\coledra-code\nexus-hr\infra\helm\nexushr\Chart.yaml)
- Helm values: [infra/helm/nexushr/values.yaml](D:\coledra-code\nexus-hr\infra\helm\nexushr\values.yaml)

## Documentation

- Architecture diagram: [docs/architecture.md](D:\coledra-code\nexus-hr\docs\architecture.md)
- Core ERD: [docs/core-erd.md](D:\coledra-code\nexus-hr\docs\core-erd.md)
- RAG, caching, and indexing strategy: [docs/rag-and-cache.md](D:\coledra-code\nexus-hr\docs\rag-and-cache.md)

## Verification commands

```bash
npm run lint:web
npm run build:web
cd backend && python -m pytest
python -m compileall backend services/shared
```

## Security and compliance baseline

- GDPR-aware data minimization, access scoping, and auditability
- ISO 27001-aligned controls for least privilege, traceability, secrets isolation, and environment segregation
- Immutable-style write audit trail with timestamp, IP address, user identifier, tenant, and route data
- Tenant-aware JWT and route-level RBAC enforcement for employees, managers, HR managers, and super admins
