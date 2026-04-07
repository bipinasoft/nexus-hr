import Link from "next/link";

const navigationLinks = [
  { label: "Products", href: "#products" },
  { label: "Platform", href: "#platform" },
  { label: "Security", href: "#security" },
  { label: "Customers", href: "#customers" },
  { label: "Launch", href: "#launch" }
];

const enterpriseSignals = [
  "AI-native workflows",
  "Global payroll controls",
  "Employee-grade UX",
  "Audit-ready security"
];

const productRows = [
  {
    title: "Core HR That Feels Consumer-Grade",
    description:
      "Design one home for employee lifecycle, documents, approvals, policies, and assets without sacrificing enterprise control.",
    stat: "93% onboarding completion in the first week"
  },
  {
    title: "Attendance, Leave, and Payroll in One Rhythm",
    description:
      "Move from fragmented operational tooling to a single rhythm across check-ins, balances, approvals, payroll readiness, and statutory reporting.",
    stat: "4x faster exception resolution across teams"
  },
  {
    title: "Performance and AI Copilots Built In",
    description:
      "Bring OKRs, 360 feedback, review intelligence, and AI support into the same experience employees already use every day.",
    stat: "1 workspace for HR, managers, and employees"
  }
];

const modules = [
  {
    title: "Employee Lifecycle",
    detail: "Offer letters, onboarding journeys, digital signing, org structures, and asset movements in one system."
  },
  {
    title: "Attendance & Leave",
    detail: "Monthly calendars, geofence-aware check-ins, policy accruals, holidays, and approval workflows."
  },
  {
    title: "Payroll & Compliance",
    detail: "Dynamic calculations, payslips, EPF/ESI/TDS controls, and compliance-ready reporting."
  },
  {
    title: "Performance Management",
    detail: "OKRs, feedback cycles, sentiment overlays, and review orchestration for managers and teams."
  }
];

const trustMetrics = [
  ["40+", "People workflows modeled"],
  ["99.95%", "Platform uptime target"],
  ["100%", "Write actions audited"],
  ["4 roles", "Granular workforce access"]
];

const platformLayers = [
  {
    label: "Experience",
    title: "Product-led website, login, and employee workspace",
    points: ["Modern marketing site", "Product-style authentication", "Employee dashboard and alerts"]
  },
  {
    label: "Platform",
    title: "FastAPI backbone with real-time services",
    points: ["JWT + RBAC + SSO hooks", "Streaming assistant APIs", "Redis + WebSocket updates"]
  },
  {
    label: "Data",
    title: "Operational and AI infrastructure for scale",
    points: ["PostgreSQL + pgvector", "Mongo audit trails", "Kubernetes and Helm delivery"]
  }
];

