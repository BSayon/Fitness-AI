"use client";

import Link from "next/link";
import Image from "next/image";
import { Dumbbell, Salad, LineChart, MessageCircle } from "lucide-react";
import { useAuth } from "@/lib/auth-context";

const FEATURES = [
  { icon: Dumbbell, label: "Workouts" },
  { icon: Salad, label: "Nutrition" },
  { icon: LineChart, label: "Tracking" },
  { icon: MessageCircle, label: "AI Coach" },
];

export default function LandingPage() {
  const { user } = useAuth();

  return (
    <div className="flex flex-col items-center">
      <section className="flex min-h-[70vh] flex-col items-center justify-center text-center">
        <Image
          src="/logo.png"
          alt="Zesayro"
          width={96}
          height={96}
          priority
          className="h-24 w-24 rounded-2xl shadow-glass-dark"
        />

        <h1 className="mt-8 max-w-3xl text-5xl font-bold leading-[1.05] tracking-tight text-slate-900 sm:text-6xl dark:text-white">
          Fitness, <span className="text-gradient">personalized</span> by AI.
        </h1>

        <p className="mt-5 max-w-xl text-lg text-slate-600 dark:text-slate-300">
          One place for your plans, nutrition, and progress — guided by a coach
          that actually knows you.
        </p>

        <div className="mt-9 flex flex-wrap items-center justify-center gap-3">
          {user ? (
            <Link href="/dashboard" className="btn-primary px-7 py-3 text-base">
              Open dashboard →
            </Link>
          ) : (
            <>
              <Link href="/register" className="btn-primary px-7 py-3 text-base">
                Get started
              </Link>
              <Link href="/login" className="btn-secondary px-7 py-3 text-base">
                Sign in
              </Link>
            </>
          )}
        </div>

        <div className="mt-14 flex flex-wrap items-center justify-center gap-3">
          {FEATURES.map((f) => (
            <div
              key={f.label}
              className="glass flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium text-slate-700 dark:text-slate-200"
            >
              <f.icon className="h-4 w-4 text-brand-500" />
              {f.label}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
