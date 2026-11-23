"use client";

import { useActionState } from "react";

import type { AuthFormState } from "@/app/(auth)/actions";

type AuthFormProps = {
  action: (state: AuthFormState, formData: FormData) => Promise<AuthFormState>;
  submitLabel: string;
  passwordAutoComplete: "current-password" | "new-password";
};

export function AuthForm({
  action,
  submitLabel,
  passwordAutoComplete,
}: AuthFormProps) {
  const [state, formAction, pending] = useActionState(action, undefined);

  return (
    <form action={formAction} className="flex flex-col gap-4">
      <label className="flex flex-col gap-1 text-sm font-medium">
        Email
        <input
          name="email"
          type="email"
          autoComplete="email"
          required
          className="rounded-md border border-gray-300 px-3 py-2 font-normal dark:border-gray-700 dark:bg-gray-900"
        />
      </label>
      <label className="flex flex-col gap-1 text-sm font-medium">
        Password
        <input
          name="password"
          type="password"
          autoComplete={passwordAutoComplete}
          minLength={8}
          maxLength={128}
          required
          className="rounded-md border border-gray-300 px-3 py-2 font-normal dark:border-gray-700 dark:bg-gray-900"
        />
      </label>
      {state?.error && (
        <p role="alert" className="text-sm text-red-600">
          {state.error}
        </p>
      )}
      <button
        type="submit"
        disabled={pending}
        className="rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-700 disabled:opacity-50 dark:bg-white dark:text-gray-900"
      >
        {pending ? "Please wait…" : submitLabel}
      </button>
    </form>
  );
}
