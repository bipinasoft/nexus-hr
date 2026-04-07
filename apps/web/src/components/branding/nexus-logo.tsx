import { useId } from "react";

type NexusLogoProps = {
  className?: string;
  inverse?: boolean;
  markOnly?: boolean;
  subtitle?: string;
};

export function NexusLogo({
  className,
  inverse = false,
  markOnly = false,
  subtitle,
}: NexusLogoProps) {
  const gradientId = useId();
  const glowId = useId();

  return (
    <div className={["flex items-center gap-4", className].filter(Boolean).join(" ")}>
      <svg
        aria-hidden="true"
        className="h-12 w-12 shrink-0"
        viewBox="0 0 64 64"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <linearGradient id={gradientId} x1="8" y1="8" x2="56" y2="56" gradientUnits="userSpaceOnUse">
            <stop stopColor="#C084FC" />
            <stop offset="0.55" stopColor="#7C3AED" />
            <stop offset="1" stopColor="#312E81" />
          </linearGradient>
          <linearGradient id={glowId} x1="14" y1="16" x2="50" y2="48" gradientUnits="userSpaceOnUse">
            <stop stopColor="white" stopOpacity="0.95" />
            <stop offset="1" stopColor="#E9D5FF" stopOpacity="0.72" />
          </linearGradient>
        </defs>
        <rect x="4" y="4" width="56" height="56" rx="18" fill={`url(#${gradientId})`} />
        <path
          d="M18 44V20h6.5l14 17.4V20H46v24h-6.4L25.5 26.5V44H18Z"
          fill={`url(#${glowId})`}
        />
        <circle cx="48.5" cy="16.5" r="4.5" fill="#F5D0FE" fillOpacity="0.9" />
      </svg>

      {markOnly ? null : (
        <div>
          <p className={`font-display text-xl font-semibold ${inverse ? "text-white" : "text-slate-950"}`}>
            NexusHR
          </p>
          {subtitle ? (
            <p className={`text-sm ${inverse ? "text-slate-300" : "text-slate-500"}`}>{subtitle}</p>
          ) : null}
        </div>
      )}
    </div>
  );
}
