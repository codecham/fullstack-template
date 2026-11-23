import type { Metadata } from "next";
import Link from "next/link";

import { login } from "@/app/(auth)/actions";
import { AuthForm } from "@/components/auth-form";

export const metadata: Metadata = { title: "Log in" };

export default function LoginPage() {
  return (
    <section className="mx-auto flex w-full max-w-sm flex-col gap-6">
      <h1 className="text-2xl font-bold">Log in</h1>
      <AuthForm
        action={login}
        submitLabel="Log in"
        passwordAutoComplete="current-password"
      />
      <p className="text-sm text-gray-600 dark:text-gray-400">
        No account yet?{" "}
        <Link href="/register" className="underline">
          Sign up
        </Link>
      </p>
    </section>
  );
}
