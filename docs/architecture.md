# NexusHR Architecture

## Architectural principles

- Domain-driven design with clean boundaries even inside the unified local backend
- Security-first identity model with JWT, OIDC/SSO hooks, MFA, and RBAC
- Multi-tenant isolation through org-scoped claims, tenant domains, and org-aware queries
- Production-ready persistence with PostgreSQL, Redis, MongoDB, and pgvector
- AI orchestration through LangGraph with OpenAI to local-LLM fallback

## High-level system architecture

```mermaid
flowchart TB
    subgraph Users["Users"]
        SA["Super Admin"]
        HR["HR Manager"]
        MG["Manager"]
        EM["Employee"]
    end

    subgraph Experience["Experience Layer"]
        WEB["Next.js Web App<br/>Branding, Login, Create Account, Dashboard"]
        WS["WebSocket Notifications"]
        SSE["Streaming Copilot UI"]
    end

    subgraph Security["Identity & Security"]
        JWT["JWT + MFA"]
        SSO["OIDC / Enterprise SSO"]
        RBAC["RBAC + Tenant Scope"]
        AUDIT["Audit Middleware"]
    end

    subgraph Backend["Unified FastAPI Backend"]
        API["Gateway App"]
        AUTH["Auth Domain"]
        DASH["Dashboard Domain"]
        ATT["Attendance & Leave Domain"]
        PAY["Payroll Domain"]
        PERF["Performance Domain"]
        NOTIFY["Notifications Domain"]
        AI["Assistant / LangGraph Domain"]
    end

    subgraph Data["Platform Data Services"]
        PG["PostgreSQL"]
        VEC["pgvector Index"]
        REDIS["Redis Cache / Session Acceleration"]
        MONGO["MongoDB Audit Store"]
        S3["Encrypted Document Storage"]
    end

    subgraph AIStack["AI Runtime"]
        GRAPH["LangGraph State Machine"]
        OPENAI["OpenAI Provider"]
        LOCAL["Local LLM Provider"]
        INDEX["Indexing Pipeline"]
    end

    subgraph Deploy["Deployment"]
        DOCKER["Docker Compose"]
        HELM["Helm Chart"]
        K8S["Kubernetes / EKS / AKS"]
        CI["GitHub Actions CI/CD"]
    end

    SA --> WEB
    HR --> WEB
    MG --> WEB
    EM --> WEB

    WEB --> JWT
    WEB --> SSO
    WEB --> API
    WEB --> WS
    WEB --> SSE

    JWT --> RBAC
    SSO --> RBAC
    RBAC --> AUTH
    AUDIT --> MONGO

    API --> AUTH
    API --> DASH
    API --> ATT
    API --> PAY
    API --> PERF
    API --> NOTIFY
    API --> AI

    DASH --> REDIS
    DASH --> PG
    ATT --> PG
    ATT --> REDIS
    PAY --> PG
    PERF --> PG
    NOTIFY --> PG
    NOTIFY --> WS
    AUTH --> REDIS
    AUTH --> PG
    AUTH --> AUDIT
    AI --> GRAPH
    GRAPH --> INDEX
    GRAPH --> OPENAI
    GRAPH --> LOCAL
    INDEX --> PG
    INDEX --> VEC
    AI --> REDIS
    API --> S3

    DOCKER --> API
    DOCKER --> WEB
    HELM --> K8S
    CI --> HELM
    CI --> DOCKER
```

## Runtime domains

### Auth

- Local JWT mode for direct development and seeded demo users
- OIDC/SSO launch hooks for enterprise federation
- MFA validation and role claim issuance

### Dashboard

- Consolidated monthly employee view
- Attendance, leave, holiday, and anomaly markers
- Cached employee month responses in Redis

### Attendance and leave

- Geofence-aware check-in
- Leave requests and approval paths
- Cache invalidation on write operations

### Notifications

- Tagged employee alerts for quick response
- Read acknowledgment APIs
- WebSocket push channel for live updates

### Assistant and RAG

- LangGraph state machine for classify → retrieve → answer → action
- pgvector-ready chunk storage
- OpenAI primary model with local-LLM fallback
- SSE streaming for frontend responses

## Deployment model

- Local: one FastAPI backend plus web app via Docker Compose
- Cloud: split web/backend deployments behind ingress with Redis/PostgreSQL/Mongo managed services
- Kubernetes packaging: Helm chart under [infra/helm/nexushr](D:\coledra-code\nexus-hr\infra\helm\nexushr)
