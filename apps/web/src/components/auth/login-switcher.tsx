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
            <div className="rounded-[24px] border border-teal-200 bg-teal-50 px-4 py-3 text-sm text-teal-800">
              Demo credentials are preloaded for the seeded workspace.
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
            <button className="button-primary w-full" disabled={isSubmitting} type="submit">
              {isSubmitting ? "Verifying..." : "Verify and enter"}
            </button>
          </form>
        ) : null}

        {statusMessage ? (
          <div className="mt-4 rounded-[24px] border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">
            {statusMessage}
          </div>
        ) : null}

        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 text-sm text-slate-500">
          <span>OIDC-compliant session management</span>
          <span>GDPR-ready access logging</span>
        </div>
        <div className="mt-4 text-sm text-slate-500">
          <Link className="font-semibold text-teal-700 hover:text-teal-600" href="/dashboard">
            Open the employee dashboard
          </Link>
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
