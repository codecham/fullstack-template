import type { Metadata } from "next";
import Link from "next/link";

import { register } from "@/app/(auth)/actions";
import { AuthForm } from "@/components/auth-form";

export const metadata: Metadata = { title: "Sign up" };

export default function RegisterPage() {
  return (
    <section className="mx-auto flex w-full max-w-sm flex-col gap-6">
      <h1 className="text-2xl font-bold">Create an account</h1>
      <AuthForm
        action={register}
        submitLabel="Sign up"
        passwordAutoComplete="new-password"
      />
      <p className="text-sm text-gray-600 dark:text-gray-400">
        Already have an account?{" "}
        <Link href="/login" className="underline">
          Log in
        </Link>
      </p>
    </section>
  );
}
