"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AuthGate from "@/components/AuthGate";
import ProfileForm, { EMPTY_PROFILE } from "@/components/ProfileForm";
import { getProfile, saveProfile, type UserProfile } from "@/lib/api";

export default function ProfilePage() {
  return (
    <AuthGate>
      <ProfileInner />
    </AuthGate>
  );
}

function ProfileInner() {
  const router = useRouter();
  const [initial, setInitial] = useState<UserProfile | null>(null);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    getProfile()
      .then((res) => setInitial(res.profile ?? EMPTY_PROFILE))
      .catch(() => setInitial(EMPTY_PROFILE));
  }, []);

  async function handleSave(profile: UserProfile) {
    setSaving(true);
    setNotice(null);
    try {
      await saveProfile(profile);
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
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Your profile</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          The more accurate this is, the better your AI coach can tailor advice.
        </p>
      </div>
      {notice && (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm text-emerald-700 dark:border-emerald-900/50 dark:bg-emerald-950/40 dark:text-emerald-300">
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
        <div className="text-slate-500 dark:text-slate-400">Loading…</div>
      )}
    </div>
  );
}
