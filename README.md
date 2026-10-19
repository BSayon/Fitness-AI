---
title: Zesayro
emoji: ⚡
colorFrom: green
colorTo: blue
sdk: docker
app_port: 8000
tags:
  - nextjs
  - fastapi
  - firebase
pinned: false
short_description: Zesayro — AI fitness & nutrition coach (Next.js + FastAPI + Firebase)
---

# ⚡ Zesayro

Full-stack app where a user signs in with **Google Firebase Auth**, fills in a
detailed fitness profile, and then gets:

- an AI-generated **workout plan**,
- an AI-generated **nutrition / diet plan**,
- a conversational **AI coach**, and
- a **health-goal tracking dashboard** (log weight/water/sleep/workouts and see
  progress, streaks, and trends).

All plan generation and chat run through the LangChain agent in
[`src/agents/agent.py`](src/agents/agent.py). The user's record (profile, plans,
chat history, and metric logs) is created and updated **by the backend** using
the **Firebase Cloud Firestore Admin APIs**.

```
┌────────────────┐   Firebase ID token    ┌─────────────────────────┐
│  Next.js (UI)  │ ─────────────────────▶ │  FastAPI backend        │
│   on Vercel    │ ◀───────────────────── │  • verifies ID token    │
└──────┬─────────┘   JSON responses       │  • src/ LangChain agent │
       │ Google sign-in                   │  • Firestore Admin SDK  │
       ▼                                   └───────────┬─────────────┘
  Firebase Auth                                        │ reads / writes
                                                        ▼
                                              Firestore  users/{uid}
                                      { profile, workoutPlan,
                                        nutritionPlan, chatHistory, metrics }
```

> Unlike a typical client-only Firebase app, the **frontend never writes to
> Firestore directly** — every read/write goes through the authenticated
> backend, which uses the Firebase Admin SDK. This is what satisfies
> "the application creates a record for the user using the Firestore APIs".

## Project layout

```
Fitness-AI/
├── src/                      # Shared AI engine ("agent folder")
│   ├── agents/agent.py       # create_agent(...) + in-memory checkpointer
│   ├── model/model.py        # ChatGroq (openai/gpt-oss-120b)
│   ├── prompts/prompt.py     # system prompt + profile/workout/nutrition/chat templates
│   └── service/service.py    # prompt building + agent invocation
├── backend/                  # FastAPI (imports src/)
│   └── app/
│       ├── main.py           # endpoints: profile, workout, nutrition, chat, metrics, dashboard
│       ├── firebase.py       # Admin init + verify_token + Firestore client
│       ├── service.py        # thin adapter over src/service
│       └── models.py         # Pydantic models (UserProfile, MetricLog, ...)
├── frontend/                 # Next.js 14 (App Router) + Tailwind
│   ├── app/                  # / , /login, /register, /profile, /dashboard, /chat
│   ├── components/           # Navbar, ProfileForm, GoalTracker, Markdown, AuthGate
│   └── lib/                  # firebase.ts, auth-context.tsx, api.ts
├── pyproject.toml            # Python deps (source of truth) + uv.lock
├── firestore.rules           # per-user access rules
├── Dockerfile.vercel         # backend image (uv + pyproject/uv.lock, ships src/ + backend/)
├── main.py                   # local launcher: `uv run python main.py`
└── .env                      # single shared env for frontend + backend (gitignored)
```

---

## 1. Prerequisites

- **Python** managed with [`uv`](https://docs.astral.sh/uv/) (the repo uses a
  `uv` virtual env). `pip`/`venv` also works.
- **Node.js 18+** and npm (for the Next.js frontend).
- A **Firebase project** and a **Groq API key**.

## 2. Firebase setup

1. Create a project at <https://console.firebase.google.com>.
2. **Authentication → Sign-in method:** enable **Google** (and optionally
   **Email/Password**).
3. **Firestore Database:** create a database.
4. **Rules:** paste [firestore.rules](firestore.rules) into
   Firebase Console → Firestore → Rules → Publish.
5. **Project settings → Your apps → Web app:** copy the config values (used for
   the `NEXT_PUBLIC_FIREBASE_*` vars below).
6. **Project settings → Service accounts → Generate new private key:** download
   the JSON. You'll copy three fields from it (`project_id`, `client_email`,
   `private_key`) into the `.env` below — no need to keep the JSON file.

## 3. One shared `.env` (frontend + backend)

Create a **single `.env` file at the repository root**. The backend loads it
directly, and the frontend loads it too (via `frontend/next.config.js`), so you
maintain only one file:

