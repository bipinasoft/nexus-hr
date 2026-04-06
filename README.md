# NexusHR

NexusHR is a next-generation HRMS scaffold built around microservices, domain-driven boundaries, and security-first HR workflows. This repository includes:

- A branded Next.js + Tailwind web experience with a landing page, login page, and create-account journey.
- A unified FastAPI backend that serves identity, employee lifecycle, attendance, payroll, performance, and audit domains from one application.
- Shared OpenID Connect, RBAC, and audit middleware for compliance-oriented write operations.
- Infrastructure scaffolding for Docker, Kubernetes, PostgreSQL, Redis, MongoDB, and S3-compatible document storage.

## Core capabilities

- Employee lifecycle: onboarding, document signing orchestration, asset tracking, org hierarchy, offboarding.
- Attendance and leave: geofencing-aware check-in flow, leave balances, policy-based accruals, approval chains.
- Payroll and compliance: payroll runs, dynamic calculation hooks, payslip generation, statutory reporting.
- Performance management: OKRs, 360 feedback, review cycles, AI-sentiment integration point.
- Security and compliance: OpenID Connect, OAuth2, MFA-ready login patterns, RBAC, audit logging, GDPR and ISO 27001 control mapping.

## Repository structure

```text
nexus-hr/
|-- apps/
|   `-- web/                     # Next.js branding site + auth UX
|-- backend/                     # Unified FastAPI backend with modular HR routers
|-- docs/
|   |-- architecture.md         # Mermaid system diagram + architecture decisions
|   `-- core-erd.md             # Mermaid ERD for the HR core domain
|-- infra/
|   |-- docker-compose.yml      # Local platform dependencies and service wiring
|   `-- kubernetes/
|       `-- nexushr-platform.yaml
|-- services/
|   |-- shared/                 # Shared auth, RBAC, and audit package
|   |-- auth-service/           # Legacy per-domain service scaffold
|   |-- employee-service/       # Legacy per-domain service scaffold
|   |-- attendance-service/     # Legacy per-domain service scaffold
|   |-- payroll-service/        # Legacy per-domain service scaffold
|   |-- performance-service/    # Legacy per-domain service scaffold
|   `-- audit-service/          # Legacy per-domain service scaffold
`-- package.json                # Workspace scripts for the web app
```

## Getting started

### Frontend

```bash
npm install
npm run dev:web
```

### Backend

The backend now runs as one FastAPI application:

```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

That single app exposes all domain routes under one API surface:

- `/v1/auth/*`
- `/v1/employees/*`
- `/v1/attendance/*`
- `/v1/leaves/*`
- `/v1/payroll/*`
- `/v1/performance/*`
- `/v1/audit/*`

Use `/health` for the backend and `/health/domains` for a domain-level summary.

### Docker Compose

When running through Docker Compose, the backend is exposed on `http://localhost:8007` to avoid host-port clashes with other local services.

## Compliance baseline

- GDPR: data minimization, role-scoped access, auditability, encryption in transit and at rest, deletion workflow hooks.
- ISO 27001 alignment: centralized identity, least privilege, immutable audit trails, secure configuration boundaries, environment segregation.
- Audit logging: every write request is captured with timestamp, IP address, user ID, service, route, method, and response status.

## Local deployment profile

- Production target: microservice boundaries remain documented for future extraction and scaling.
- Local development target: one backend process is easier to run, debug, document, and test end-to-end.
- Domain isolation is preserved in router modules under [backend/app/routers](D:\coledra-code\nexus-hr\backend\app\routers).

## Key deliverables

- System architecture diagram: [docs/architecture.md](D:\coledra-code\nexus-hr\docs\architecture.md)
- Core HR database ERD: [docs/core-erd.md](D:\coledra-code\nexus-hr\docs\core-erd.md)
- Unified backend entrypoint: [backend/app/main.py](D:\coledra-code\nexus-hr\backend\app\main.py)
- Authentication middleware boilerplate: [services/shared/nexus_shared/security.py](D:\coledra-code\nexus-hr\services\shared\nexus_shared\security.py) and [services/shared/nexus_shared/audit.py](D:\coledra-code\nexus-hr\services\shared\nexus_shared\audit.py)
