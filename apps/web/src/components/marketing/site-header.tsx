import Link from "next/link";

export type SiteNavLink = {
  href: string;
  label: string;
};

type SiteHeaderProps = {
  links: SiteNavLink[];
  primaryAction: {
    href: string;
    label: string;
  };
  secondaryAction: {
    href: string;
    label: string;
  };
  subtitle?: string;
};

export function SiteHeader({
  links,
  primaryAction,
  secondaryAction,
  subtitle = "Enterprise HRMS for change-ready teams."
}: SiteHeaderProps) {
  return (
    <header className="shell sticky top-4 z-50 pt-6 md:pt-8">
      <div className="site-nav px-5 py-4 md:px-7">
        <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
          <Link className="flex items-center gap-4" href="/">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-950 font-display text-xl font-bold text-white">
              N
            </div>
            <div>
              <p className="font-display text-xl font-semibold text-slate-950">NexusHR</p>
              <p className="text-sm text-slate-500">{subtitle}</p>
            </div>
          </Link>

          <nav className="hidden items-center gap-6 xl:flex">
            {links.map((item) => (
              <a className="nav-link" href={item.href} key={item.label}>
                {item.label}
              </a>
            ))}
          </nav>

          <div className="flex flex-wrap gap-3">
            <Link className="button-secondary" href={secondaryAction.href}>
              {secondaryAction.label}
            </Link>
            <Link className="button-primary" href={primaryAction.href}>
              {primaryAction.label}
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}
