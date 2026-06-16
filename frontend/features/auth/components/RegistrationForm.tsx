"use client";

import { useRouter } from "next/navigation";

import { useForm } from "react-hook-form";

import { zodResolver } from "@hookform/resolvers/zod";

import { register as registerUser } from "../api";

import { RegisterFormValues, registerSchema } from "../validation";

export function RegisterForm() {
  const router = useRouter();

  const {
    register,
    handleSubmit,
    formState: { isSubmitting, errors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
  });

  async function onSubmit(values: RegisterFormValues) {
    try {
      await registerUser(values);

      router.push("/login");
    } catch {
      alert("Registration failed");
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <input
        {...register("username")}
        placeholder="Username"
        className="w-full rounded-xl border p-3"
      />

      {errors.username && <p className="text-sm text-red-500">{errors.username.message}</p>}

      <input {...register("email")} placeholder="Email" className="w-full rounded-xl border p-3" />

      {errors.email && <p className="text-sm text-red-500">{errors.email.message}</p>}

      <input
        type="password"
        {...register("password")}
        placeholder="Password"
        className="w-full rounded-xl border p-3"
      />

      {errors.password && <p className="text-sm text-red-500">{errors.password.message}</p>}

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
        Create Account
      </button>
    </form>
  );
}