```dotenv
# ---- Backend / shared ----
GROQ_API_KEY=your_groq_api_key_here
ALLOWED_ORIGINS=http://localhost:3000

# ---- Firebase Admin (backend) — split from the service-account JSON ----
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-project-id.iam.gserviceaccount.com
# Paste the private_key value from the JSON, keeping the \n sequences, in quotes:
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIE...\n-----END PRIVATE KEY-----\n"

# ---- Firebase Web config (frontend, must be NEXT_PUBLIC_*) ----
NEXT_PUBLIC_FIREBASE_API_KEY=...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project-id.firebasestorage.app
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=...
NEXT_PUBLIC_FIREBASE_APP_ID=...
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Notes:

- `FIREBASE_PROJECT_ID` / `FIREBASE_CLIENT_EMAIL` / `FIREBASE_PRIVATE_KEY` map to
  the `project_id` / `client_email` / `private_key` fields in the service-account
  JSON. Optional: `FIREBASE_PRIVATE_KEY_ID`, `FIREBASE_CLIENT_ID`.
- Keep the whole `private_key` on one line with literal `\n`; the backend
  converts them back to real newlines.
- Do **not** keep a separate `frontend/.env.local` — delete it so the single
  root `.env` is the only source of truth.
- Legacy fallbacks still work if you prefer them: `GOOGLE_APPLICATION_CREDENTIALS`
  (path to a JSON file) or `FIREBASE_SERVICE_ACCOUNT_JSON` (full JSON inline).

### Run the backend (local, no Docker)

```powershell
# from the repo root
uv sync                       # install deps into the uv env (first time only)
uv run python main.py         # → http://127.0.0.1:8000  (auto-reload)
# or explicitly:
# uv run uvicorn backend.app.main:app --reload --port 8000
```

Smoke test:

```powershell
curl http://127.0.0.1:8000/health          # {"status":"ok"}
```

Interactive API docs: <http://127.0.0.1:8000/docs>.
(Every `/api/*` route except `/health` requires a Firebase ID token.)

### Run the frontend

```powershell
cd frontend
npm install        # first time only
npm run dev        # → http://localhost:3000 (reads the root .env)
```

## 5. End-to-end local test (two terminals)

```powershell
# Terminal 1 — backend
uv run python main.py

# Terminal 2 — frontend
cd frontend; npm run dev
```

Then in the browser at <http://localhost:3000>:

1. Click **Sign in** → **Continue with Google** (or register with email).
2. You're redirected to **Profile** — fill in age, gender, weight, height,
   fitness level/goal, activities, weekly schedule, diet, allergies, health
   issues, medications, water, and sleep → **Save profile**.
   → The backend writes `users/{uid}.profile` to Firestore (check the Firestore
   console to confirm the record was created).
3. On the **Dashboard**:
   - **Generate** a workout plan and a nutrition plan (calls the `src` agent;
     results are saved to Firestore).
   - Use the **Health goal tracker** to log today's weight/water/sleep/workouts
     and watch the streak, weight trend, and averages update.
4. Open **Chat Coach** and ask a question — replies are generated by the agent
   and the conversation is persisted.

> If generation returns a `502 LLM error … Invalid API Key`, your
> `GROQ_API_KEY` is missing or invalid — fix it in the root `.env` (or
> `src/.env`) and restart the backend.

---

## 6. Run the backend in Docker (optional, local)

The image is built with **uv** from `pyproject.toml` + `uv.lock`, from the
**repo root** so `src/` is included:

```powershell
docker build -f Dockerfile.vercel -t zesayro-backend .

# Pass the backend env vars (loaded from your root .env, or set inline):
docker run --rm -p 8000:8000 `
  -e GROQ_API_KEY=$env:GROQ_API_KEY `
  -e FIREBASE_PROJECT_ID=$env:FIREBASE_PROJECT_ID `
  -e FIREBASE_CLIENT_EMAIL=$env:FIREBASE_CLIENT_EMAIL `
  -e FIREBASE_PRIVATE_KEY=$env:FIREBASE_PRIVATE_KEY `
  -e ALLOWED_ORIGINS=http://localhost:3000 `
  zesayro-backend
```

> Tip: `docker run --env-file .env ...` loads everything at once. Note that
> `--env-file` does not support quoted multi-line values, so keep
> `FIREBASE_PRIVATE_KEY` on one line with literal `\n` sequences (the backend
> converts them back to newlines).

## 7. Deployment

**Frontend → Vercel**

1. Push the repo to GitHub and import it in Vercel.
2. Set **Root Directory** to `frontend`.
3. Add every `NEXT_PUBLIC_*` env var, and set `NEXT_PUBLIC_API_BASE_URL` to the
   public URL of your deployed backend.
4. Deploy (Next.js is auto-detected).

**Backend → Docker host** (`Dockerfile.vercel` at the repo root)

- Vercel Fluid Compute / HuggingFace Spaces / Cloud Run / Fly.io / Railway —
  anything that runs a Dockerfile. The container binds to the injected `$PORT`
  (defaults to 8000).
- Required env: `GROQ_API_KEY`, `FIREBASE_PROJECT_ID`, `FIREBASE_CLIENT_EMAIL`,
  `FIREBASE_PRIVATE_KEY`, `ALLOWED_ORIGINS` (include your Vercel URL).

> After the frontend is live, add its URL to the backend `ALLOWED_ORIGINS` and
> to **Firebase Auth → Settings → Authorized domains**.

## 8. API reference

All `/api/*` routes require `Authorization: Bearer <Firebase ID token>`.

| Method | Path                | Purpose                                            |
| ------ | ------------------- | -------------------------------------------------- |
| GET    | `/health`           | Liveness probe (no auth)                           |
| GET    | `/api/me`           | Decoded token claims; ensures the base user record |
| GET    | `/api/profile`      | Fetch the stored profile                           |
| POST   | `/api/profile`      | **Create/update** the Firestore profile record     |
| POST   | `/api/workout`      | Generate + persist a workout plan                  |
| POST   | `/api/nutrition`    | Generate + persist a nutrition plan                |
| POST   | `/api/chat`         | Chat with the agent; appends to chat history       |
| GET    | `/api/chat/history` | Fetch chat history                                 |
| GET    | `/api/metrics`      | List health-metric logs                            |
| POST   | `/api/metrics`      | Add/replace a daily metric log                     |
| GET    | `/api/dashboard`    | Profile + plans + metrics + computed stats         |

## Notes

- Agent memory is in-process per `thread_id` (see the `InMemorySaver` in
  [`src/agents/agent.py`](src/agents/agent.py)); durable history lives in
  Firestore under `users/{uid}.chatHistory`.
- Firestore writes happen only via the Admin SDK in the backend; the
  [firestore.rules](firestore.rules) still restrict any direct client access to
  each user's own document.
- Keep the root `.env` (and any `serviceAccountKey.json`) out of version control
  (already handled by [.gitignore](.gitignore)).
