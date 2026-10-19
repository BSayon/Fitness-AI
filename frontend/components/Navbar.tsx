"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname, useRouter } from "next/navigation";
import { LogOut } from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import ThemeToggle from "@/components/ThemeToggle";

const NAV = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/profile", label: "Profile" },
  { href: "/chat", label: "Coach" },
];

export default function Navbar() {
  const { user, logout, loading } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  return (
    <header className="sticky top-0 z-50 border-b border-white/30 bg-white/40 backdrop-blur-xl dark:border-white/10 dark:bg-black/30">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-3">
        <Link href="/" className="flex items-center gap-2.5">
          <Image
            src="/logo.png"
            alt="Zesayro"
            width={32}
            height={32}
            className="h-8 w-8 rounded-lg"
            priority
          />
          <span className="text-lg font-bold tracking-tight text-slate-900 dark:text-white">
            Zesayro
          </span>
        </Link>

        {user && (
          <nav className="hidden gap-1 md:flex">
            {NAV.map((n) => (
              <Link
                key={n.href}
                href={n.href}
                className={`rounded-lg px-3 py-1.5 text-sm font-medium transition ${
                  pathname?.startsWith(n.href)
                    ? "bg-brand-500/15 text-brand-700 dark:text-brand-300"
                    : "text-slate-600 hover:bg-white/50 dark:text-slate-300 dark:hover:bg-white/10"
                }`}
              >
                {n.label}
              </Link>
            ))}
          </nav>
        )}

        <div className="flex items-center gap-2">
          <ThemeToggle />
          {loading ? null : user ? (
            <button
              onClick={async () => {
                await logout();
                router.push("/");
              }}
              className="btn-secondary !py-1.5 !px-3"
            >
              <LogOut className="h-4 w-4" />
              <span className="hidden sm:inline">Sign out</span>
            </button>
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
