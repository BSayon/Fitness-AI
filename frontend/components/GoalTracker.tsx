"use client";

import { useState } from "react";
import {
  Activity,
  CalendarCheck,
  Flame,
  Moon,
  TrendingDown,
  TrendingUp,
  Droplets,
} from "lucide-react";
import { addMetric, type DashboardStats, type MetricLog } from "@/lib/api";

function StatCard({
  icon: Icon,
  label,
  value,
  accent = "text-slate-900 dark:text-slate-100",
}: {
  icon: any;
  label: string;
  value: string;
  accent?: string;
}) {
  return (
    <div className="rounded-xl border border-white/40 bg-white/40 p-3 dark:border-white/10 dark:bg-white/5">
      <div className="flex items-center gap-2 text-xs uppercase text-slate-500 dark:text-slate-400">
        <Icon className="h-3.5 w-3.5" /> {label}
      </div>
      <div className={`mt-1 text-lg font-semibold ${accent}`}>{value}</div>
    </div>
  );
}

function WeightSparkline({ metrics }: { metrics: MetricLog[] }) {
  const points = metrics
    .filter((m) => typeof m.weight === "number")
    .map((m) => ({ date: m.date, weight: m.weight as number }));

  if (points.length < 2) {
    return (
      <p className="text-sm text-slate-500 dark:text-slate-400">
        Log at least two weigh-ins to see your trend.
      </p>
    );
  }

  const w = 480;
  const h = 120;
  const pad = 10;
  const weights = points.map((p) => p.weight);
  const min = Math.min(...weights);
  const max = Math.max(...weights);
  const span = max - min || 1;
  const stepX = (w - pad * 2) / (points.length - 1);

  const coords = points.map((p, i) => {
    const x = pad + i * stepX;
    const y = pad + (1 - (p.weight - min) / span) * (h - pad * 2);
    return [x, y] as const;
  });

  const path = coords
    .map(([x, y], i) => `${i === 0 ? "M" : "L"}${x.toFixed(1)},${y.toFixed(1)}`)
    .join(" ");

  return (
    <div>
      <svg viewBox={`0 0 ${w} ${h}`} className="w-full">
        <polyline
          points={`${pad},${h - pad} ${coords
            .map(([x, y]) => `${x},${y}`)
            .join(" ")} ${w - pad},${h - pad}`}
          fill="rgba(99,102,241,0.08)"
          stroke="none"
        />
        <path d={path} fill="none" stroke="#6366f1" strokeWidth={2.5} />
        {coords.map(([x, y], i) => (
          <circle key={i} cx={x} cy={y} r={3} fill="#6366f1" />
        ))}
      </svg>
      <div className="mt-1 flex justify-between text-xs text-slate-400 dark:text-slate-500">
        <span>{points[0].date}</span>
        <span>
          {min.toFixed(1)}–{max.toFixed(1)} kg
        </span>
        <span>{points[points.length - 1].date}</span>
      </div>
    </div>
  );
}

const today = () => new Date().toISOString().slice(0, 10);

