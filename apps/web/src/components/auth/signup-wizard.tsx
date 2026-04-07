"use client";

import { useState } from "react";

const steps = [
  {
    id: "workspace",
    title: "Workspace",
    description: "Set up your brand, legal entity, and initial admin account."
  },
  {
    id: "policies",
    title: "Policies",
    description: "Choose attendance, leave, and payroll defaults for launch."
  },
  {
    id: "security",
    title: "Security",
    description: "Enable MFA, document retention, and region-aware data controls."
  }
] as const;

export function SignupWizard() {
  const [step, setStep] = useState(0);

  return (
    <div className="grid gap-6 lg:grid-cols-[1.02fr_0.98fr]">
      <div className="panel px-6 py-6 md:px-8">
        <div className="flex flex-wrap gap-3">
          {steps.map((item, index) => {
            const active = index === step;

            return (
              <button
                className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
                  active ? "bg-slate-950 text-white" : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`}
                key={item.id}
                onClick={() => setStep(index)}
                type="button"
              >
                {index + 1}. {item.title}
              </button>
            );
          })}
        </div>

        <div className="mt-6">
          <p className="text-sm uppercase tracking-[0.25em] text-slate-500">Step {step + 1}</p>
          <h2 className="mt-2 font-display text-3xl font-semibold text-slate-950">{steps[step].title}</h2>
          <p className="mt-2 text-sm leading-7 text-slate-600">{steps[step].description}</p>
        </div>

        {step === 0 ? (
          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <div className="md:col-span-2">
              <label className="mb-2 block text-sm font-medium text-slate-700">Company name</label>
              <input className="field" placeholder="NexusHR Labs Pvt. Ltd." type="text" />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Primary domain</label>
              <input className="field" placeholder="app.nexushr.com" type="text" />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Employee count</label>
              <select className="field" defaultValue="201-1000">
                <option>1-50</option>
                <option>51-200</option>
                <option>201-1000</option>
                <option>1000+</option>
              </select>
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Admin work email</label>
              <input className="field" placeholder="hr.lead@company.com" type="email" />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Operating region</label>
              <select className="field" defaultValue="India">
                <option>India</option>
                <option>United Kingdom</option>
                <option>European Union</option>
                <option>Middle East</option>
              </select>
            </div>
          </div>
        ) : null}

        {step === 1 ? (
          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Attendance mode</label>
              <select className="field" defaultValue="Hybrid with geofencing">
                <option>Hybrid with geofencing</option>
                <option>Office-only</option>
                <option>Remote-first</option>
              </select>
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Leave accrual cadence</label>
              <select className="field" defaultValue="Monthly">
                <option>Monthly</option>
                <option>Quarterly</option>
                <option>Annually</option>
              </select>
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Payroll cycle</label>
              <select className="field" defaultValue="Monthly">
                <option>Monthly</option>
                <option>Semi-monthly</option>
                <option>Bi-weekly</option>
              </select>
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Statutory bundle</label>
              <select className="field" defaultValue="EPF / ESI / TDS">
                <option>EPF / ESI / TDS</option>
                <option>Custom compliance package</option>
                <option>Global payroll starter</option>
              </select>
            </div>
            <div className="md:col-span-2">
              <label className="mb-2 block text-sm font-medium text-slate-700">Approval policy</label>
              <textarea
                className="field min-h-32 resize-none"
                placeholder="Example: Leave requests route to manager, then HR Manager for balances over 5 days."
              />
            </div>
          </div>
        ) : null}

        {step === 2 ? (
          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <label className="rounded-[24px] border border-slate-200 bg-slate-50 px-5 py-4">
              <p className="font-semibold text-slate-900">Enforce MFA for all users</p>
              <p className="mt-2 text-sm leading-7 text-slate-600">
                Require app-based MFA, with OTP fallback for workforce continuity.
              </p>
            </label>
            <label className="rounded-[24px] border border-slate-200 bg-slate-50 px-5 py-4">
              <p className="font-semibold text-slate-900">Enable document encryption</p>
              <p className="mt-2 text-sm leading-7 text-slate-600">
                Store employee letters, IDs, and policies with encrypted object storage.
              </p>
            </label>
            <label className="rounded-[24px] border border-slate-200 bg-slate-50 px-5 py-4">
              <p className="font-semibold text-slate-900">Activate audit retention</p>
              <p className="mt-2 text-sm leading-7 text-slate-600">
                Capture write events with user ID, IP address, service, and response status.
              </p>
            </label>
            <label className="rounded-[24px] border border-slate-200 bg-slate-50 px-5 py-4">
              <p className="font-semibold text-slate-900">Region-specific data controls</p>
              <p className="mt-2 text-sm leading-7 text-slate-600">
                Apply GDPR-aware retention and deletion workflows by entity or geography.
              </p>
            </label>
          </div>
        ) : null}

        <div className="mt-8 flex flex-wrap justify-between gap-3">
          <button
            className="button-secondary"
            disabled={step === 0}
            onClick={() => setStep((current) => Math.max(0, current - 1))}
            type="button"
          >
            Previous
          </button>
          <button
            className="button-primary"
            onClick={() => setStep((current) => Math.min(steps.length - 1, current + 1))}
            type="button"
          >
            {step === steps.length - 1 ? "Review launch checklist" : "Continue"}
          </button>
        </div>
      </div>

      <aside className="panel-dark px-6 py-6 md:px-8">
        <p className="text-xs uppercase tracking-[0.25em] text-cyan-200">Launch blueprint</p>
        <h2 className="mt-4 font-display text-3xl font-semibold">A workspace creation flow built for enterprise HR teams.</h2>
        <div className="mt-6 space-y-4">
          {[
            "Connect your brand domain and define the legal entity powering payroll and contracts.",
            "Preset attendance, leave, and statutory defaults so HR operations do not start from blank states.",
            "Turn on security controls from day one, including MFA, retention policies, and full audit capture."
          ].map((item) => (
            <div className="rounded-[24px] border border-white/10 bg-white/5 p-4 text-sm leading-7 text-slate-300" key={item}>
              {item}
            </div>
          ))}
        </div>
        <div className="mt-6 grid gap-3">
          {[
            "Automated onboarding packs",
            "Geofence-ready attendance",
            "Payroll compliance bundles",
            "OKR and 360 review starter templates"
          ].map((item) => (
            <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white" key={item}>
              {item}
            </div>
          ))}
        </div>
      </aside>
    </div>
  );
}
