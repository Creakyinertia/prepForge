import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <section className="mx-auto flex max-w-7xl flex-col items-center justify-center px-6 py-32 text-center">
        <h1 className="max-w-4xl text-5xl font-bold tracking-tight">
          Become Interview Ready.
        </h1>

        <p className="mt-6 max-w-2xl text-lg text-slate-600">
          Structured roadmaps, revision
          tracking, interview questions,
          notes, and readiness scoring
          designed for engineers.
        </p>

        <div className="mt-10 flex gap-4">
          <Link
            href="/register"
            className="rounded-xl bg-blue-600 px-6 py-3 font-medium text-white"
          >
            Get Started
          </Link>

          <Link
            href="/login"
            className="rounded-xl border px-6 py-3 font-medium"
          >
            Sign In
          </Link>
        </div>
      </section>
    </main>
  );
}