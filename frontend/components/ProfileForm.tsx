"use client";

import { useEffect, useState } from "react";
import type { UserProfile } from "@/lib/api";

const DAYS = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
];
const TIME_SLOTS = [
  "Morning (6-10 AM)",
  "Afternoon (12-4 PM)",
  "Evening (5-8 PM)",
  "Night (8-10 PM)",
];
const WORKOUT_OPTIONS = [
  "Cardio",
  "Strength Training",
  "Yoga",
  "Pilates",
  "HIIT",
  "CrossFit",
  "Swimming",
  "Running",
  "Cycling",
  "Dancing",
];
const FOOD_OPTIONS = [
  "Vegetarian",
  "Vegan",
  "Pescatarian",
  "Keto",
  "Paleo",
  "Mediterranean",
  "Low-carb",
  "High-protein",
  "Gluten-free",
  "No restrictions",
];

export const EMPTY_PROFILE: UserProfile = {
  age: 25,
  weight: 70,
  height: 170,
  gender: "Male",
  workout_preference: ["Cardio", "Strength Training"],
  workout_time: "30-45 minutes",
  fitness_level: "Beginner",
  fitness_goal: "General Health",
  schedule: Object.fromEntries(DAYS.map((d) => [d, "Not Available"])),
  food_preferences: ["No restrictions"],
  allergies: "",
  health_issues: "",
  medications: "",
  water_intake: 8,
  sleep_hours: 7,
};

function Chips({
  options,
  value,
  onChange,
}: {
  options: string[];
  value: string[];
  onChange: (v: string[]) => void;
}) {
  return (
    <div className="flex flex-wrap gap-2">
      {options.map((opt) => {
        const active = value.includes(opt);
        return (
          <button
            type="button"
            key={opt}
            onClick={() =>
              onChange(
                active ? value.filter((v) => v !== opt) : [...value, opt]
              )
            }
            className={`rounded-full border px-3 py-1 text-xs font-medium transition ${
              active
                ? "border-brand-500 bg-brand-500 text-white"
                : "border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
            }`}
          >
            {opt}
          </button>
        );
      })}
    </div>
  );
}

