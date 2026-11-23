import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { Suspense } from "react";

import { getCurrentUser } from "@/lib/auth/session";

export const metadata: Metadata = { title: "Account" };

export default function AccountPage() {
  return (
    <section className="flex flex-col gap-6">
      <h1 className="text-2xl font-bold">Your account</h1>
      {/* Reading the session happens per request, so it streams in behind Suspense */}
      <Suspense fallback={<p className="text-gray-500">Loading…</p>}>
        <AccountDetails />
      </Suspense>
    </section>
  );
}

async function AccountDetails() {
  // The authoritative check: the API validates the token on every request
  const user = await getCurrentUser();
  if (!user) {
    redirect("/login");
  }

  return (
    <dl className="grid grid-cols-[max-content_1fr] gap-x-6 gap-y-2 text-sm">
      <dt className="text-gray-500">Email</dt>
      <dd>{user.email}</dd>
      <dt className="text-gray-500">Member since</dt>
      <dd>{new Date(user.created_at).toLocaleDateString("en")}</dd>
    </dl>
  );
}
