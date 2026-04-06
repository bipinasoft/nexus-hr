"use client";

import { useState } from "react";

type AuthMethod = "password" | "sso" | "otp";

const methods: Array<{
  id: AuthMethod;
  label: string;
  helper: string;
}> = [
  {
    id: "password",
    label: "Password",
    helper: "Email, password, and authenticator verification"
  },
  {
    id: "sso",
    label: "Enterprise SSO",
    helper: "OIDC or SAML federation for workforce identity"
  },
  {
    id: "otp",
    label: "Mobile OTP",
    helper: "Fast fallback for distributed and field teams"
  }
];

export function LoginSwitcher() {
  const [active, setActive] = useState<AuthMethod>("password");

  return (
    <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
      <div className="panel px-6 py-6 md:px-8">
        <div className="flex flex-wrap gap-2">
          {methods.map((method) => {
            const isActive = method.id === active;

            return (
              <button
                className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
                  isActive ? "bg-slate-950 text-white" : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`}
                key={method.id}
                onClick={() => setActive(method.id)}
                type="button"
              >
                {method.label}
              </button>
            );
          })}
        </div>

        <div className="mt-6">
          <p className="text-sm font-semibold text-slate-900">
            {methods.find((method) => method.id === active)?.helper}
          </p>
        </div>

        {active === "password" ? (
          <form className="mt-6 space-y-4">
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Work email</label>
              <input className="field" placeholder="you@company.com" type="email" />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Password</label>
              <input className="field" placeholder="Enter your password" type="password" />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Authenticator code</label>
              <input className="field" placeholder="6-digit MFA code" type="text" />
            </div>
            <button className="button-primary w-full" type="submit">
              Sign in securely
            </button>
          </form>
        ) : null}

        {active === "sso" ? (
          <form className="mt-6 space-y-4">
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Company domain</label>
              <input className="field" placeholder="company.nexushr.com" type="text" />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Identity provider</label>
              <select className="field" defaultValue="Azure AD">
                <option>Azure AD</option>
                <option>Okta</option>
                <option>Google Workspace</option>
                <option>Ping Identity</option>
              </select>
            </div>
            <button className="button-primary w-full" type="submit">
              Continue with SSO
            </button>
          </form>
        ) : null}

        {active === "otp" ? (
          <form className="mt-6 space-y-4">
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">Work mobile number</label>
              <input className="field" placeholder="+91 98xxxxxx98" type="tel" />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-700">One-time passcode</label>
              <input className="field" placeholder="Enter SMS or WhatsApp OTP" type="text" />
            </div>
            <button className="button-primary w-full" type="submit">
              Verify and enter
            </button>
          </form>
        ) : null}

        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 text-sm text-slate-500">
          <span>OIDC-compliant session management</span>
          <span>GDPR-ready access logging</span>
        </div>
      </div>

      <aside className="panel-dark px-6 py-6 md:px-8">
        <p className="text-xs uppercase tracking-[0.25em] text-teal-200">Adaptive access</p>
        <h2 className="mt-4 font-display text-3xl font-semibold">Step-up authentication built into the flow.</h2>
        <div className="mt-6 space-y-4">
          {[
            {
              title: "Primary identity check",
              detail: "OIDC token exchange, enterprise SSO, or password verification with phishing-resistant controls."
            },
            {
              title: "Second-factor challenge",
              detail: "Authenticator app, OTP fallback, or device trust based on policy and risk posture."
            },
            {
              title: "Scoped workspace access",
              detail: "Role, department, and team constraints are attached before any write-capable route is exposed."
            }
          ].map((item, index) => (
            <div className="rounded-[24px] border border-white/10 bg-white/5 p-4" key={item.title}>
              <p className="text-sm font-semibold text-white">
                0{index + 1}. {item.title}
              </p>
              <p className="mt-2 text-sm leading-7 text-slate-300">{item.detail}</p>
            </div>
          ))}
        </div>
        <div className="mt-6 grid gap-3 sm:grid-cols-2">
          {["Session cache on Redis", "Every write action audited", "IP and user traceability", "Least-privilege RBAC"].map(
            (item) => (
              <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200" key={item}>
                {item}
              </div>
            )
          )}
        </div>
      </aside>
    </div>
  );
}

