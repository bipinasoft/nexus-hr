import Link from "next/link";
import { SignupWizard } from "@/components/auth/signup-wizard";

export default function CreateAccountPage() {
  return (
    <main className="shell py-10 md:py-16">
      <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
        <div>
          <Link className="eyebrow" href="/">
            NexusHR launch flow
          </Link>
          <h1 className="mt-5 font-display text-4xl font-semibold text-slate-950 md:text-6xl">
            Create a branded HRMS workspace without skipping security or policy design.
          </h1>
        </div>
        <Link className="button-secondary" href="/login">
          Already have an account?
        </Link>
      </div>

      <SignupWizard />
    </main>
  );
}
