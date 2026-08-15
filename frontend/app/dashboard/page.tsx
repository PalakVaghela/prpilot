"use client";

import { useEffect, useState } from "react";

type Repository = {
  id: number;
  name: string;
  full_name: string;
  description: string;
  language: string;
  private: boolean;
  stars: number;
  forks: number;
  open_issues: number;
  html_url: string;
};

export default function Dashboard() {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/repositories/")
      .then((response) => response.json())
      .then((data) => {
        setRepositories(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to fetch repositories:", error);
        setLoading(false);
      });
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      {/* Navbar */}
      <nav className="border-b border-slate-800">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div className="text-2xl font-bold tracking-tight">
            PR<span className="text-blue-500">Pilot</span>
          </div>

          <div className="flex items-center gap-4">
            <span className="text-sm text-slate-400">
              GitHub Connected
            </span>

            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-800">
              👤
            </div>
          </div>
        </div>
      </nav>

      {/* Dashboard */}
      <section className="mx-auto max-w-7xl px-6 py-10">
        <div>
          <h1 className="text-3xl font-bold">
            Welcome back 👋
          </h1>

          <p className="mt-2 text-slate-400">
            Here's what's happening with your repositories.
          </p>
        </div>

        {/* Stats */}
        <div className="mt-8 grid gap-5 md:grid-cols-3">
          <StatCard
            title="Repositories"
            value={repositories.length.toString()}
          />

          <StatCard
            title="Pull Requests"
            value="—"
          />

          <StatCard
            title="AI Reviews"
            value="—"
          />
        </div>

        {/* Repositories */}
        <div className="mt-12">
          <h2 className="text-xl font-semibold">
            Your Repositories
          </h2>

          {loading ? (
            <p className="mt-6 text-slate-400">
              Loading repositories...
            </p>
          ) : repositories.length === 0 ? (
            <p className="mt-6 text-slate-400">
              No repositories found.
            </p>
          ) : (
            <div className="mt-5 space-y-4">
              {repositories.map((repo) => (
                <RepositoryCard
                  key={repo.id}
                  repository={repo}
                />
              ))}
            </div>
          )}
        </div>
      </section>
    </main>
  );
}

function StatCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6">
      <p className="text-sm text-slate-400">
        {title}
      </p>

      <p className="mt-3 text-3xl font-bold">
        {value}
      </p>
    </div>
  );
}

function RepositoryCard({
  repository,
}: {
  repository: Repository;
}) {
  return (
    <div className="flex items-center justify-between rounded-2xl border border-slate-800 bg-slate-900/50 p-6 transition hover:border-slate-700">
      <div>
        <h3 className="font-semibold">
          {repository.name}
        </h3>

        <p className="mt-1 text-sm text-slate-400">
          {repository.description || "No description"}
        </p>

        <div className="mt-3 flex gap-4 text-xs text-slate-500">
          <span>
            ⭐ {repository.stars}
          </span>

          <span>
            🍴 {repository.forks}
          </span>

          <span>
            {repository.language || "Unknown"}
          </span>
        </div>
      </div>

      <button className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium transition hover:bg-blue-500">
        View
      </button>
    </div>
  );
}