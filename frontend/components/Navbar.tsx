"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { LogOut, User } from "lucide-react";
import { useAuth } from "@/lib/auth-context";

const NAV = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/profile", label: "Profile" },
  { href: "/chat", label: "Chat Coach" },
];

export default function Navbar() {
  const { user, logout, loading } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  return (
    <header className="border-b border-slate-200 bg-white/80 backdrop-blur">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-3">
        <Link href="/" className="flex items-center gap-2 font-bold text-slate-900">
          <span className="text-2xl">🏋️</span>
          <span>AI Fitness Coach</span>
        </Link>

        {user && (
          <nav className="hidden gap-1 md:flex">
            {NAV.map((n) => (
              <Link
                key={n.href}
                href={n.href}
                className={`rounded-lg px-3 py-1.5 text-sm font-medium transition ${
                  pathname?.startsWith(n.href)
                    ? "bg-brand-500/10 text-brand-700"
                    : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                {n.label}
              </Link>
            ))}
          </nav>
        )}

        <div className="flex items-center gap-2">
          {loading ? null : user ? (
            <>
              <span className="hidden items-center gap-2 rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700 sm:inline-flex">
                <User className="h-3.5 w-3.5" />
                {user.displayName || user.email}
              </span>
              <button
                onClick={async () => {
                  await logout();
                  router.push("/");
                }}
                className="btn-secondary !py-1.5 !px-3"
              >
                <LogOut className="h-4 w-4" />
                Sign out
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="btn-secondary !py-1.5 !px-3">
                Log in
              </Link>
              <Link href="/register" className="btn-primary !py-1.5 !px-3">
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
