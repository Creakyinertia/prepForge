import axios from "axios";

import { getAccessToken, removeAccessToken } from "@/features/auth/auth-storage";

import { refreshAccessToken } from "./auth-refresh";

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,

  withCredentials: true,
});

apiClient.interceptors.request.use((config) => {
  const token = getAccessToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

apiClient.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    const isUnauthorized = error.response?.status === 401;

    const isRetry = originalRequest._retry;

    if (isUnauthorized && !isRetry) {
      originalRequest._retry = true;

      try {
        const newToken = await refreshAccessToken();

        originalRequest.headers.Authorization = `Bearer ${newToken}`;

        return apiClient(originalRequest);
      } catch {
        removeAccessToken();

        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);
