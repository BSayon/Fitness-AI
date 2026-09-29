"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AuthGate from "@/components/AuthGate";
import ProfileForm, { EMPTY_PROFILE } from "@/components/ProfileForm";
import { useAuth } from "@/lib/auth-context";
import { getUserRecord, saveProfile } from "@/lib/firestore";
import type { UserProfile } from "@/lib/api";

export default function ProfilePage() {
  return (
    <AuthGate>
      <ProfileInner />
    </AuthGate>
  );
}

function ProfileInner() {
  const { user } = useAuth();
  const router = useRouter();
  const [initial, setInitial] = useState<UserProfile | null>(null);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    getUserRecord(user.uid).then((rec) => {
      setInitial(rec?.profile ?? EMPTY_PROFILE);
    });
  }, [user]);

  async function handleSave(profile: UserProfile) {
    if (!user) return;
    setSaving(true);
    setNotice(null);
    try {
      await saveProfile(user.uid, profile);
      setNotice("Profile saved successfully.");
      setTimeout(() => router.push("/dashboard"), 600);
    } catch (err: any) {
      setNotice(err?.message ?? "Failed to save profile");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Your profile</h1>
        <p className="text-sm text-slate-500">
          The more accurate this is, the better your AI coach can tailor advice.
        </p>
      </div>
      {notice && (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm text-emerald-700">
          {notice}
        </div>
      )}
      {initial ? (
        <ProfileForm
          initial={initial}
          onSubmit={handleSave}
          submitting={saving}
          submitLabel="Save profile"
        />
      ) : (
        <div className="text-slate-500">Loading…</div>
      )}
    </div>
  );
}
