import { SignupWizard } from "@/components/auth/signup-wizard";
import { SiteFooter } from "@/components/marketing/site-footer";
import { SiteHeader, type SiteNavLink } from "@/components/marketing/site-header";

const navigationLinks: SiteNavLink[] = [
  { label: "Products", href: "/#products" },
  { label: "Platform", href: "/#platform" },
  { label: "Security", href: "/#security" },
  { label: "Launch", href: "/#launch" }
];

export default function CreateAccountPage() {
  return (
    <>
      <SiteHeader
        links={navigationLinks}
        primaryAction={{ href: "/login", label: "Sign in" }}
        secondaryAction={{ href: "/", label: "Back to website" }}
        subtitle="Enterprise HRMS launch workspace"
      />

      <main className="overflow-hidden pb-6">
        <section className="shell pt-10 md:pt-14">
          <div className="grid gap-8 xl:grid-cols-[0.9fr_1.1fr] xl:items-end">
            <div className="space-y-6">
              <span className="eyebrow">Launch workflow</span>
              <h1 className="max-w-3xl font-display text-4xl font-semibold text-slate-950 md:text-6xl">
                Create a branded HRMS workspace with the same polish as the public website.
              </h1>
              <p className="max-w-3xl text-lg leading-8 text-slate-600">
                Configure company identity, rollout defaults, and security posture in a guided flow built for enterprise
                HR and IT teams that want structure from the beginning.
              </p>
            </div>

            <div className="grid gap-4 md:grid-cols-3">
              {[
                ["Day 0", "Workspace ready"],
                ["3", "Launch steps"],
                ["100%", "Security-first setup"]
              ].map(([value, label]) => (
                <div className="website-card h-full px-5 py-5" key={label}>
                  <p className="font-display text-3xl font-semibold text-slate-950">{value}</p>
                  <p className="mt-2 text-xs uppercase tracking-[0.18em] text-slate-500">{label}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="shell pt-10 md:pt-12">
          <SignupWizard />
        </section>
      </main>

      <SiteFooter />
    </>
  );
}
