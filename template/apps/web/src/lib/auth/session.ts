import "server-only";

import { cookies } from "next/headers";
import { cache } from "react";

import { api } from "@/lib/api/client";
import type { components } from "@/lib/api/schema";

export type User = components["schemas"]["UserRead"];

const SESSION_COOKIE = "session";

/** Store the API access token in a cookie that client-side JavaScript cannot read. */
export async function createSession(
  accessToken: string,
  expiresInSeconds: number,
) {
  const cookieStore = await cookies();
  cookieStore.set(SESSION_COOKIE, accessToken, {
    httpOnly: true, // not readable from JavaScript: protects the token against XSS
    secure: process.env.NODE_ENV === "production", // HTTPS only in production
    sameSite: "lax", // not sent on cross-site POST requests: protects against CSRF
    path: "/",
    maxAge: expiresInSeconds, // the cookie disappears when the token expires
  });
}

export async function deleteSession() {
  const cookieStore = await cookies();
  cookieStore.delete(SESSION_COOKIE);
}

/**
 * The logged-in user, or null. Wrapped in React's `cache` so several components
 * can call it during one request while the API is only asked once.
 */
export const getCurrentUser = cache(async (): Promise<User | null> => {
  const cookieStore = await cookies();
  const token = cookieStore.get(SESSION_COOKIE)?.value;
  if (!token) {
    return null;
  }
  const { data } = await api.GET("/users/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return data ?? null; // an expired or invalid token gives a 401: treat as logged out
});