export default function GoalTracker({
  stats,
  metrics,
  onLogged,
}: {
  stats: DashboardStats;
  metrics: MetricLog[];
  onLogged: (metrics: MetricLog[]) => void;
}) {
  const [form, setForm] = useState<MetricLog>({ date: today(), note: "" });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function num(v: string): number | null {
    return v === "" ? null : Number(v);
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      const res = await addMetric(form);
      onLogged(res.metrics);
      setForm({ date: today(), note: "" });
    } catch (err: any) {
      setError(err?.message ?? "Failed to log metrics");
    } finally {
      setSaving(false);
    }
  }

  const weightChange = stats.weightChange ?? 0;
  const recent = [...metrics].reverse().slice(0, 7);

  return (
    <section className="space-y-6">
      <div className="card">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-indigo-500/10 p-2 text-indigo-600">
            <Activity className="h-5 w-5" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
              Health goal tracker
            </h2>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              Goal: <span className="font-medium">{stats.goal ?? "—"}</span>
            </p>
          </div>
        </div>

        <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard
            icon={Flame}
            label="Logging streak"
            value={`${stats.streak ?? 0} day${(stats.streak ?? 0) === 1 ? "" : "s"}`}
            accent="text-amber-600"
          />
          <StatCard
            icon={weightChange <= 0 ? TrendingDown : TrendingUp}
            label="Weight change"
            value={
              stats.weightChange === undefined
                ? "—"
                : `${weightChange > 0 ? "+" : ""}${weightChange} kg`
            }
            accent={weightChange <= 0 ? "text-emerald-600" : "text-slate-900 dark:text-slate-100"}
          />
          <StatCard
            icon={CalendarCheck}
            label="Workouts done"
            value={`${stats.totalWorkouts ?? 0}`}
          />
          <StatCard
            icon={Activity}
            label="Days tracked"
            value={`${stats.daysTracked ?? 0}`}
          />
          <StatCard
            icon={Moon}
            label="Avg sleep"
            value={stats.avgSleep ? `${stats.avgSleep} h` : "—"}
          />
          <StatCard
            icon={Droplets}
            label="Avg water"
            value={stats.avgWater ? `${stats.avgWater} glasses` : "—"}
          />
          <StatCard
            icon={TrendingDown}
            label="Current weight"
            value={stats.latestWeight ? `${stats.latestWeight} kg` : "—"}
          />
          <StatCard
            icon={Activity}
            label="BMI"
            value={stats.bmi ? `${stats.bmi}` : "—"}
          />
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="card">
          <h3 className="section-title">📈 Weight trend</h3>
          <WeightSparkline metrics={metrics} />
        </div>

        <div className="card">
          <h3 className="section-title">📝 Log today</h3>
          <form onSubmit={submit} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="label">Date</label>
                <input
                  type="date"
                  className="input"
                  value={form.date}
                  onChange={(e) => setForm({ ...form, date: e.target.value })}
                />
              </div>
              <div>
                <label className="label">Weight (kg)</label>
                <input
                  type="number"
                  step="0.1"
                  className="input"
                  value={form.weight ?? ""}
                  onChange={(e) =>
                    setForm({ ...form, weight: num(e.target.value) })
                  }
                />
              </div>
              <div>
                <label className="label">Water (glasses)</label>
                <input
                  type="number"
                  className="input"
                  value={form.water_glasses ?? ""}
                  onChange={(e) =>
                    setForm({ ...form, water_glasses: num(e.target.value) })
                  }
                />
              </div>
              <div>
                <label className="label">Sleep (hrs)</label>
                <input
                  type="number"
                  step="0.1"
                  className="input"
                  value={form.sleep_hours ?? ""}
                  onChange={(e) =>
                    setForm({ ...form, sleep_hours: num(e.target.value) })
                  }
                />
              </div>
              <div>
                <label className="label">Workouts done</label>
                <input
                  type="number"
                  className="input"
                  value={form.workouts_completed ?? ""}
                  onChange={(e) =>
                    setForm({ ...form, workouts_completed: num(e.target.value) })
                  }
                />
              </div>
              <div>
                <label className="label">Calories</label>
                <input
                  type="number"
                  className="input"
                  value={form.calories ?? ""}
                  onChange={(e) =>
                    setForm({ ...form, calories: num(e.target.value) })
                  }
                />
              </div>
            </div>
            <div>
              <label className="label">Note</label>
              <input
                className="input"
                placeholder="How did today go?"
                value={form.note ?? ""}
                onChange={(e) => setForm({ ...form, note: e.target.value })}
              />
            </div>
            {error && (
              <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 dark:bg-red-950/40 dark:text-red-300">
                {error}
              </p>
            )}
            <button type="submit" className="btn-primary w-full" disabled={saving}>
              {saving ? "Saving…" : "Log entry"}
            </button>
          </form>
        </div>
      </div>

      {recent.length > 0 && (
        <div className="card overflow-x-auto">
          <h3 className="section-title">🗓️ Recent logs</h3>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase text-slate-500 dark:text-slate-400">
                <th className="py-2 pr-4">Date</th>
                <th className="py-2 pr-4">Weight</th>
                <th className="py-2 pr-4">Water</th>
                <th className="py-2 pr-4">Sleep</th>
                <th className="py-2 pr-4">Workouts</th>
                <th className="py-2 pr-4">Calories</th>
                <th className="py-2">Note</th>
              </tr>
            </thead>
            <tbody>
              {recent.map((m) => (
                <tr key={m.date} className="border-t border-slate-100 dark:border-slate-700">
                  <td className="py-2 pr-4 font-medium text-slate-700 dark:text-slate-200">{m.date}</td>
                  <td className="py-2 pr-4">{m.weight ?? "—"}</td>
                  <td className="py-2 pr-4">{m.water_glasses ?? "—"}</td>
                  <td className="py-2 pr-4">{m.sleep_hours ?? "—"}</td>
                  <td className="py-2 pr-4">{m.workouts_completed ?? "—"}</td>
                  <td className="py-2 pr-4">{m.calories ?? "—"}</td>
                  <td className="py-2 text-slate-500 dark:text-slate-400">{m.note || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
