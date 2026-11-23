import { connection } from "next/server";

import { api } from "@/lib/api/client";

/** Shows whether the API and its database answer. Rendered on each request. */
export async function ApiStatus() {
  await connection(); // render at request time, never at build time
  const healthy = await api.GET("/health/db").then(
    ({ response }) => response.ok,
    () => false, // network error: the API is not reachable
  );

  return (
    <p className="flex items-center gap-2 text-sm">
      <span
        className={`h-2.5 w-2.5 rounded-full ${healthy ? "bg-green-500" : "bg-red-500"}`}
      />
      {healthy ? "API and database are up" : "API or database unreachable"}
    </p>
  );
}
