import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white flex flex-col items-center justify-center">
      <h1 className="text-5xl font-bold mb-6">
        Churn AI Platform
      </h1>

      <p className="text-gray-400 mb-8">
        AI Powered Customer Retention Intelligence
      </p>

      <Link
        href="/dashboard"
        className="bg-white text-black px-6 py-3 rounded-xl font-semibold"
      >
        Go to Dashboard
      </Link>
    </main>
  );
}