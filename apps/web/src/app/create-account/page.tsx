import Link from "next/link";

import { SignupWizard } from "@/components/auth/signup-wizard";

export default function CreateAccountPage() {
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
                <p className="text-sm text-slate-500">Enterprise HRMS launch workspace</p>
              </div>
            </div>

            <div className="flex flex-wrap gap-3">
              <Link className="button-secondary" href="/">
                Back to website
              </Link>
              <Link className="button-primary" href="/login">
                Sign in
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="shell pt-8 md:pt-10">
        <div className="mb-8 grid gap-6 lg:grid-cols-[1.05fr_0.95fr] lg:items-end">
          <div>
            <Link className="eyebrow" href="/">
              NexusHR launch flow
            </Link>
            <h1 className="mt-5 font-display text-4xl font-semibold text-slate-950 md:text-6xl">
              Create a branded HRMS workspace without skipping security, payroll, or policy design.
            </h1>
            <p className="mt-5 max-w-3xl text-lg leading-8 text-slate-600">
              Configure your company identity, rollout defaults, and security posture in one guided flow designed for
              enterprise HR and IT teams.
            </p>
          </div>

          <div className="panel px-6 py-6">
            <p className="text-xs uppercase tracking-[0.25em] text-slate-500">Launch expectations</p>
            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              {[
                ["Day 0", "Workspace ready"],
                ["3", "Launch steps"],
                ["100%", "Security-first setup"]
              ].map(([value, label]) => (
                <div className="rounded-[24px] border border-slate-200 bg-slate-50 px-4 py-4" key={label}>
                  <p className="font-display text-3xl font-semibold text-slate-950">{value}</p>
                  <p className="mt-2 text-xs uppercase tracking-[0.18em] text-slate-500">{label}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <SignupWizard />
      </section>
    </main>
  );
}
