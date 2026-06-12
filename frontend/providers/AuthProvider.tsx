"use client";

import { createContext, useContext, useEffect, useState } from "react";

import { getMe, logout as logoutApi } from "@/features/auth/api";

import { getAccessToken, removeAccessToken, setAccessToken } from "@/features/auth/auth-storage";

import { User } from "@/features/auth/types";

type AuthContextType = {
  user: User | null;

  isAuthenticated: boolean;

  isLoading: boolean;

  login: (accessToken: string) => Promise<void>;

  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    initializeAuth();
  }, []);

  async function initializeAuth() {
    try {
      const token = getAccessToken();

      if (!token) {
        setIsLoading(false);
        return;
      }

      const user = await getMe();

      setUser(user);
    } catch {
      removeAccessToken();
    } finally {
      setIsLoading(false);
    }
  }

  async function login(accessToken: string) {
    setAccessToken(accessToken);

    const user = await getMe();

    setUser(user);
  }

  async function logout() {
    try {
      await logoutApi();
    } finally {
      removeAccessToken();

      setUser(null);
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,

        isLoading,

        isAuthenticated: !!user,

        login,

        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }

  return context;
}