export default function ProfileForm({
  initial,
  onSubmit,
  submitting,
  submitLabel = "Save profile",
}: {
  initial?: UserProfile | null;
  onSubmit: (profile: UserProfile) => void | Promise<void>;
  submitting?: boolean;
  submitLabel?: string;
}) {
  const [p, setP] = useState<UserProfile>(initial ?? EMPTY_PROFILE);

  useEffect(() => {
    if (initial) setP(initial);
  }, [initial]);

  function set<K extends keyof UserProfile>(key: K, val: UserProfile[K]) {
    setP((prev) => ({ ...prev, [key]: val }));
  }

  const bmi = p.weight / Math.pow(p.height / 100, 2);

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit({ ...p, timestamp: new Date().toISOString() });
      }}
      className="space-y-8"
    >
      <div className="card">
        <h2 className="section-title">👤 Personal details</h2>
        <div className="grid gap-4 md:grid-cols-4">
          <div>
            <label className="label">Age</label>
            <input
              type="number"
              min={13}
              max={100}
              className="input"
              value={p.age}
              onChange={(e) => set("age", Number(e.target.value))}
            />
          </div>
          <div>
            <label className="label">Weight (kg)</label>
            <input
              type="number"
              step="0.1"
              className="input"
              value={p.weight}
              onChange={(e) => set("weight", Number(e.target.value))}
            />
          </div>
          <div>
            <label className="label">Height (cm)</label>
            <input
              type="number"
              step="0.1"
              className="input"
              value={p.height}
              onChange={(e) => set("height", Number(e.target.value))}
            />
          </div>
          <div>
            <label className="label">Gender</label>
            <select
              className="input"
              value={p.gender}
              onChange={(e) => set("gender", e.target.value)}
            >
              {["Male", "Female", "Other", "Prefer not to say"].map((v) => (
                <option key={v}>{v}</option>
              ))}
            </select>
          </div>
        </div>
        <p className="mt-3 text-xs text-slate-500">
          Computed BMI: <span className="font-semibold">{bmi.toFixed(1)}</span>
        </p>
      </div>

      <div className="card">
        <h2 className="section-title">🏋️ Workout preferences</h2>
        <div className="grid gap-4 md:grid-cols-3">
          <div>
            <label className="label">Fitness level</label>
            <select
              className="input"
              value={p.fitness_level}
              onChange={(e) => set("fitness_level", e.target.value)}
            >
              {["Beginner", "Intermediate", "Advanced"].map((v) => (
                <option key={v}>{v}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="label">Primary goal</label>
            <select
              className="input"
              value={p.fitness_goal}
              onChange={(e) => set("fitness_goal", e.target.value)}
            >
              {[
                "Weight Loss",
                "Muscle Gain",
                "Endurance",
                "Strength",
                "Flexibility",
                "General Health",
              ].map((v) => (
                <option key={v}>{v}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="label">Session duration</label>
            <select
              className="input"
              value={p.workout_time}
              onChange={(e) => set("workout_time", e.target.value)}
            >
              {[
                "15-30 minutes",
                "30-45 minutes",
                "45-60 minutes",
                "60-90 minutes",
                "90+ minutes",
              ].map((v) => (
                <option key={v}>{v}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="mt-4">
          <label className="label">Favorite activities</label>
          <Chips
            options={WORKOUT_OPTIONS}
            value={p.workout_preference}
            onChange={(v) => set("workout_preference", v)}
          />
        </div>
      </div>

      <div className="card">
        <h2 className="section-title">📅 Weekly schedule</h2>
        <div className="grid gap-3 md:grid-cols-7">
          {DAYS.map((day) => {
            const val = p.schedule[day] ?? "Not Available";
            const available = val !== "Not Available";
            return (
              <div key={day} className="rounded-xl border border-slate-200 p-3">
                <label className="flex items-center gap-2 text-sm font-medium text-slate-700">
                  <input
                    type="checkbox"
                    checked={available}
                    onChange={(e) =>
                      set("schedule", {
                        ...p.schedule,
                        [day]: e.target.checked ? TIME_SLOTS[0] : "Not Available",
                      })
                    }
                  />
                  {day.slice(0, 3)}
                </label>
                {available && (
                  <select
                    className="input mt-2 !py-1 !text-xs"
                    value={val}
                    onChange={(e) =>
                      set("schedule", { ...p.schedule, [day]: e.target.value })
                    }
                  >
                    {TIME_SLOTS.map((s) => (
                      <option key={s}>{s}</option>
                    ))}
                  </select>
                )}
              </div>
            );
          })}
        </div>
      </div>

      <div className="card">
        <h2 className="section-title">🍽️ Dietary preferences &amp; health</h2>
        <label className="label">Dietary preferences</label>
        <Chips
          options={FOOD_OPTIONS}
          value={p.food_preferences}
          onChange={(v) => set("food_preferences", v)}
        />
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <div>
            <label className="label">Allergies / intolerances</label>
            <textarea
              className="input h-20"
              value={p.allergies}
              onChange={(e) => set("allergies", e.target.value)}
              placeholder="e.g. nuts, dairy, shellfish"
            />
          </div>
          <div>
            <label className="label">Health issues / conditions</label>
            <textarea
              className="input h-20"
              value={p.health_issues}
              onChange={(e) => set("health_issues", e.target.value)}
              placeholder="e.g. hypertension, joint pain"
            />
          </div>
          <div>
            <label className="label">Current medications</label>
            <textarea
              className="input h-20"
              value={p.medications}
              onChange={(e) => set("medications", e.target.value)}
              placeholder="Any medications affecting exercise or diet"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Water (glasses/day): {p.water_intake}</label>
              <input
                type="range"
                min={1}
                max={15}
                value={p.water_intake}
                onChange={(e) => set("water_intake", Number(e.target.value))}
                className="w-full accent-brand-500"
              />
            </div>
            <div>
              <label className="label">Sleep (hrs): {p.sleep_hours}</label>
              <input
                type="range"
                min={4}
                max={12}
                value={p.sleep_hours}
                onChange={(e) => set("sleep_hours", Number(e.target.value))}
                className="w-full accent-brand-500"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-end">
        <button type="submit" className="btn-primary" disabled={submitting}>
          {submitting ? "Saving…" : submitLabel}
        </button>
      </div>
    </form>
  );
}
