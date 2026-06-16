import Link from "next/link";
import { PublicRoute } from "@/components/auth/PublicRoute";
import { LoginForm } from "@/features/auth/components/LoginForm";

export default function LoginPage() {
  return (
    <PublicRoute>
      <main className="flex min-h-screen items-center justify-center px-6">
        <div className="w-full max-w-md">
          <h1 className="mb-2 text-3xl font-bold">Welcome Back</h1>

          <p className="mb-8 text-muted-foreground">Sign in to continue.</p>

          <LoginForm />

          <p className="mt-6 text-center text-sm">
            No account?{" "}
            <Link href="/register" className="text-blue-600">
              Register
            </Link>
          </p>
        </div>
      </main>
    </PublicRoute>
  );
}
