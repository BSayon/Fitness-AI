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

// --------------------------------------------------------------------------- //
// Types
// --------------------------------------------------------------------------- //
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

export type MetricLog = {
  date: string;
  weight?: number | null;
  water_glasses?: number | null;
  sleep_hours?: number | null;
  workouts_completed?: number | null;
  calories?: number | null;
  note?: string;
};

export type DashboardStats = {
  bmi?: number | null;
  goal?: string;
  startingWeight?: number;
  latestWeight?: number;
  weightChange?: number;
  totalWorkouts?: number;
  daysTracked?: number;
  avgSleep?: number;
  avgWater?: number;
  streak?: number;
};

export type DashboardData = {
  profile: UserProfile | null;
  workoutPlan: string | null;
  nutritionPlan: string | null;
  metrics: MetricLog[];
  stats: DashboardStats;
};

export type ChatMessage = { role: "user" | "assistant"; content: string; ts: number };

export type GenerateResponse = { response: string; session_id: string };

// --------------------------------------------------------------------------- //
// Identity & profile
// --------------------------------------------------------------------------- //
export function getMe() {
  return authedFetch("/api/me") as Promise<{
    uid: string;
    email?: string;
    name?: string;
    picture?: string;
  }>;
}

export function getProfile() {
  return authedFetch("/api/profile") as Promise<{ profile: UserProfile | null }>;
}

export function saveProfile(profile: UserProfile) {
  return authedFetch("/api/profile", {
    method: "POST",
    body: JSON.stringify({ profile }),
  }) as Promise<{ ok: boolean; profile: UserProfile }>;
}

// --------------------------------------------------------------------------- //
// Plans & chat (persisted server-side)
// --------------------------------------------------------------------------- //
export function generateWorkout(profile?: UserProfile) {
  return authedFetch("/api/workout", {
    method: "POST",
    body: JSON.stringify(profile ? { profile } : {}),
  }) as Promise<GenerateResponse>;
}

export function generateNutrition(profile?: UserProfile) {
  return authedFetch("/api/nutrition", {
    method: "POST",
    body: JSON.stringify(profile ? { profile } : {}),
  }) as Promise<GenerateResponse>;
}

export function sendChat(message: string, profile?: UserProfile) {
  return authedFetch("/api/chat", {
    method: "POST",
    body: JSON.stringify(profile ? { profile, message } : { message }),
  }) as Promise<GenerateResponse>;
}

export function getChatHistory() {
  return authedFetch("/api/chat/history") as Promise<{ chatHistory: ChatMessage[] }>;
}

// --------------------------------------------------------------------------- //
// Health-goal tracking & dashboard
// --------------------------------------------------------------------------- //
export function getDashboard() {
  return authedFetch("/api/dashboard") as Promise<DashboardData>;
}

export function listMetrics() {
  return authedFetch("/api/metrics") as Promise<{ metrics: MetricLog[] }>;
}

export function addMetric(entry: MetricLog) {
  return authedFetch("/api/metrics", {
    method: "POST",
    body: JSON.stringify(entry),
  }) as Promise<{ ok: boolean; metrics: MetricLog[] }>;
}
