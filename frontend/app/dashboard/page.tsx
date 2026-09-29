"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Dumbbell, Salad, Download, Sparkles } from "lucide-react";
import AuthGate from "@/components/AuthGate";
import Markdown from "@/components/Markdown";
import { useAuth } from "@/lib/auth-context";
import {
  getUserRecord,
  savePlan,
  type UserRecord,
} from "@/lib/firestore";
import {
  generateNutrition,
  generateWorkout,
  type UserProfile,
} from "@/lib/api";

export default function DashboardPage() {
  return (
    <AuthGate>
      <DashboardInner />
    </AuthGate>
  );
}

function bmiCategory(bmi: number) {
  if (bmi < 18.5) return { label: "Underweight", color: "text-blue-600" };
  if (bmi < 25) return { label: "Normal", color: "text-emerald-600" };
  if (bmi < 30) return { label: "Overweight", color: "text-amber-600" };
  return { label: "Obese", color: "text-red-600" };
}

function downloadText(name: string, content: string) {
  const blob = new Blob([content], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  URL.revokeObjectURL(url);
}

function DashboardInner() {
  const { user } = useAuth();
  const [record, setRecord] = useState<UserRecord | null>(null);
  const [loadingWorkout, setLoadingWorkout] = useState(false);
  const [loadingNutrition, setLoadingNutrition] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    getUserRecord(user.uid).then(setRecord);
  }, [user]);

  const profile: UserProfile | undefined = record?.profile;

  async function handleGenerate(kind: "workout" | "nutrition") {
    if (!user || !profile) return;
    setError(null);
    if (kind === "workout") setLoadingWorkout(true);
    else setLoadingNutrition(true);
    try {
      const res =
        kind === "workout"
          ? await generateWorkout(profile)
          : await generateNutrition(profile);
      await savePlan(
        user.uid,
        kind === "workout" ? "workoutPlan" : "nutritionPlan",
        res.response
      );
      setRecord((prev) =>
        prev
          ? {
              ...prev,
              ...(kind === "workout"
                ? { workoutPlan: res.response }
                : { nutritionPlan: res.response }),
            }
          : prev
      );
    } catch (err: any) {
      setError(err?.message ?? "Failed to generate plan");
    } finally {
      setLoadingWorkout(false);
      setLoadingNutrition(false);
    }
  }

  if (!record) {
    return <div className="text-slate-500">Loading…</div>;
  }

  if (!profile) {
    return (
      <div className="card text-center">
        <Sparkles className="mx-auto h-8 w-8 text-brand-500" />
        <h2 className="mt-3 text-xl font-semibold text-slate-900">
          Let&apos;s get started
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          Fill in your profile so we can build a plan tailored to you.
        </p>
        <Link href="/profile" className="btn-primary mt-4">
          Complete profile →
        </Link>
      </div>
    );
  }

  const bmi = profile.weight / Math.pow(profile.height / 100, 2);
  const cat = bmiCategory(bmi);
  const availableDays = Object.values(profile.schedule).filter(
    (v) => v !== "Not Available"
  ).length;

  return (
    <div className="space-y-8">
      <section className="card">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">
              Hi {user?.displayName ?? "there"} 👋
            </h1>
            <p className="text-sm text-slate-500">
              Here&apos;s a snapshot of your fitness profile.
            </p>
          </div>
          <Link href="/profile" className="btn-secondary">
            Edit profile
          </Link>
        </div>

        <div className="mt-6 grid gap-4 sm:grid-cols-2 md:grid-cols-4">
          {[
            { label: "Age", value: `${profile.age} yrs` },
            { label: "Weight", value: `${profile.weight} kg` },
            { label: "Height", value: `${profile.height} cm` },
            {
              label: "BMI",
              value: (
                <span className={cat.color}>
                  {bmi.toFixed(1)} · {cat.label}
                </span>
              ),
            },
            { label: "Level", value: profile.fitness_level },
            { label: "Goal", value: profile.fitness_goal },
            { label: "Days/wk", value: `${availableDays}/7` },
            { label: "Water", value: `${profile.water_intake} glasses` },
          ].map((s) => (
            <div
              key={s.label}
              className="rounded-xl border border-slate-100 bg-slate-50 p-3"
            >
              <div className="text-xs uppercase text-slate-500">{s.label}</div>
              <div className="mt-1 text-lg font-semibold text-slate-900">
                {s.value}
              </div>
            </div>
          ))}
        </div>
      </section>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      <section className="grid gap-6 md:grid-cols-2">
        <div className="card">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-brand-500/10 p-2 text-brand-600">
                <Dumbbell className="h-5 w-5" />
              </div>
              <h2 className="text-lg font-semibold text-slate-900">
                Workout plan
              </h2>
            </div>
            <button
              onClick={() => handleGenerate("workout")}
              disabled={loadingWorkout}
              className="btn-primary !py-1.5 !px-3"
            >
              {loadingWorkout
                ? "Generating…"
                : record.workoutPlan
                ? "Regenerate"
                : "Generate"}
            </button>
          </div>
          <div className="mt-4 max-h-[500px] overflow-auto">
            {record.workoutPlan ? (
              <>
                <Markdown content={record.workoutPlan} />
                <button
                  onClick={() =>
                    downloadText("workout_plan.md", record.workoutPlan!)
                  }
                  className="btn-secondary mt-4 !py-1.5 !px-3"
                >
                  <Download className="h-4 w-4" /> Download
                </button>
              </>
            ) : (
              <p className="text-sm text-slate-500">
                No plan yet — generate one to get started.
              </p>
            )}
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-emerald-500/10 p-2 text-emerald-600">
                <Salad className="h-5 w-5" />
              </div>
              <h2 className="text-lg font-semibold text-slate-900">
                Nutrition plan
              </h2>
            </div>
            <button
              onClick={() => handleGenerate("nutrition")}
              disabled={loadingNutrition}
              className="btn-primary !py-1.5 !px-3"
            >
              {loadingNutrition
                ? "Generating…"
                : record.nutritionPlan
                ? "Regenerate"
                : "Generate"}
            </button>
          </div>
          <div className="mt-4 max-h-[500px] overflow-auto">
            {record.nutritionPlan ? (
              <>
                <Markdown content={record.nutritionPlan} />
                <button
                  onClick={() =>
                    downloadText("nutrition_plan.md", record.nutritionPlan!)
                  }
                  className="btn-secondary mt-4 !py-1.5 !px-3"
                >
                  <Download className="h-4 w-4" /> Download
                </button>
              </>
            ) : (
              <p className="text-sm text-slate-500">
                No plan yet — generate one to get personalized guidance.
              </p>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
