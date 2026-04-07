import Link from "next/link";

import { NexusLogo } from "@/components/branding/nexus-logo";

const productLinks = [
  { href: "/#products", label: "Employee lifecycle" },
  { href: "/#products", label: "Attendance and leave" },
  { href: "/#products", label: "Payroll and compliance" },
  { href: "/#products", label: "Performance management" }
];

const platformLinks = [
  { href: "/#platform", label: "Architecture" },
  { href: "/#security", label: "Security and compliance" },
  { href: "/#launch", label: "Implementation" },
  { href: "/login", label: "Live login" }
];

const resourceLinks = [
  { href: "/create-account", label: "Launch workspace" },
  { href: "/dashboard", label: "Employee dashboard" },
  { href: "https://github.com/bipinasoft/nexus-hr", label: "GitHub repository" }
];

export function SiteFooter() {
  return (
    <footer className="shell pb-10 pt-16 md:pt-20">
      <div className="panel-dark overflow-hidden px-6 py-8 md:px-8 md:py-10">
        <div className="grid gap-10 xl:grid-cols-[1.1fr_0.9fr]">
          <div>
            <NexusLogo inverse subtitle="Corporate workforce platform" />
            <h2 className="mt-6 max-w-2xl font-display text-4xl font-semibold text-white md:text-5xl">
              A public brand, secure login, and employee workspace designed as one coherent product.
            </h2>
            <p className="mt-4 max-w-2xl text-sm leading-8 text-slate-300 md:text-base">
              NexusHR combines marketing-grade storytelling with enterprise HR operations so teams move from discovery
              to adoption without visual or workflow friction.
            </p>

            <div className="mt-8 flex flex-wrap gap-4">
              <Link className="button-primary" href="/login">
                Open the live product
              </Link>
              <Link
                className="button-secondary border-white/20 bg-white/5 text-white hover:border-white/40 hover:bg-white/10"
                href="/create-account"
              >
                Start a launch plan
              </Link>
            </div>
          </div>

          <div className="grid gap-8 md:grid-cols-3">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-violet-200">Product</p>
              <div className="mt-4 grid gap-3">
                {productLinks.map((item) => (
                  <Link className="footer-link" href={item.href} key={item.label}>
                    {item.label}
                  </Link>
                ))}
              </div>
            </div>

            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-violet-200">Platform</p>
              <div className="mt-4 grid gap-3">
                {platformLinks.map((item) => (
                  <Link className="footer-link" href={item.href} key={item.label}>
                    {item.label}
                  </Link>
                ))}
              </div>
            </div>

            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-violet-200">Resources</p>
              <div className="mt-4 grid gap-3">
                {resourceLinks.map((item) => (
                  <Link className="footer-link" href={item.href} key={item.label}>
                    {item.label}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="mt-10 flex flex-col gap-3 border-t border-white/10 pt-6 text-sm text-slate-400 md:flex-row md:items-center md:justify-between">
          <span>GDPR-aware. ISO 27001-aligned. Role-scoped by design.</span>
          <span>Next.js, FastAPI, PostgreSQL, Redis, MongoDB, Helm, and Kubernetes ready.</span>
        </div>
      </div>
    </footer>
  );
}
