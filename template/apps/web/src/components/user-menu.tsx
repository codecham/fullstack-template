import Link from "next/link";

import { logout } from "@/app/(auth)/actions";
import { getCurrentUser } from "@/lib/auth/session";

export async function UserMenu() {
  const user = await getCurrentUser();

  if (!user) {
    return (
      <div className="flex items-center gap-4 text-sm">
        <Link href="/login">Log in</Link>
        <Link
          href="/register"
          className="rounded-md bg-gray-900 px-3 py-1.5 text-white dark:bg-white dark:text-gray-900"
        >
          Sign up
        </Link>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-4 text-sm">
      <Link href="/account">{user.email}</Link>
      <form action={logout}>
        <button type="submit" className="underline">
          Log out
        </button>
      </form>
    </div>
  );
}
