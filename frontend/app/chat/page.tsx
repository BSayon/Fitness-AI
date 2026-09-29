"use client";

import { useEffect, useRef, useState } from "react";
import { Send } from "lucide-react";
import AuthGate from "@/components/AuthGate";
import Markdown from "@/components/Markdown";
import { useAuth } from "@/lib/auth-context";
import { generateChat, type UserProfile } from "@/lib/api";
import {
  getUserRecord,
  saveChat,
  type ChatMessage,
} from "@/lib/firestore";

export default function ChatPage() {
  return (
    <AuthGate>
      <ChatInner />
    </AuthGate>
  );
}

function ChatInner() {
  const { user } = useAuth();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [history, setHistory] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const listRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!user) return;
    getUserRecord(user.uid).then((rec) => {
      setProfile(rec?.profile ?? null);
      setHistory(rec?.chatHistory ?? []);
    });
  }, [user]);

  useEffect(() => {
    listRef.current?.scrollTo({
      top: listRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [history]);

  async function send() {
    if (!input.trim() || !profile || !user) return;
    const question = input.trim();
    setInput("");
    setError(null);
    const next: ChatMessage[] = [
      ...history,
      { role: "user", content: question, ts: Date.now() },
    ];
    setHistory(next);
    setBusy(true);
    try {
      const res = await generateChat(profile, question);
      const updated: ChatMessage[] = [
        ...next,
        { role: "assistant", content: res.response, ts: Date.now() },
      ];
      setHistory(updated);
      await saveChat(user.uid, updated);
    } catch (err: any) {
      setError(err?.message ?? "Chat failed");
    } finally {
      setBusy(false);
    }
  }

  if (!profile) {
    return (
      <div className="card text-center">
        <h2 className="text-lg font-semibold text-slate-900">
          Complete your profile first
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          The chat coach uses your profile to give tailored advice.
        </p>
      </div>
    );
  }

  return (
    <div className="flex h-[calc(100vh-180px)] flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-100 px-6 py-4">
        <h1 className="text-lg font-semibold text-slate-900">💬 Chat with your AI coach</h1>
        <p className="text-xs text-slate-500">
          Ask about your workout, nutrition, form, recovery — anything fitness.
        </p>
      </div>

      <div ref={listRef} className="flex-1 space-y-4 overflow-y-auto px-6 py-4">
        {history.length === 0 && (
          <p className="text-sm text-slate-500">
            Start the conversation, e.g.{" "}
            <em>&quot;What warm-up should I do before leg day?&quot;</em>
          </p>
        )}
        {history.map((m, i) => (
          <div
            key={i}
            className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm ${
                m.role === "user"
                  ? "bg-brand-500 text-white"
                  : "bg-slate-100 text-slate-800"
              }`}
            >
              {m.role === "user" ? m.content : <Markdown content={m.content} />}
            </div>
          </div>
        ))}
        {busy && (
          <div className="flex justify-start">
            <div className="rounded-2xl bg-slate-100 px-4 py-3 text-sm text-slate-500">
              Thinking…
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="border-t border-red-200 bg-red-50 px-6 py-2 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="border-t border-slate-100 px-4 py-3">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            send();
          }}
          className="flex items-center gap-2"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question…"
            className="input flex-1"
            disabled={busy}
          />
          <button
            type="submit"
            disabled={busy || !input.trim()}
            className="btn-primary !px-4"
          >
            <Send className="h-4 w-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
