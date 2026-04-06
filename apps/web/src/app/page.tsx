import Link from "next/link";

const modules = [
  {
    title: "Employee Lifecycle",
    description:
      "Digital onboarding, contract workflows, asset allocation, and offboarding orchestration in one people graph.",
    stats: "eSign, documents, assets, lifecycle events"
  },
  {
    title: "Attendance & Leave",
    description:
      "Geofence-enabled check-ins, shift controls, automated accruals, and multi-level approvals tuned for distributed teams.",
    stats: "Live clocks, balances, policies, escalation rules"
  },
  {
    title: "Payroll & Compliance",
    description:
      "Dynamic pay rules, EPF/ESI/TDS reporting, reconciliations, and payslip delivery without spreadsheet debt.",
    stats: "Payroll runs, tax adapters, statutory exports"
  },
  {
    title: "Performance Intelligence",
    description:
      "OKR alignment, 360 feedback, calibration cycles, and AI sentiment overlays on review narratives.",
    stats: "OKRs, feedback loops, sentiment scoring"
  }
];

const platformPillars = [
  "OpenID Connect / OAuth2",
  "MFA and device trust",
  "Department and team RBAC",
  "FastAPI microservices",
  "PostgreSQL + Redis + MongoDB",
  "Kubernetes and encrypted S3 storage"
];

const personas = [
  {
    name: "Super Admin",
    scope: "Global governance",
    description: "Owns tenant configuration, compliance controls, and cross-region reporting."
  },
  {
    name: "HR Manager",
    scope: "Department-specific",
    description: "Manages people operations, policies, hiring pipelines, and payroll review for assigned units."
  },
  {
    name: "Manager",
    scope: "Team-specific",
    description: "Approves leave, reviews goals, monitors attendance exceptions, and closes reviews."
  },
  {
    name: "Employee",
    scope: "Self-service",
    description: "Updates personal records, clocks in, submits leave, views payslips, and tracks OKRs."
  }
];

