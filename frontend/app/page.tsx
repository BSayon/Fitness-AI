"use client";

import Link from "next/link";
import { Dumbbell, Salad, MessageCircle, Sparkles } from "lucide-react";
import { useAuth } from "@/lib/auth-context";

export default function LandingPage() {
  const { user } = useAuth();

  return (
    <div className="space-y-12">
      <section className="relative overflow-hidden rounded-3xl bg-gradient-brand px-8 py-16 text-white shadow-xl">
        <div className="absolute -right-16 -top-16 h-64 w-64 rounded-full bg-white/10 blur-3xl" />
        <div className="absolute -bottom-16 -left-16 h-64 w-64 rounded-full bg-white/10 blur-3xl" />
        <div className="relative">
          <span className="inline-flex items-center gap-2 rounded-full bg-white/20 px-3 py-1 text-xs font-semibold uppercase tracking-wide backdrop-blur">
            <Sparkles className="h-3.5 w-3.5" /> Powered by Groq LLMs
          </span>
          <h1 className="mt-4 max-w-3xl text-4xl font-bold leading-tight sm:text-5xl">
            Your personalized AI fitness &amp; nutrition coach.
          </h1>
          <p className="mt-4 max-w-2xl text-lg text-white/90">
            Build a plan tailored to your goals, schedule, and dietary needs.
            Track your progress and chat with an evidence-based coach 24/7.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            {user ? (
              <Link
                href="/dashboard"
                className="rounded-xl bg-white px-6 py-3 text-sm font-semibold text-brand-600 shadow-md transition hover:bg-slate-100"
              >
                Go to Dashboard →
              </Link>
            ) : (
              <>
                <Link
                  href="/register"
                  className="rounded-xl bg-white px-6 py-3 text-sm font-semibold text-brand-600 shadow-md transition hover:bg-slate-100"
                >
                  Get Started Free
                </Link>
                <Link
                  href="/login"
                  className="rounded-xl border border-white/40 px-6 py-3 text-sm font-semibold text-white transition hover:bg-white/10"
                >
                  Sign In
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        {[
          {
            icon: Dumbbell,
            title: "Custom Workout Plans",
            body: "Weekly programming built around your goals, schedule, equipment, and fitness level.",
          },
          {
            icon: Salad,
            title: "Nutrition Guidance",
            body: "Macro targets and meal ideas that respect your preferences, allergies, and health conditions.",
          },
          {
            icon: MessageCircle,
            title: "AI Chat Coach",
            body: "Ask follow-up questions, adjust programs, and get evidence-based answers on demand.",
          },
        ].map((f) => (
          <div key={f.title} className="card">
            <div className="mb-4 inline-flex h-11 w-11 items-center justify-center rounded-xl bg-brand-500/10 text-brand-600">
              <f.icon className="h-5 w-5" />
            </div>
            <h3 className="text-lg font-semibold text-slate-900">{f.title}</h3>
            <p className="mt-2 text-sm text-slate-600">{f.body}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
