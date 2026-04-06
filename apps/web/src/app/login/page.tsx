import Link from "next/link";
import { LoginSwitcher } from "@/components/auth/login-switcher";

export default function LoginPage() {
  return (
    <main className="shell py-10 md:py-16">
      <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
        <div>
          <Link className="eyebrow" href="/">
            Back to NexusHR
          </Link>
          <h1 className="mt-5 font-display text-4xl font-semibold text-slate-950 md:text-6xl">
            Secure access for every persona in the HR operating model.
          </h1>
        </div>
        <Link className="button-secondary" href="/create-account">
          Create a new workspace
        </Link>
      </div>

      <LoginSwitcher />
    </main>
  );
}

