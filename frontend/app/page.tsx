export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      {/* Navbar */}
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
        <div className="text-2xl font-bold tracking-tight">
          PR<span className="text-blue-500">Pilot</span>
        </div>

        <button className="rounded-lg border border-slate-700 px-4 py-2 text-sm font-medium transition hover:bg-slate-800">
          Sign in
        </button>
      </nav>

      {/* Hero */}
      <section className="mx-auto flex max-w-6xl flex-col items-center px-6 pb-24 pt-20 text-center">
        <div className="mb-6 rounded-full border border-blue-500/20 bg-blue-500/10 px-4 py-2 text-sm text-blue-400">
          AI-powered GitHub code reviews
        </div>

        <h1 className="max-w-4xl text-5xl font-bold tracking-tight sm:text-6xl">
          Ship better code with
          <span className="text-blue-500"> AI-powered reviews.</span>
        </h1>

        <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-400">
          PRPilot analyzes your GitHub Pull Requests and gives you
          actionable feedback on code quality, issues, strengths, and
          improvements.
        </p>

        <div className="mt-10">
          <button className="rounded-xl bg-blue-600 px-7 py-3.5 font-semibold transition hover:bg-blue-500">
            <a href="http://127.0.0.1:8000/api/v1/auth/github/login">
              Get Started with GitHub
            </a>
          </button>
        </div>
      </section>

      {/* Features */}
      <section className="mx-auto grid max-w-6xl gap-6 px-6 pb-24 md:grid-cols-3">
        <FeatureCard
          title="AI Code Review"
          description="Analyze Pull Request changes and get an AI-generated code review."
        />

        <FeatureCard
          title="Actionable Insights"
          description="Understand strengths, issues, and suggestions without manually reviewing every change."
        />

        <FeatureCard
          title="GitHub Integration"
          description="Connect your GitHub account and review Pull Requests directly through PRPilot."
        />
      </section>

      {/* Bottom CTA */}
      <section className="border-t border-slate-800">
        <div className="mx-auto max-w-4xl px-6 py-20 text-center">
          <h2 className="text-3xl font-bold">
            Ready to review your next Pull Request?
          </h2>

          <p className="mt-4 text-slate-400">
            Connect GitHub and let PRPilot do the first pass.
          </p>

          <button className="mt-8 rounded-xl bg-blue-600 px-7 py-3.5 font-semibold transition hover:bg-blue-500">
            Connect GitHub
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-6 text-center text-sm text-slate-500">
        © 2026 PRPilot. AI-powered Pull Request reviews.
      </footer>
    </main>
  );
}

function FeatureCard({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6">
      <h3 className="text-xl font-semibold">{title}</h3>

      <p className="mt-3 leading-7 text-slate-400">
        {description}
      </p>
    </div>
  );
}