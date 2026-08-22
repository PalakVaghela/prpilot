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

export default function PullRequestPage() {
  const params = useParams();
  const router = useRouter();

  const prId = params.id;

  const [pullRequest, setPullRequest] = useState<PullRequest | null>(null);
  const [loading, setLoading] = useState(true);
  const [reviewing, setReviewing] = useState(false);
  const [review, setReview] = useState<any>(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/v1/pull-req/${prId}/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch pull request");
        }

        return response.json();
      })
      .then((data) => {
        setPullRequest(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to fetch pull request:", error);
        setLoading(false);
      });
  }, [prId]);

    const handleAIReview = async () => {
      setReviewing(true);

      try {
        const response = await fetch(
          `http://localhost:8000/api/v1/pull-req/${prId}/ai-review/`,
          {
            method: "POST",
          }
        );

        if (!response.ok) {
          throw new Error("AI review failed");
        }

        const data = await response.json();

        setReview(data.review);
      } catch (error) {
        console.error("AI review failed:", error);
      } finally {
        setReviewing(false);
      }
  };

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-950 text-white p-10">
        <p className="text-slate-400">Loading pull request...</p>
      </main>
    );
  }

  if (!pullRequest) {
    return (
      <main className="min-h-screen bg-slate-950 text-white p-10">
        <p className="text-slate-400">
          Pull request not found.
        </p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <nav className="border-b border-slate-800">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <button
            onClick={() => router.back()}
            className="text-sm text-slate-400 hover:text-white"
          >
            ← Back
          </button>

          <div className="text-2xl font-bold">
            PR<span className="text-blue-500">Pilot</span>
          </div>
        </div>
      </nav>

      <section className="mx-auto max-w-5xl px-6 py-10">

        <div className="flex items-center gap-3">
          <span className="text-slate-500">
            #{pullRequest.number}
          </span>

          <span className="rounded-full bg-green-500/10 px-3 py-1 text-xs text-green-400">
            {pullRequest.state}
          </span>
        </div>

        <h1 className="mt-4 text-3xl font-bold">
          {pullRequest.title}
        </h1>

        <p className="mt-3 text-slate-400">
          👤 {pullRequest.author}
        </p>

        <div className="mt-4 text-sm text-slate-500">
          {pullRequest.head_branch}
          {" → "}
          {pullRequest.base_branch}
        </div>

        <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900/50 p-6">
          <h2 className="text-lg font-semibold">
            Description
          </h2>

          <p className="mt-4 whitespace-pre-wrap text-sm leading-7 text-slate-400">
            {pullRequest.description || "No description provided."}
          </p>
        </div>

        <div className="mt-8 flex gap-4">
          <a
            href={pullRequest.html_url}
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-lg border border-slate-700 px-5 py-3 text-sm font-medium hover:bg-slate-900"
          >
            View on GitHub ↗
          </a>

          <button className="rounded-lg bg-blue-600 px-5 py-3 text-sm font-medium transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
          onClick={handleAIReview} disabled={reviewing}
          >
            {reviewing ? "🤖 Reviewing..." : "🤖 Review with AI"}
          </button>
        </div>

      </section>

      {reviewing && (
      <div className="mt-6 rounded-xl border border-blue-500/20 bg-blue-500/5 p-5">
        <div className="flex items-center gap-3">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-slate-600 border-t-blue-500" />

          <div>
            <p className="font-medium text-white">
              AI is reviewing this pull request...
            </p>

            <p className="mt-1 text-sm text-slate-400">
              Analyzing the code changes and generating suggestions.
            </p>
          </div>
        </div>
      </div>
    )}

      {review && (
      <div className="mt-10 rounded-2xl border border-slate-800 bg-slate-900/50 p-6">
        <h2 className="text-xl font-semibold">
          🤖 AI Review
        </h2>

        <div className="mt-6 text-4xl font-bold text-blue-400">
          {review.score}/100
        </div>

        <div className="mt-8">
          <h3 className="font-semibold">Summary</h3>

          <p className="mt-2 text-slate-400">
            {review.summary}
          </p>
        </div>

        <div className="mt-8">
          <h3 className="font-semibold">Strengths</h3>

          <ul className="mt-3 space-y-2 text-slate-400">
            {review.strengths.map((item: string, index: number) => (
              <li key={index}>✓ {item}</li>
            ))}
          </ul>
        </div>

    <div className="mt-8">
      <h3 className="font-semibold">
        Issues
      </h3>

    <div className="mt-3 space-y-3">
      {review.issues.map((issue: any, index: number) => (
        <div
          key={index}
          className="rounded-lg border border-slate-800 bg-slate-950 p-4"
        >
          <div className="flex items-center gap-3">
            <span className="rounded-md bg-red-500/10 px-2 py-1 text-xs text-red-400">
              {issue.severity}
            </span>

            <span className="text-xs text-slate-500">
              {issue.file}:{issue.line}
            </span>
          </div>

          <p className="mt-2 text-sm text-slate-300">
            {issue.message}
          </p>
        </div>
      ))}
    </div>
  </div>

        <div className="mt-8">
          <h3 className="font-semibold">Suggestions</h3>

          <ul className="mt-3 space-y-2 text-slate-400">
            {review.suggestions.map((item: string, index: number) => (
              <li key={index}>💡 {item}</li>
            ))}
          </ul>
        </div>
      </div>
    )}
    </main>
  );
}
