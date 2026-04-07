import Link from "next/link";

import { SiteFooter } from "@/components/marketing/site-footer";
import { SiteHeader, type SiteNavLink } from "@/components/marketing/site-header";

const navigationLinks: SiteNavLink[] = [
  { label: "Products", href: "#products" },
  { label: "Platform", href: "#platform" },
  { label: "Security", href: "#security" },
  { label: "Customers", href: "#customers" },
  { label: "Launch", href: "#launch" }
];

const heroSignals = ["AI-native workflows", "Global payroll controls", "Employee-grade UX", "Audit-ready security"];

const trustMetrics = [
  ["40+", "People workflows modeled"],
  ["99.95%", "Platform uptime target"],
  ["100%", "Write actions audited"],
  ["4 roles", "Granular workforce access"]
] as const;

const logoCloud = ["FinServe Global", "Atlas Retail", "Northlight Health", "Meridian Logistics", "PulseTech"];

const operatingPillars = [
  {
    title: "One operating layer for HR, managers, and employees",
    detail:
      "Bring employee lifecycle, approvals, policies, attendance, payroll readiness, and performance into one coherent workspace.",
    stat: "1 shared system instead of siloed HR tools"
  },
  {
    title: "A website-to-product journey that feels intentional",
    detail:
      "The public brand, login flow, and employee dashboard all share one visual language so adoption begins before the first form is filled.",
    stat: "Shorter ramp-up from evaluation to usage"
  },
  {
    title: "Enterprise controls without an enterprise-heavy experience",
    detail:
      "Use RBAC, MFA, audit trails, tenancy, and compliance workflows without forcing employees through cluttered admin screens.",
    stat: "Cleaner UX with policy-grade controls"
  }
];

const modules = [
  {
    title: "Employee lifecycle",
    detail: "Offer letters, onboarding journeys, digital signing, document storage, org structures, and asset handovers."
  },
  {
    title: "Attendance and leave",
    detail: "Geofence-aware check-in, monthly attendance calendar, leave accruals, holidays, balances, and approvals."
  },
  {
    title: "Payroll and compliance",
    detail: "Dynamic payroll calculations, payslip generation, EPF, ESI, TDS readiness, and statutory reporting scaffolds."
  },
  {
    title: "Performance and feedback",
    detail: "OKRs, 360-degree reviews, sentiment overlays, manager prompts, and AI-supported review follow-through."
  }
];

const platformLayers = [
  {
    label: "Experience",
    title: "A public website, secure login, and employee workspace that feel like one product.",
    points: ["Next.js 16", "Tailwind CSS", "Responsive marketing and app surfaces"]
  },
  {
    label: "Services",
    title: "A FastAPI platform layer that unifies auth, people operations, attendance, payroll, and AI endpoints.",
    points: ["JWT and RBAC", "Redis caching", "Streaming assistant APIs"]
  },
  {
    label: "Operations",
    title: "Infrastructure built for scale, observability, and controlled delivery into cloud-native environments.",
    points: ["PostgreSQL and pgvector", "Mongo audit trail", "Helm and Kubernetes"]
  }
];

const implementationCards = [
  {
    title: "Security baseline",
    detail: "OpenID Connect, OAuth2, MFA, tenant-aware route protection, write auditing, and encrypted document storage patterns."
  },
  {
    title: "AI and workflow orchestration",
    detail: "LangGraph-driven assistant flows, RAG-ready retrieval, OpenAI-to-local fallback, and policy-aware response streaming."
  },
  {
    title: "Delivery readiness",
    detail: "Dockerized services, Compose startup, Helm deployment templates, CI workflows, and AWS or Azure-friendly packaging."
  }
];

