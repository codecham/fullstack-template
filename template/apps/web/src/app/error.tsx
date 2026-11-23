"use client";

// Shown when a page fails to render (for example when the API is down)
export default function Error({ reset }: { reset: () => void }) {
  return (
    <section className="flex flex-col items-start gap-4">
      <h1 className="text-2xl font-bold">Something went wrong</h1>
      <p className="text-gray-600 dark:text-gray-400">
        The page could not be loaded. Please try again.
      </p>
      <button type="button" onClick={reset} className="underline">
        Try again
      </button>
    </section>
  );
}
