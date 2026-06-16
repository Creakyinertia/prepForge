import { apiClient } from "./api-client";

import { setAccessToken, removeAccessToken } from "@/features/auth/auth-storage";

type RefreshResponse = {
  access_token: string;

  token_type: string;
};

export async function refreshAccessToken() {
  try {
    const response = await apiClient.post<RefreshResponse>("/auth/refresh");

    const token = response.data.access_token;

    setAccessToken(token);

    return token;
  } catch {
    removeAccessToken();

    throw new Error("Unable to refresh token");
  }
}