export default function HomePage() {
  return (
    <main className="overflow-hidden pb-24">
      <section className="shell pt-6 md:pt-10">
        <div className="panel px-5 py-4 md:px-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-950 font-display text-xl font-bold text-white">
                N
              </div>
              <div>
                <p className="font-display text-xl font-semibold text-slate-950">NexusHR</p>
                <p className="text-sm text-slate-500">
                  The operating system for secure, modern people teams.
                </p>
              </div>
            </div>
            <div className="flex flex-wrap gap-3">
              <Link className="button-secondary" href="#architecture">
                Explore architecture
              </Link>
              <Link className="button-primary" href="/login">
                Launch workspace
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="shell relative pt-12 md:pt-20">
        <div className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="space-y-8">
            <span className="eyebrow">AI-ready HR command center</span>
            <div className="space-y-6">
              <h1 className="font-display text-5xl font-semibold tracking-tight text-slate-950 md:text-7xl">
                Orchestrate every people workflow from candidate welcome to compliant exit.
              </h1>
              <p className="max-w-2xl text-lg leading-8 text-slate-600 md:text-xl">
                NexusHR brings employee lifecycle, attendance, payroll, compliance, and performance into one
                branded platform designed for scale, control, and modern HR operations.
              </p>
            </div>
            <div className="flex flex-wrap gap-4">
              <Link className="button-primary" href="/create-account">
                Create workspace
              </Link>
              <Link className="button-secondary" href="/login">
                Experience the login flow
              </Link>
            </div>
            <div className="grid gap-4 md:grid-cols-3">
              {[
                ["99.95%", "Target uptime"],
                ["4 roles", "Granular RBAC personas"],
                ["100%", "Write actions audit logged"]
              ].map(([value, label]) => (
                <div className="panel px-5 py-5" key={label}>
                  <p className="font-display text-3xl font-semibold text-slate-950">{value}</p>
                  <p className="mt-2 text-sm text-slate-500">{label}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="panel relative overflow-hidden bg-slate-950 px-6 py-6 text-white">
            <div className="absolute inset-x-8 top-0 h-px bg-gradient-to-r from-transparent via-white/70 to-transparent" />
            <div className="grid gap-5">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.25em] text-teal-200">Operations cockpit</p>
                  <h2 className="mt-2 font-display text-3xl font-semibold">People pulse</h2>
                </div>
                <div className="rounded-full border border-white/20 px-4 py-2 text-xs text-slate-300">
                  India payroll cycle live
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <div className="rounded-[24px] border border-white/10 bg-white/5 p-5">
                  <p className="text-sm text-slate-300">Attendance anomalies</p>
                  <p className="mt-3 font-display text-4xl font-semibold">12</p>
                  <p className="mt-2 text-sm text-teal-200">4 geofence exceptions auto-routed</p>
                </div>
                <div className="rounded-[24px] border border-white/10 bg-gradient-to-br from-teal-500/30 to-sky-500/10 p-5">
                  <p className="text-sm text-slate-200">Payroll readiness</p>
                  <p className="mt-3 font-display text-4xl font-semibold">97%</p>
                  <p className="mt-2 text-sm text-slate-300">Only compliance attestations pending</p>
                </div>
              </div>

              <div className="rounded-[28px] border border-white/10 bg-white/5 p-5">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <p className="text-sm text-slate-300">Review cycle sentiment</p>
                    <p className="mt-1 font-display text-2xl font-semibold">Healthy, but manager coaching needed in Support</p>
                  </div>
                  <span className="pill border-white/10 bg-white/10 text-white">AI signal enabled</span>
                </div>
                <div className="mt-5 grid gap-3">
                  {[
                    ["Onboarding packs signed", "93%"],
                    ["Leave approvals within SLA", "88%"],
                    ["Assets returned before exit", "96%"]
                  ].map(([label, value]) => (
                    <div className="flex items-center gap-4" key={label}>
                      <p className="w-40 shrink-0 text-sm text-slate-300">{label}</p>
                      <div className="h-3 flex-1 rounded-full bg-white/10">
                        <div className="h-3 rounded-full bg-gradient-to-r from-teal-300 to-sky-300" style={{ width: value }} />
                      </div>
                      <span className="text-sm font-semibold text-white">{value}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid gap-3 md:grid-cols-3">
                {["GDPR aware", "ISO 27001 aligned", "S3 encrypted"].map((item) => (
                  <div key={item} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200">
                    {item}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="shell pt-20">
        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
          {modules.map((module) => (
            <article className="panel h-full px-6 py-6" key={module.title}>
              <span className="pill">{module.title}</span>
              <h3 className="mt-5 font-display text-2xl font-semibold text-slate-950">{module.title}</h3>
              <p className="mt-3 text-sm leading-7 text-slate-600">{module.description}</p>
              <p className="mt-5 text-sm font-semibold text-teal-700">{module.stats}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="shell pt-20" id="architecture">
        <div className="grid gap-8 lg:grid-cols-[0.88fr_1.12fr]">
          <div className="space-y-6">
            <span className="eyebrow">Security architecture</span>
            <h2 className="section-title">Built for policy-heavy, high-growth HR teams.</h2>
            <p className="muted">
              The platform layers a Next.js experience on top of FastAPI services, with PostgreSQL for core HR
              records, Redis for performance-sensitive state, MongoDB for audit trails, and encrypted object storage
              for documents.
            </p>
            <div className="flex flex-wrap gap-3">
              {platformPillars.map((pillar) => (
                <span className="pill" key={pillar}>
                  {pillar}
                </span>
              ))}
            </div>
          </div>

          <div className="panel px-6 py-6">
            <div className="grid gap-4 md:grid-cols-2">
              {personas.map((persona) => (
                <div key={persona.name} className="rounded-[24px] border border-slate-200 bg-slate-50 px-5 py-5">
                  <p className="text-xs uppercase tracking-[0.2em] text-slate-500">{persona.scope}</p>
                  <h3 className="mt-3 font-display text-2xl font-semibold text-slate-950">{persona.name}</h3>
                  <p className="mt-2 text-sm leading-7 text-slate-600">{persona.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="shell pt-20">
        <div className="panel px-6 py-8 md:px-10">
          <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
            <div>
              <span className="eyebrow">Deployment ready</span>
              <h2 className="mt-6 section-title">Launch a brand site today. Scale into a multi-service HR platform tomorrow.</h2>
            </div>
            <div className="grid gap-4 text-sm leading-7 text-slate-600 md:grid-cols-2">
              <p>
                Run the web app on a single domain for marketing and auth, then route API traffic through Kubernetes
                ingress to isolate payroll, attendance, performance, and audit workloads independently.
              </p>
              <p>
                The scaffold includes Docker and Kubernetes manifests, OpenAPI-native FastAPI services, and a shared
                auth layer that keeps RBAC and audit logic consistent across the platform.
              </p>
            </div>
          </div>
          <div className="mt-8 flex flex-wrap gap-4">
            <Link className="button-primary" href="/create-account">
              Book an HR architecture walkthrough
            </Link>
            <Link className="button-secondary" href="/login">
              Explore advanced login
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}

