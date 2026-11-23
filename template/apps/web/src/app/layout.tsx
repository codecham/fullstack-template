import type { Metadata } from "next";
import Link from "next/link";
import { Suspense } from "react";

import { UserMenu } from "@/components/user-menu";
import { site } from "@/lib/site";

import "./globals.css";

export const metadata: Metadata = {
  title: { default: site.name, template: `%s · ${site.name}` },
  description: site.description,
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="flex min-h-full flex-col">
        <header className="border-b border-gray-200 dark:border-gray-800">
          <nav className="mx-auto flex max-w-3xl items-center justify-between px-6 py-4">
            <Link href="/" className="font-semibold">
              {site.name}
            </Link>
            <Suspense fallback={null}>
              <UserMenu />
            </Suspense>
          </nav>
        </header>
        <main className="mx-auto flex w-full max-w-3xl flex-1 flex-col px-6 py-12">
          {children}
        </main>
      </body>
    </html>
  );
}
