import Link from "next/link";
import { Suspense } from "react";

import { ApiStatus } from "@/components/api-status";
import { site } from "@/lib/site";

export default function HomePage() {
  return (
    <section className="flex flex-col gap-6">
      <h1 className="text-4xl font-bold">{site.name}</h1>
      <p className="text-lg text-gray-600 dark:text-gray-400">
        {site.description}
      </p>
      <Suspense
        fallback={<p className="text-sm text-gray-500">Checking the API…</p>}
      >
        <ApiStatus />
      </Suspense>
      <div>
        <Link
          href="/register"
          className="inline-block rounded-md bg-gray-900 px-4 py-2 text-sm font-medium text-white dark:bg-white dark:text-gray-900"
        >
          Get started
        </Link>
      </div>
    </section>
  );
}
