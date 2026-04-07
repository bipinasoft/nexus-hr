"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { buildApiUrl, persistSession } from "@/lib/api";

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

const securitySignals = [
  {
    label: "Session control",
    value: "Redis-backed",
    detail: "Fast, revocable workforce sessions"
  },
  {
    label: "Identity posture",
    value: "MFA enforced",
    detail: "Step-up verification across routes"
  },
  {
    label: "Access model",
    value: "RBAC scoped",
    detail: "Role, team, and department filters"
  }
];

const experienceNotes = [
  "Monthly calendar with present, leave, and holiday markers",
  "Tagged alerts routed to employees for quick action",
  "Audit-ready access events tied to user and IP",
  "SSO launch hooks for enterprise domain onboarding"
];

export function LoginSwitcher() {
  const [active, setActive] = useState<AuthMethod>("password");
  const [email, setEmail] = useState("maya.rao@nexushr.example");
  const [password, setPassword] = useState("NexusHR!2026");
  const [mfaCode, setMfaCode] = useState("246810");
  const [companyDomain, setCompanyDomain] = useState("nexushr.example");
  const [provider, setProvider] = useState("Azure AD");
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  async function submitCredentialFlow(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatusMessage(null);
    setIsSubmitting(true);

    try {
      const response = await fetch(buildApiUrl("/v1/auth/login"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email,
          password: active === "password" ? password : undefined,
          mfa_code: mfaCode,
          method: active
        })
      });

      if (!response.ok) {
        throw new Error("Unable to complete secure sign-in.");
      }

      const payload = await response.json();
      persistSession(payload);
      router.push("/dashboard");
    } catch (error) {
      setStatusMessage(error instanceof Error ? error.message : "Login failed.");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function submitSso(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatusMessage(null);
    setIsSubmitting(true);

    try {
      const response = await fetch(buildApiUrl("/v1/auth/sso/start"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          company_domain: companyDomain,
          provider
        })
      });

      if (!response.ok) {
        throw new Error("Unable to prepare SSO launch.");
      }

      const payload = (await response.json()) as { authorization_url: string };
      setStatusMessage(`SSO launch URL generated: ${payload.authorization_url}`);
    } catch (error) {
      setStatusMessage(error instanceof Error ? error.message : "SSO launch failed.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="space-y-5">
      <div className="soft-card overflow-hidden border-slate-200/90 bg-white">
        <div className="border-b border-slate-200 bg-gradient-to-br from-[#120824] via-[#24104a] to-[#581c87] px-6 py-7 text-white md:px-8">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.28em] text-violet-200">Workforce access hub</p>
              <h2 className="mt-3 font-display text-3xl font-semibold">Choose the login path your organization trusts.</h2>
              <p className="mt-3 max-w-2xl text-sm leading-7 text-slate-300">
                Password, SSO, and OTP all land in the same product experience, with policy-aware access and fast
                continuity for distributed teams.
              </p>
            </div>
            <span className="rounded-full border border-white/15 bg-white/10 px-4 py-2 text-xs uppercase tracking-[0.18em] text-slate-200">
              OIDC-ready
            </span>
          </div>

          <div className="mt-6 grid gap-3 sm:grid-cols-3">
            {securitySignals.map((item) => (
              <div className="rounded-[24px] border border-white/10 bg-white/5 px-4 py-4" key={item.label}>
                <p className="text-xs uppercase tracking-[0.18em] text-slate-400">{item.label}</p>
                <p className="mt-3 font-display text-2xl font-semibold text-white">{item.value}</p>
                <p className="mt-2 text-sm leading-6 text-slate-300">{item.detail}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="px-6 py-7 md:px-8 md:py-8">
          <div className="flex flex-wrap gap-2 rounded-full border border-slate-200 bg-slate-100/80 p-1.5">
            {methods.map((method) => {
              const isActive = method.id === active;

              return (
                <button
                  className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
                    isActive
                      ? "bg-white text-slate-950 shadow-sm"
                      : "text-slate-500 hover:bg-white/70 hover:text-slate-900"
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

          <div className="mt-5 flex flex-wrap items-center justify-between gap-3">
            <p className="text-sm font-semibold text-slate-900">
              {methods.find((method) => method.id === active)?.helper}
            </p>
            <span className="rounded-full border border-violet-200 bg-violet-50 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-violet-700">
              Product login flow
            </span>
          </div>

          {active === "password" ? (
            <form className="mt-6 space-y-4" onSubmit={submitCredentialFlow}>
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">Work email</label>
                <input className="field" onChange={(event) => setEmail(event.target.value)} type="email" value={email} />
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">Password</label>
                <input
                  className="field"
                  onChange={(event) => setPassword(event.target.value)}
                  type="password"
                  value={password}
                />
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">Authenticator code</label>
                <input className="field" onChange={(event) => setMfaCode(event.target.value)} type="text" value={mfaCode} />
              </div>
              <div className="rounded-[26px] border border-violet-200 bg-violet-50 px-5 py-4 text-sm leading-7 text-violet-900">
                <p className="font-semibold">Use the preloaded demo workspace credentials.</p>
                <div className="mt-2 grid gap-1 text-violet-800">
                  <span>Email: maya.rao@nexushr.example</span>
                  <span>Password: NexusHR!2026</span>
                  <span>MFA code: 246810</span>
                </div>
              </div>
              <button className="button-primary w-full" disabled={isSubmitting} type="submit">
                {isSubmitting ? "Signing in..." : "Sign in securely"}
              </button>
            </form>
          ) : null}

          {active === "sso" ? (
            <form className="mt-6 space-y-4" onSubmit={submitSso}>
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">Company domain</label>
                <input
                  className="field"
                  onChange={(event) => setCompanyDomain(event.target.value)}
                  type="text"
                  value={companyDomain}
                />
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">Identity provider</label>
                <select className="field" onChange={(event) => setProvider(event.target.value)} value={provider}>
                  <option>Azure AD</option>
                  <option>Okta</option>
                  <option>Google Workspace</option>
                  <option>Ping Identity</option>
                </select>
              </div>
              <div className="rounded-[26px] border border-slate-200 bg-slate-50 px-5 py-4 text-sm leading-7 text-slate-600">
                The SSO flow generates a launch URL so enterprise customers can plug NexusHR into their identity layer.
              </div>
              <button className="button-primary w-full" disabled={isSubmitting} type="submit">
                {isSubmitting ? "Preparing SSO..." : "Continue with SSO"}
              </button>
            </form>
          ) : null}

          {active === "otp" ? (
            <form className="mt-6 space-y-4" onSubmit={submitCredentialFlow}>
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">Work email</label>
                <input className="field" onChange={(event) => setEmail(event.target.value)} type="email" value={email} />
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">One-time passcode</label>
                <input className="field" onChange={(event) => setMfaCode(event.target.value)} type="text" value={mfaCode} />
              </div>
              <div className="rounded-[26px] border border-amber-200 bg-amber-50 px-5 py-4 text-sm leading-7 text-amber-900">
                Designed for field teams, kiosks, and workforce continuity when a passwordless fallback is needed.
              </div>
              <button className="button-primary w-full" disabled={isSubmitting} type="submit">
                {isSubmitting ? "Verifying..." : "Verify and enter"}
              </button>
            </form>
          ) : null}

          {statusMessage ? (
            <div className="mt-4 rounded-[24px] border border-slate-200 bg-slate-50 px-4 py-3 text-sm leading-7 text-slate-600">
              {statusMessage}
            </div>
          ) : null}

          <div className="mt-6 flex flex-wrap items-center justify-between gap-3 border-t border-slate-200 pt-5 text-sm text-slate-500">
            <span>OIDC-compliant session management</span>
            <span>GDPR-ready access logging</span>
            <Link className="font-semibold text-violet-700 hover:text-violet-600" href="/dashboard">
              Open the employee dashboard
            </Link>
          </div>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="panel-dark px-6 py-6 md:px-7">
          <p className="text-xs uppercase tracking-[0.25em] text-violet-200">Why it feels like product</p>
          <div className="mt-5 grid gap-3">
            {experienceNotes.map((item, index) => (
              <div className="rounded-[24px] border border-white/10 bg-white/5 px-4 py-4" key={item}>
                <p className="text-sm font-semibold text-white">
                  0{index + 1}. {item}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div className="panel px-6 py-6 md:px-7">
          <p className="text-xs uppercase tracking-[0.25em] text-slate-500">After login</p>
          <h3 className="mt-3 font-display text-3xl font-semibold text-slate-950">Employees land in a useful workspace, not a blank portal.</h3>
          <p className="mt-3 text-sm leading-7 text-slate-600">
            Attendance, leave, notifications, and policy-aware prompts appear immediately so the first screen drives
            action instead of orientation.
          </p>
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            {[
              "Interactive monthly attendance calendar",
              "Leave balances and approval context",
              "Tagged alerts for rapid response",
              "Copilot guidance on day-one tasks"
            ].map((item) => (
              <div className="rounded-[24px] border border-slate-200 bg-slate-50 px-4 py-4 text-sm leading-7 text-slate-600" key={item}>
                {item}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