export default function HomePage() {
  return (
    <main className="overflow-hidden pb-24">
      <section className="shell pt-6 md:pt-8">
        <div className="panel px-5 py-4 md:px-7">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-950 font-display text-xl font-bold text-white">
                N
              </div>
              <div>
                <p className="font-display text-xl font-semibold text-slate-950">NexusHR</p>
                <p className="text-sm text-slate-500">Enterprise HRMS for change-ready teams.</p>
              </div>
            </div>

            <nav className="flex flex-wrap items-center gap-5">
              {navigationLinks.map((item) => (
                <a className="nav-link" href={item.href} key={item.label}>
                  {item.label}
                </a>
              ))}
            </nav>

            <div className="flex flex-wrap gap-3">
              <Link className="button-secondary" href="/login">
                Sign in
              </Link>
              <Link className="button-primary" href="/create-account">
                Book a demo
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="shell relative pt-10 md:pt-16">
        <div className="hero-orb left-0 top-12 h-44 w-44 bg-sky-200/50" />
        <div className="hero-orb right-10 top-8 h-52 w-52 bg-emerald-100/60" />

        <div className="grid gap-8 lg:grid-cols-[1.02fr_0.98fr] lg:items-center">
          <div className="relative z-10 space-y-8">
            <div className="flex flex-wrap gap-3">
              <span className="eyebrow">Built To Make Enterprises Change-Ready</span>
              <span className="pill">AI-native HR platform</span>
            </div>

            <div className="space-y-6">
              <h1 className="max-w-4xl font-display text-5xl font-semibold tracking-tight text-slate-950 md:text-7xl">
                A new-age HR platform for global teams, operations leaders, and every employee.
              </h1>
              <p className="max-w-3xl text-lg leading-8 text-slate-600 md:text-xl">
                NexusHR turns the HRMS into a product experience: polished website, secure product-style login,
                interactive employee dashboards, and one platform for attendance, payroll, compliance, and performance.
              </p>
            </div>

            <div className="flex flex-wrap gap-4">
              <Link className="button-primary" href="/create-account">
                Schedule a walkthrough
              </Link>
              <Link className="button-secondary" href="/login">
                Explore the live product
              </Link>
            </div>

            <div className="flex flex-wrap gap-2">
              {enterpriseSignals.map((item) => (
                <span className="pill" key={item}>
                  {item}
                </span>
              ))}
            </div>
          </div>

          <div className="relative">
            <div className="soft-card relative overflow-hidden border-slate-200/80 bg-slate-950 px-6 py-6 text-white md:px-8 md:py-8">
              <div className="absolute inset-x-8 top-0 h-px bg-gradient-to-r from-transparent via-white/50 to-transparent" />
              <div className="grid gap-5">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <p className="text-xs uppercase tracking-[0.28em] text-cyan-200">Unified workspace</p>
                    <h2 className="mt-2 font-display text-3xl font-semibold">One HR operating layer</h2>
                  </div>
                  <span className="rounded-full border border-white/15 bg-white/5 px-4 py-2 text-xs text-slate-300">
                    Live dashboard preview
                  </span>
                </div>

                <div className="grid gap-4 md:grid-cols-[0.95fr_1.05fr]">
                  <div className="rounded-[28px] border border-white/10 bg-white/5 p-5">
                    <p className="text-sm text-slate-300">Monthly attendance calendar</p>
                    <div className="mt-4 grid grid-cols-7 gap-2 text-center text-[11px] text-slate-400">
                      {["M", "T", "W", "T", "F", "S", "S"].map((day) => (
                        <span key={day}>{day}</span>
                      ))}
                    </div>
                    <div className="mt-3 grid grid-cols-7 gap-2">
                      {[
                        "bg-cyan-300/70",
                        "bg-emerald-300/80",
                        "bg-white/10",
                        "bg-violet-300/70",
                        "bg-white/10",
                        "bg-white/5",
                        "bg-white/5",
                        "bg-emerald-300/80",
                        "bg-amber-300/80",
                        "bg-white/10",
                        "bg-cyan-300/70",
                        "bg-white/10",
                        "bg-rose-300/80",
                        "bg-white/5"
                      ].map((tone, index) => (
                        <div className={`h-9 rounded-xl ${tone}`} key={index} />
                      ))}
                    </div>
                    <div className="mt-4 grid gap-2 text-xs text-slate-300">
                      <span>Present, leave, holidays, and anomalies in a single month view</span>
                      <span>Tag-driven alerts for employee action</span>
                    </div>
                  </div>

                  <div className="grid gap-4">
                    <div className="rounded-[28px] border border-white/10 bg-gradient-to-br from-cyan-500/20 to-sky-500/10 p-5">
                      <p className="text-sm text-cyan-100">People pulse</p>
                      <div className="mt-4 grid gap-3 sm:grid-cols-2">
                        {[
                          ["97%", "Payroll readiness"],
                          ["12", "Attendance exceptions"],
                          ["18", "Unread alerts"],
                          ["0.78", "Review sentiment score"]
                        ].map(([value, label]) => (
                          <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-4" key={label}>
                            <p className="font-display text-3xl font-semibold text-white">{value}</p>
                            <p className="mt-2 text-xs uppercase tracking-[0.18em] text-slate-300">{label}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="rounded-[28px] border border-white/10 bg-white p-5 text-slate-900">
                      <p className="text-sm font-semibold text-slate-500">NexusHR Copilot</p>
                      <p className="mt-3 font-display text-2xl font-semibold text-slate-950">
                        “What should I prioritize this month?”
                      </p>
                      <p className="mt-3 text-sm leading-7 text-slate-600">
                        Review the March 19 missed check-in, clear one pending wellbeing leave request, and confirm
                        payroll cut-off before the 25th.
                      </p>
                      <div className="mt-4 flex flex-wrap gap-2">
                        {["OpenAI fallback", "Local LLM support", "Streaming responses"].map((item) => (
                          <span className="pill" key={item}>
                            {item}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="shell pt-12 md:pt-16" id="customers">
        <div className="panel px-6 py-6 md:px-8">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">Trusted product language</p>
              <p className="mt-2 max-w-2xl text-sm leading-7 text-slate-600 md:text-base">
                Built with the visual confidence of a modern enterprise software website: product storytelling,
                trust metrics, polished auth, and a clear path into the live experience.
              </p>
            </div>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              {trustMetrics.map(([value, label]) => (
                <div className="metric-tile min-w-[150px]" key={label}>
                  <p className="font-display text-3xl font-semibold text-slate-950">{value}</p>
                  <p className="mt-2 text-sm text-slate-500">{label}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="shell pt-16 md:pt-20" id="products">
        <div className="grid gap-12 lg:grid-cols-[0.82fr_1.18fr]">
          <div className="space-y-6">
            <span className="eyebrow">Why teams switch</span>
            <h2 className="section-title">The HRMS should feel like a product, not a collection of admin screens.</h2>
            <p className="section-copy">
              NexusHR is designed to look and behave like the front door to a workforce platform. Marketing pages,
              authentication, employee dashboards, and HR operations all share one visual language and one modern stack.
            </p>
            <div className="grid gap-4">
              {productRows.map((row) => (
                <div className="soft-card px-5 py-5" key={row.title}>
                  <p className="text-xs uppercase tracking-[0.22em] text-slate-500">Outcome</p>
                  <h3 className="mt-3 font-display text-2xl font-semibold text-slate-950">{row.title}</h3>
                  <p className="mt-3 text-sm leading-7 text-slate-600">{row.description}</p>
                  <p className="mt-4 text-sm font-semibold text-sky-700">{row.stat}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="grid gap-5 md:grid-cols-2">
            {modules.map((module, index) => (
              <article className="soft-card h-full px-6 py-6" key={module.title}>
                <div className="flex items-center justify-between gap-3">
                  <span className="pill">0{index + 1}</span>
                  <span className="text-xs uppercase tracking-[0.22em] text-slate-400">Product module</span>
                </div>
                <h3 className="mt-6 font-display text-2xl font-semibold text-slate-950">{module.title}</h3>
                <p className="mt-3 text-sm leading-7 text-slate-600">{module.detail}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="shell pt-16 md:pt-20" id="platform">
        <div className="panel px-6 py-8 md:px-8 md:py-10">
          <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:items-start">
            <div>
              <span className="eyebrow">Platform architecture</span>
              <h2 className="mt-6 section-title">Designed like a modern software company would ship an HR platform.</h2>
              <p className="mt-4 section-copy">
                The frontend is product-grade Next.js with Tailwind, and the backend is a scalable FastAPI platform
                with JWT auth, Redis caching, pgvector indexing, audit trails, and Kubernetes delivery.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                {[
                  "Next.js + Tailwind CSS",
                  "FastAPI + OpenAPI",
                  "PostgreSQL + Redis + MongoDB",
                  "Helm + Kubernetes",
                  "RBAC + JWT + SSO",
                  "LangGraph + RAG"
                ].map((item) => (
                  <span className="pill" key={item}>
                    {item}
                  </span>
                ))}
              </div>
            </div>

            <div className="grid gap-4">
              {platformLayers.map((layer) => (
                <div className="soft-card px-6 py-6" key={layer.title}>
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <span className="eyebrow">{layer.label}</span>
                    <span className="text-xs uppercase tracking-[0.22em] text-slate-400">NexusHR stack</span>
                  </div>
                  <h3 className="mt-5 font-display text-2xl font-semibold text-slate-950">{layer.title}</h3>
                  <div className="mt-4 grid gap-3 md:grid-cols-3">
                    {layer.points.map((point) => (
                      <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600" key={point}>
                        {point}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="shell pt-16 md:pt-20" id="security">
        <div className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
          <div className="panel-dark px-6 py-8 md:px-8">
            <span className="eyebrow border-white/10 bg-white/5 text-white">Security and compliance</span>
            <h2 className="mt-6 font-display text-4xl font-semibold text-white md:text-5xl">
              Secure by default. Productive by design.
            </h2>
            <p className="mt-4 max-w-2xl text-sm leading-8 text-slate-300 md:text-base">
              Identity, auditability, GDPR controls, and ISO 27001-aligned patterns are built into the experience,
              not bolted on after launch.
            </p>
            <div className="mt-8 grid gap-4 md:grid-cols-2">
              {[
                "OpenID Connect / OAuth2 with MFA",
                "Role and department scoped access",
                "Every write action logged to audit storage",
                "Encrypted document storage and API-ready governance"
              ].map((item) => (
                <div className="rounded-[24px] border border-white/10 bg-white/5 px-5 py-4 text-sm leading-7 text-slate-200" key={item}>
                  {item}
                </div>
              ))}
            </div>
          </div>

          <div className="panel px-6 py-8 md:px-8" id="launch">
            <span className="eyebrow">Go from website to product in minutes</span>
            <h2 className="mt-6 section-title">The same design system powers the public brand and the logged-in HR experience.</h2>
            <p className="mt-4 section-copy">
              That means sharper first impressions, better adoption after login, and less friction between marketing,
              identity, and day-to-day employee workflows.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link className="button-primary" href="/login">
                View the login experience
              </Link>
              <Link className="button-secondary" href="/dashboard">
                Jump to dashboard
              </Link>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
