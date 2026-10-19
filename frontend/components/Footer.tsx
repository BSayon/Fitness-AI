import Link from "next/link";

export default function Footer() {
  return (
    <footer className="mt-auto border-t border-white/30 bg-white/30 backdrop-blur-xl dark:border-white/10 dark:bg-black/20">
      <div className="mx-auto flex w-full max-w-6xl flex-col items-center justify-between gap-2 px-4 py-5 text-sm text-slate-500 sm:flex-row dark:text-slate-400">
        <span>© {new Date().getFullYear()} Zesayro. All rights reserved.</span>
        <nav className="flex items-center gap-4">
          <Link
            href="/privacy"
            className="transition hover:text-brand-600 dark:hover:text-brand-300"
          >
            Privacy Policy
          </Link>
        </nav>
      </div>
    </footer>
  );
}
