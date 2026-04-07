import { LoginSwitcher } from "@/components/auth/login-switcher";
import { SiteFooter } from "@/components/marketing/site-footer";
import { SiteHeader, type SiteNavLink } from "@/components/marketing/site-header";

const spotlightItems = [
  "Monthly attendance calendar with leave and holiday markers",
  "Alerts and notifications tagged by employee action",
  "Streaming HR copilot with policy-aware answers",
  "Enterprise security with JWT, RBAC, MFA, and SSO hooks"
];

const navigationLinks: SiteNavLink[] = [
  { label: "Products", href: "/#products" },
  { label: "Platform", href: "/#platform" },
  { label: "Security", href: "/#security" },
  { label: "Launch", href: "/#launch" }
];

export default function LoginPage() {
  return (
    <>
      <SiteHeader
        links={navigationLinks}
        primaryAction={{ href: "/create-account", label: "Create workspace" }}
        secondaryAction={{ href: "/", label: "Back to website" }}
        subtitle="Product-led enterprise HRMS"
      />

      <main className="overflow-hidden pb-6">
        <section className="shell relative pt-10 md:pt-14">
          <div className="hero-orb left-0 top-12 h-52 w-52 bg-violet-300/35" />
          <div className="hero-orb right-10 top-20 h-56 w-56 bg-fuchsia-200/50" />

          <div className="grid gap-8 xl:grid-cols-[0.86fr_1.14fr] xl:items-start">
            <div className="relative z-10 space-y-7">
              <div className="space-y-5">
                <span className="eyebrow">Secure product access</span>
                <h1 className="max-w-2xl font-display text-5xl font-semibold tracking-tight text-slate-950 md:text-6xl">
                  Sign in through a page that feels like the product, not a disconnected form.
                </h1>
                <p className="max-w-2xl text-lg leading-8 text-slate-600">
                  This login page now sits inside the same website language as the public brand, so the experience
                  feels consistent from first impression through authenticated use.
                </p>
              </div>

              <div className="grid gap-4">
                {spotlightItems.map((item, index) => (
                  <div className="website-card px-5 py-4" key={item}>
                    <div className="flex items-start gap-4">
                      <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-slate-950 font-display text-sm font-semibold text-white">
                        0{index + 1}
                      </span>
                      <p className="text-sm leading-7 text-slate-600">{item}</p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="website-card-dark px-6 py-6">
                <p className="text-xs uppercase tracking-[0.28em] text-violet-200">Inside the product</p>
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

        <section className="shell pt-14 md:pt-16">
          <div className="grid auto-rows-fr gap-4 md:grid-cols-3">
            {[
              {
                title: "Identity routes",
                detail: "Password, SSO, and OTP are presented as clear product choices rather than a flat technical form."
              },
              {
                title: "Trust at the point of login",
                detail: "Users see the same product story, security posture, and value framing before entering the dashboard."
              },
              {
                title: "A cleaner path into the dashboard",
                detail: "The experience is visually aligned with the rest of the website, so the transition into the app feels deliberate."
              }
            ].map((item) => (
              <article className="website-card h-full px-6 py-6" key={item.title}>
                <p className="text-xs uppercase tracking-[0.22em] text-slate-500">Login experience</p>
                <h2 className="mt-3 font-display text-2xl font-semibold text-slate-950">{item.title}</h2>
                <p className="mt-3 text-sm leading-7 text-slate-600">{item.detail}</p>
              </article>
            ))}
          </div>
        </section>
      </main>

      <SiteFooter />
    </>
  );
}
