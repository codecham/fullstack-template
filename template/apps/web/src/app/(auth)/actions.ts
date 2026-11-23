"use server";

import { redirect } from "next/navigation";

import { api } from "@/lib/api/client";
import { createSession, deleteSession } from "@/lib/auth/session";

export type AuthFormState = { error: string } | undefined;

function readCredentials(formData: FormData) {
  return {
    email: String(formData.get("email") ?? ""),
    password: String(formData.get("password") ?? ""),
  };
}

/** Ask the API for an access token and store it in the session cookie. */
async function startSession(email: string, password: string): Promise<boolean> {
  const { data } = await api.POST("/auth/login", {
    // OAuth2 login is a form post, and calls the email "username"
    body: { username: email, password },
    bodySerializer: (body) =>
      new URLSearchParams(body as Record<string, string>),
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  if (!data) {
    return false;
  }
  await createSession(data.access_token, data.expires_in);
  return true;
}

export async function login(
  _previousState: AuthFormState,
  formData: FormData,
): Promise<AuthFormState> {
  const { email, password } = readCredentials(formData);
  if (!(await startSession(email, password))) {
    return { error: "Incorrect email or password." };
  }
  redirect("/account");
}

export async function register(
  _previousState: AuthFormState,
  formData: FormData,
): Promise<AuthFormState> {
  const { email, password } = readCredentials(formData);
  const { response } = await api.POST("/auth/register", {
    body: { email, password },
  });
  if (response.status === 409) {
    return { error: "An account with this email already exists." };
  }
  if (!response.ok) {
    return {
      error: "Enter a valid email and a password of 8 to 128 characters.",
    };
  }
  if (!(await startSession(email, password))) {
    return { error: "Your account was created, but logging in failed." };
  }
  redirect("/account");
}

export async function logout() {
  await deleteSession();
  redirect("/");
}
