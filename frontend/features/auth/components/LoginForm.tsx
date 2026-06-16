"use client";

import { useRouter } from "next/navigation";

import { useForm } from "react-hook-form";

import { zodResolver } from "@hookform/resolvers/zod";

import { login } from "../api";

import { LoginFormValues, loginSchema } from "../validation";

import { useAuth } from "@/providers/AuthProvider";

export function LoginForm() {
  const router = useRouter();

  const { login: loginUser } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { isSubmitting, errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  async function onSubmit(values: LoginFormValues) {
    try {
      const response = await login(values);

      await loginUser(response.access_token);

      router.push("/dashboard");
    } catch {
      alert("Invalid credentials");
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <input
          {...register("email")}
          placeholder="Email"
          className="w-full rounded-xl border p-3"
        />

        {errors.email && <p className="mt-1 text-sm text-red-500">{errors.email.message}</p>}
      </div>

      <div>
        <input
          type="password"
          {...register("password")}
          placeholder="Password"
          className="w-full rounded-xl border p-3"
        />

        {errors.password && <p className="mt-1 text-sm text-red-500">{errors.password.message}</p>}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="
          w-full
          rounded-xl
          bg-blue-600
          py-3
          font-medium
          text-white
        "
      >
        Sign In
      </button>
    </form>
  );
}
