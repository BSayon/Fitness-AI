import { auth } from "./firebase";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ??
  "http://localhost:8000";

async function authedFetch(path: string, init: RequestInit = {}) {
  const user = auth.currentUser;
  if (!user) throw new Error("Not signed in");
  const token = await user.getIdToken();

  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...(init.headers ?? {}),
    },
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const data = await res.json();
      detail = data.detail ?? detail;
    } catch {
      /* ignore */
    }
    throw new Error(`Request failed (${res.status}): ${detail}`);
  }
  return res.json();
}

export type UserProfile = {
  name?: string;
  age: number;
  weight: number;
  height: number;
  gender: string;
  workout_preference: string[];
  workout_time: string;
  fitness_level: string;
  fitness_goal: string;
  schedule: Record<string, string>;
  food_preferences: string[];
  allergies: string;
  health_issues: string;
  medications: string;
  water_intake: number;
  sleep_hours: number;
  timestamp?: string;
};

export type GenerateResponse = { response: string; session_id: string };

export function generateWorkout(profile: UserProfile) {
  return authedFetch("/api/workout", {
    method: "POST",
    body: JSON.stringify({ profile }),
  }) as Promise<GenerateResponse>;
}

export function generateNutrition(profile: UserProfile) {
  return authedFetch("/api/nutrition", {
    method: "POST",
    body: JSON.stringify({ profile }),
  }) as Promise<GenerateResponse>;
}

export function generateChat(profile: UserProfile, message: string) {
  return authedFetch("/api/chat", {
    method: "POST",
    body: JSON.stringify({ profile, message }),
  }) as Promise<GenerateResponse>;
}
