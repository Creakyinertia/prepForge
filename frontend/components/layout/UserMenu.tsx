"use client";

import { useRouter } from "next/navigation";

import { useAuth } from "@/providers/AuthProvider";

export function UserMenu() {
  const router = useRouter();

  const { user, logout } = useAuth();

  async function handleLogout() {
    await logout();

    router.replace("/login");
  }

  return (
    <div className="flex items-center gap-3">
      <div className="text-right">
        <p className="text-sm font-medium">{user?.username}</p>

        <p className="text-xs text-muted-foreground">{user?.email}</p>
      </div>

      <button
        onClick={handleLogout}
        className="
          rounded-lg
          border
          px-3
          py-2
          text-sm
        "
      >
        Logout
      </button>
    </div>
  );
}