export default function HomePage() {
  return (
    <>
      <SiteHeader
        links={navigationLinks}
        primaryAction={{ href: "/create-account", label: "Book a demo" }}
        secondaryAction={{ href: "/login", label: "Sign in" }}
      />

      <main className="overflow-hidden pb-6">
        <section className="shell relative pt-10 md:pt-14">
          <div className="hero-orb left-0 top-16 h-56 w-56 bg-sky-200/45" />
          <div className="hero-orb right-10 top-8 h-64 w-64 bg-emerald-100/60" />

          <div className="grid gap-8 xl:grid-cols-[1.02fr_0.98fr] xl:items-center">
            <div className="relative z-10 space-y-8">
              <div className="flex flex-wrap gap-3">
                <span className="eyebrow">Built for change-ready people operations</span>
                <span className="pill">HRMS website and product in one system</span>
              </div>

              <div className="space-y-6">
                <h1 className="max-w-4xl font-display text-5xl font-semibold tracking-tight text-slate-950 md:text-7xl">
                  The HR platform your brand, your HR team, and your employees can all believe in.
                </h1>
                <p className="max-w-3xl text-lg leading-8 text-slate-600 md:text-xl">
                  NexusHR gives you a real product website, polished login flows, and a modern HRMS workspace for
                  attendance, leave, payroll, compliance, and performance, all on one scalable stack.
                </p>
              </div>

              <div className="flex flex-wrap gap-4">
                <Link className="button-primary" href="/create-account">
                  Start a launch plan
                </Link>
                <Link className="button-secondary" href="/login">
                  Explore the live product
                </Link>
              </div>

              <div className="flex flex-wrap gap-2">
                {heroSignals.map((item) => (
                  <span className="pill" key={item}>
                    {item}
                  </span>
                ))}
              </div>

              <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                {trustMetrics.map(([value, label]) => (
                  <div className="metric-tile h-full" key={label}>
                    <p className="font-display text-3xl font-semibold text-slate-950">{value}</p>
                    <p className="mt-2 text-sm text-slate-500">{label}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="relative z-10">
              <div className="website-card-dark overflow-hidden px-6 py-6 md:px-8 md:py-8">
                <div className="flex flex-wrap items-start justify-between gap-4">
                  <div>
                    <p className="text-xs uppercase tracking-[0.28em] text-cyan-200">Unified workspace preview</p>
                    <h2 className="mt-3 font-display text-3xl font-semibold">
                      A website-quality product surface for people operations.
                    </h2>
                  </div>
                  <span className="rounded-full border border-white/15 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.18em] text-slate-200">
                    Live dashboard concept
                  </span>
                </div>

                <div className="mt-6 grid gap-4 lg:grid-cols-[1.05fr_0.95fr]">
                  <div className="rounded-[28px] border border-white/10 bg-white/5 p-5">
                    <div className="flex items-center justify-between gap-3">
                      <p className="text-sm font-semibold text-white">Attendance calendar</p>
                      <span className="text-xs uppercase tracking-[0.18em] text-slate-400">April 2026</span>
                    </div>

                    <div className="mt-4 grid grid-cols-7 gap-2 text-center text-[11px] text-slate-400">
                      {["M", "T", "W", "T", "F", "S", "S"].map((day) => (
                        <span key={day}>{day}</span>
                      ))}
                    </div>
                    <div className="mt-3 grid grid-cols-7 gap-2">
                      {[
                        "bg-cyan-300/75",
                        "bg-emerald-300/80",
                        "bg-white/10",
                        "bg-violet-300/75",
                        "bg-white/10",
                        "bg-white/5",
                        "bg-white/5",
                        "bg-emerald-300/80",
                        "bg-amber-300/80",
                        "bg-white/10",
                        "bg-cyan-300/75",
                        "bg-white/10",
                        "bg-rose-300/75",
                        "bg-white/5"
                      ].map((tone, index) => (
                        <div className={`h-10 rounded-2xl ${tone}`} key={index} />
                      ))}
                    </div>

                    <div className="mt-4 grid gap-2 text-xs text-slate-300">
                      <span>Present, leave, holidays, and anomalies in one monthly view</span>
                      <span>Tagged alerts prompt employees before payroll cut-off</span>
                    </div>
                  </div>

                  <div className="grid gap-4">
                    <div className="rounded-[28px] border border-white/10 bg-gradient-to-br from-cyan-500/20 to-sky-500/10 p-5">
                      <div className="flex items-center justify-between gap-3">
                        <p className="text-sm font-semibold text-white">People pulse</p>
                        <span className="text-xs uppercase tracking-[0.18em] text-cyan-100">Live metrics</span>
                      </div>
                      <div className="mt-4 grid gap-3 sm:grid-cols-2">
                        {[
                          ["97%", "Payroll readiness"],
                          ["12", "Attendance exceptions"],
                          ["18", "Unread alerts"],
                          ["0.78", "Review sentiment score"]
                        ].map(([value, label]) => (
                          <div className="rounded-[22px] border border-white/10 bg-white/5 px-4 py-4" key={label}>
                            <p className="font-display text-3xl font-semibold text-white">{value}</p>
                            <p className="mt-2 text-xs uppercase tracking-[0.18em] text-slate-300">{label}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="rounded-[28px] border border-white/10 bg-white p-5 text-slate-900">
                      <p className="text-sm font-semibold text-slate-500">NexusHR Copilot</p>
                      <p className="mt-3 font-display text-2xl font-semibold text-slate-950">
                        &quot;What should I prioritize this month?&quot;
                      </p>
                      <p className="mt-3 text-sm leading-7 text-slate-600">
                        Review the March 19 missed check-in, clear the pending wellbeing leave request, and confirm the
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
        </section>

        <section className="shell pt-12 md:pt-16" id="customers">
          <div className="panel px-6 py-7 md:px-8">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.28em] text-slate-500">Positioning and trust</p>
                <p className="mt-2 max-w-2xl text-sm leading-7 text-slate-600 md:text-base">
                  A real website needs trust signals, not just product cards. NexusHR leads with operational clarity,
                  visual consistency, and a path from buyer evaluation into employee usage.
                </p>
              </div>
              <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
                {logoCloud.map((logo) => (
                  <div className="metric-tile flex min-h-[92px] items-center justify-center text-center" key={logo}>
                    <span className="text-sm font-semibold text-slate-700">{logo}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="shell pt-16 md:pt-20" id="products">
          <div className="grid gap-10 xl:grid-cols-[0.9fr_1.1fr] xl:items-start">
            <div className="space-y-6">
              <span className="eyebrow">Why the website now feels aligned</span>
              <h2 className="section-title">Structured like a product website, not like disconnected app panels.</h2>
              <p className="section-copy">
                The public experience now follows a clearer arc: promise, proof, modules, platform, security, and
                implementation. That structure makes the page scan more like a real SaaS site and less like a feature dump.
              </p>
              <div className="grid gap-4">
                {operatingPillars.map((item) => (
                  <article className="website-card h-full px-6 py-6" key={item.title}>
                    <p className="text-xs uppercase tracking-[0.22em] text-slate-500">Outcome</p>
                    <h3 className="mt-3 font-display text-2xl font-semibold text-slate-950">{item.title}</h3>
                    <p className="mt-3 text-sm leading-7 text-slate-600">{item.detail}</p>
                    <p className="mt-4 text-sm font-semibold text-sky-700">{item.stat}</p>
                  </article>
                ))}
              </div>
            </div>

            <div className="grid auto-rows-fr gap-5 md:grid-cols-2">
              {modules.map((module, index) => (
                <article className="website-card flex h-full flex-col px-6 py-6" key={module.title}>
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
            <div className="max-w-3xl">
              <span className="eyebrow">Platform story</span>
              <h2 className="mt-6 section-title">
                Designed to scale like a modern software platform, not a legacy HR portal.
              </h2>
              <p className="mt-4 section-copy">
                The frontend is product-grade Next.js with Tailwind, and the backend is a FastAPI platform with
                tenant-aware auth, caching, RAG-ready services, audit capture, and cloud-native deployment scaffolding.
              </p>
            </div>

            <div className="mt-8 grid gap-4 xl:grid-cols-3">
              {platformLayers.map((layer) => (
                <div className="website-card h-full px-6 py-6" key={layer.title}>
                  <span className="eyebrow">{layer.label}</span>
                  <h3 className="mt-5 font-display text-2xl font-semibold text-slate-950">{layer.title}</h3>
                  <div className="mt-5 grid gap-3">
                    {layer.points.map((point) => (
                      <div className="rounded-[22px] border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600" key={point}>
                        {point}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="shell pt-16 md:pt-20" id="security">
          <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
            <div className="website-card-dark px-6 py-8 md:px-8">
              <span className="eyebrow border-white/10 bg-white/5 text-white">Security and compliance</span>
              <h2 className="mt-6 font-display text-4xl font-semibold text-white md:text-5xl">
                Enterprise controls built in from day one.
              </h2>
              <p className="mt-4 max-w-2xl text-sm leading-8 text-slate-300 md:text-base">
                Identity, auditability, GDPR controls, and ISO 27001-aligned operational patterns are part of the
                platform design, not an afterthought added after launch.
              </p>

              <div className="mt-8 grid gap-4 md:grid-cols-2">
                {[
                  "OpenID Connect and OAuth2 with MFA",
                  "Role and department scoped access",
                  "Every write action logged to audit storage",
                  "Encrypted document storage and governance-ready patterns"
                ].map((item) => (
                  <div className="rounded-[24px] border border-white/10 bg-white/5 px-5 py-4 text-sm leading-7 text-slate-200" key={item}>
                    {item}
                  </div>
                ))}
              </div>
            </div>

            <div className="grid auto-rows-fr gap-4" id="launch">
              {implementationCards.map((item) => (
                <article className="website-card h-full px-6 py-6" key={item.title}>
                  <p className="text-xs uppercase tracking-[0.22em] text-slate-500">Launch readiness</p>
                  <h3 className="mt-3 font-display text-2xl font-semibold text-slate-950">{item.title}</h3>
                  <p className="mt-3 text-sm leading-7 text-slate-600">{item.detail}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="shell pt-16 md:pt-20">
          <div className="website-card overflow-hidden px-6 py-8 md:px-8 md:py-10">
            <div className="grid gap-8 xl:grid-cols-[1.08fr_0.92fr] xl:items-center">
              <div>
                <span className="eyebrow">Ready to open the product</span>
                <h2 className="mt-6 section-title">
                  Move from website to workspace without losing the product narrative.
                </h2>
                <p className="mt-4 section-copy">
                  That is what makes NexusHR feel like a website-backed product instead of a standalone admin tool:
                  every public and private touchpoint belongs to the same system.
                </p>
              </div>

              <div className="flex flex-wrap gap-4 xl:justify-end">
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

      <SiteFooter />
    </>
  );
}
