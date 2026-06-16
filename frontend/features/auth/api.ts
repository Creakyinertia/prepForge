import { apiClient } from "@/services/api-client";

import { LoginRequest, LoginResponse, RegisterRequest, User } from "./types";

export async function login(payload: LoginRequest) {
  const response = await apiClient.post<LoginResponse>("/auth/login", payload);

  return response.data;
}

export async function register(payload: RegisterRequest) {
  const response = await apiClient.post<User>("/auth/register", payload);

  return response.data;
}

export async function getMe() {
  const response = await apiClient.get<User>("/auth/me");

  return response.data;
}

export async function logout() {
  await apiClient.post("/auth/logout");
}

export async function refreshToken() {
  const response = await apiClient.post<LoginResponse>("/auth/refresh");

  return response.data;
}
