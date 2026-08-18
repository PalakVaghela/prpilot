"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

type PullRequest = {
  id: number;
  number: number;
  title: string;
  description: string;
  state: string;
  author: string;
  base_branch: string;
  head_branch: string;
  html_url: string;
};

export default function RepositoryPage() {
  const params = useParams();
  const router = useRouter();

  const repositoryId = params.id;

  const [pullRequests, setPullRequests] = useState<PullRequest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(
      `http://localhost:8000/api/v1/pull-req/repository/${repositoryId}/`
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch pull requests");
        }

        return response.json();
      })
      .then((data) => {
        setPullRequests(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to fetch pull requests:", error);
        setLoading(false);
      });
  }, [repositoryId]);

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <nav className="border-b border-slate-800">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <button
            onClick={() => router.push("/dashboard")}
            className="text-sm text-slate-400 hover:text-white"
          >
            ← Back to Dashboard
          </button>

          <div className="text-2xl font-bold">
            PR<span className="text-blue-500">Pilot</span>
          </div>
        </div>
      </nav>

      <section className="mx-auto max-w-5xl px-6 py-10">
        <div>
          <p className="text-sm text-blue-400">
            Repository
          </p>

          <h1 className="mt-2 text-3xl font-bold">
            Pull Requests
          </h1>

          <p className="mt-2 text-slate-400">
            Review pull requests with AI-powered code analysis.
          </p>
        </div>

        {loading ? (
          <div className="mt-10 text-slate-400">
            Loading pull requests...
          </div>
        ) : pullRequests.length === 0 ? (
          <div className="mt-10 rounded-2xl border border-slate-800 bg-slate-900/50 p-8 text-center">
            <p className="text-slate-300">
              No pull requests found.
            </p>

            <p className="mt-2 text-sm text-slate-500">
              Try syncing your pull requests from GitHub.
            </p>
          </div>
        ) : (
          <div className="mt-8 space-y-4">
            {pullRequests.map((pr) => (
              <div
                key={pr.id}
                className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 transition hover:border-slate-700"
              >
                <div className="flex items-start justify-between gap-6">
                  <div className="min-w-0">
                    <div className="flex items-center gap-3">
                      <span className="text-sm font-medium text-slate-500">
                        #{pr.number}
                      </span>

                      <span
                        className={`rounded-full px-2.5 py-1 text-xs font-medium ${
                          pr.state === "open"
                            ? "bg-green-500/10 text-green-400"
                            : "bg-slate-700 text-slate-300"
                        }`}
                      >
                        {pr.state}
                      </span>
                    </div>

                    <h2 className="mt-3 text-lg font-semibold">
                      {pr.title}
                    </h2>

                    <p className="mt-2 line-clamp-2 text-sm text-slate-400">
                      {pr.description || "No description provided."}
                    </p>

                    <div className="mt-4 flex gap-4 text-xs text-slate-500">
                      <span>
                        👤 {pr.author}
                      </span>

                      <span>
                        {pr.head_branch} → {pr.base_branch}
                      </span>
                    </div>
                  </div>

                  <button
                    onClick={() =>
                      router.push(`/dashboard/pr/${pr.id}`)
                    }
                    className="shrink-0 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium hover:bg-blue-500"
                  >
                    Review
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
