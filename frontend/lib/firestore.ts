import {
  doc,
  getDoc,
  setDoc,
  updateDoc,
  serverTimestamp,
} from "firebase/firestore";
import { db } from "./firebase";
import type { UserProfile } from "./api";

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  ts: number;
};

export type UserRecord = {
  email?: string;
  name?: string;
  profile?: UserProfile;
  workoutPlan?: string;
  nutritionPlan?: string;
  chatHistory?: ChatMessage[];
};

const userRef = (uid: string) => doc(db, "users", uid);

export async function getUserRecord(uid: string): Promise<UserRecord | null> {
  const snap = await getDoc(userRef(uid));
  return snap.exists() ? (snap.data() as UserRecord) : null;
}

export async function saveProfile(uid: string, profile: UserProfile) {
  await setDoc(
    userRef(uid),
    { profile, updatedAt: serverTimestamp() },
    { merge: true },
  );
}

export async function savePlan(
  uid: string,
  kind: "workoutPlan" | "nutritionPlan",
  content: string,
) {
  await updateDoc(userRef(uid), {
    [kind]: content,
    updatedAt: serverTimestamp(),
  });
}

export async function saveChat(uid: string, history: ChatMessage[]) {
  await updateDoc(userRef(uid), {
    chatHistory: history,
    updatedAt: serverTimestamp(),
  });
}
