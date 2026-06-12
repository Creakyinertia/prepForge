import axios from "axios";

import { getAccessToken } from "@/features/auth/auth-storage";

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
