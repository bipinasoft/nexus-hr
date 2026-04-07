import Link from "next/link";

import { LoginSwitcher } from "@/components/auth/login-switcher";

const spotlightItems = [
  "Monthly attendance calendar with leave and holiday markers",
  "Alerts and notifications tagged by employee action",
  "Streaming HR copilot with policy-aware answers",
  "Enterprise security with JWT, RBAC, MFA, and SSO hooks"
];

export default function LoginPage() {
  return (
    <main className="overflow-hidden py-8 md:py-12">
      <section className="shell">
        <div className="panel px-5 py-4 md:px-7">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-center gap-4">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-950 font-display text-lg font-bold text-white">
                N
              </div>
              <div>
                <p className="font-display text-xl font-semibold text-slate-950">NexusHR</p>
                <p className="text-sm text-slate-500">Product-led enterprise HRMS</p>
              </div>
            </div>

            <div className="flex flex-wrap gap-3">
              <Link className="button-secondary" href="/">
                Back to website
              </Link>
              <Link className="button-primary" href="/create-account">
                Create workspace
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="shell relative pt-8 md:pt-10">
        <div className="hero-orb left-0 top-12 h-48 w-48 bg-sky-200/50" />
        <div className="hero-orb right-10 top-20 h-52 w-52 bg-emerald-100/60" />

        <div className="grid gap-8 lg:grid-cols-[0.95fr_1.05fr] lg:items-start">
          <div className="relative z-10 space-y-7">
            <div className="space-y-5">
              <span className="eyebrow">Secure product access</span>
              <h1 className="font-display text-5xl font-semibold tracking-tight text-slate-950 md:text-6xl">
                Enter the NexusHR workspace through a product-grade sign-in experience.
              </h1>
              <p className="max-w-2xl text-lg leading-8 text-slate-600">
                This login flow is designed to feel like part of the product journey, with enterprise trust signals,
                guided identity options, and a clear preview of what employees unlock after authentication.
              </p>
            </div>

            <div className="grid gap-4">
              {spotlightItems.map((item, index) => (
                <div className="soft-card px-5 py-4" key={item}>
                  <div className="flex items-start gap-4">
                    <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-slate-950 font-display text-sm font-semibold text-white">
                      0{index + 1}
                    </span>
                    <p className="text-sm leading-7 text-slate-600">{item}</p>
                  </div>
                </div>
              ))}
            </div>

            <div className="panel-dark px-6 py-6">
              <p className="text-xs uppercase tracking-[0.28em] text-cyan-200">Inside the product</p>
              <div className="mt-5 grid gap-4 sm:grid-cols-3">
                {[
                  ["12", "Attendance exceptions surfaced"],
                  ["3", "Employee notifications waiting"],
                  ["97%", "Payroll readiness coverage"]
                ].map(([value, label]) => (
                  <div className="rounded-[24px] border border-white/10 bg-white/5 px-4 py-4" key={label}>
                    <p className="font-display text-3xl font-semibold text-white">{value}</p>
                    <p className="mt-2 text-xs uppercase tracking-[0.18em] text-slate-300">{label}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="relative z-10">
            <LoginSwitcher />
          </div>
        </div>
      </section>
    </main>
  );
}
