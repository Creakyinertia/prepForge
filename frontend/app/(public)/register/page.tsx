import Link from "next/link";

import { RegisterForm } from "@/features/auth/components/RegistrationForm";
import { PublicRoute } from "@/components/auth/PublicRoute";

export default function RegisterPage() {
  return (
    <PublicRoute>
      <main className="flex min-h-screen items-center justify-center px-6">
        <div className="w-full max-w-md">
          <h1 className="mb-2 text-3xl font-bold">Create Account</h1>

          <p className="mb-8 text-muted-foreground">Start your interview preparation journey.</p>

          <RegisterForm />

          <p className="mt-6 text-center text-sm">
            Already have an account?{" "}
            <Link href="/login" className="text-blue-600">
              Login
            </Link>
          </p>
        </div>
      </main>
    </PublicRoute>
  );
}
