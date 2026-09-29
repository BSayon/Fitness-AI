---
title: Fitness AI Bot
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8000
tags:
  - nextjs
  - fastapi
  - firebase
pinned: false
short_description: AI-powered Fitness Coach (Next.js + FastAPI + Firebase)
---

# 🏋️ AI Fitness Coach

Full-stack app that generates personalized workout & nutrition plans and lets
users chat with an AI fitness coach.

- **Frontend** — Next.js 14 (App Router) + TypeScript + Tailwind CSS, hosted on
  **Vercel**. Uses the **Firebase Auth** client SDK for sign-in and **Firestore**
  for per-user profile / plan / chat storage.
- **Backend** — **FastAPI** + LangChain + Groq (`openai/gpt-oss-120b`), packaged
  as a Docker image (`backend/Dockerfile`). Verifies incoming Firebase ID
  tokens with the **Firebase Admin SDK** before calling the LLM.
- **Auth & DB** — **Firebase** (Authentication + Firestore).

```
┌────────────────┐   Firebase ID token   ┌──────────────────┐
│  Next.js (UI)  │ ────────────────────▶ │  FastAPI (Docker)│
│   on Vercel    │ ◀─────────────────── │  LangChain+Groq  │
└──────┬─────────┘  workout/nutrition/  └──────────────────┘
       │            chat responses
       │  reads / writes
       ▼
   Firestore (users/{uid})
```

## Project layout

```
Fitness-AI-Bot/
├── backend/                  # FastAPI + Docker (deploy anywhere Docker runs)
│   ├── app/
│   │   ├── main.py           # FastAPI entrypoint (/api/workout, /api/nutrition, /api/chat)
│   │   ├── service.py        # LangChain/Groq logic (ported from src/service.py)
│   │   ├── firebase.py       # Firebase Admin init + verify_token dependency
│   │   └── models.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/                 # Next.js 14 (deploy to Vercel)
│   ├── app/                  # / , /login, /register, /profile, /dashboard, /chat
│   ├── components/           # Navbar, ProfileForm, Markdown, AuthGate
│   ├── lib/                  # firebase.ts, auth-context.tsx, firestore.ts, api.ts
│   └── .env.local.example
├── firestore.rules           # Users can only read/write their own /users/{uid}
├── src/                      # Original Streamlit prototype (kept for reference)
└── README.md
```

## 1. Firebase setup

1. Create a project at <https://console.firebase.google.com>.
2. **Authentication → Sign-in method:** enable **Email/Password** and **Google**.
3. **Firestore Database:** create a database (production mode).
4. Deploy the security rules in [firestore.rules](firestore.rules) (Firebase Console → Firestore → Rules).
5. **Project settings → Your apps → Web app:** copy the config values into `frontend/.env.local`.
6. **Project settings → Service accounts → Generate new private key**. Save the JSON — this powers the backend's Admin SDK.

## 2. Backend (Docker)

```powershell
cd backend
Copy-Item .env.example .env
# Fill in GROQ_API_KEY and either GOOGLE_APPLICATION_CREDENTIALS or FIREBASE_SERVICE_ACCOUNT_JSON
docker build -t fitness-ai-backend .
docker run --rm -p 8000:8000 --env-file .env fitness-ai-backend
```

Endpoints (all require `Authorization: Bearer <firebase-id-token>` except `/health`):

| Method | Path             | Purpose                         |
| ------ | ---------------- | ------------------------------- |
| GET    | `/health`        | Liveness probe                  |
| GET    | `/api/me`        | Return decoded token claims     |
| POST   | `/api/workout`   | Generate personalized workout   |
| POST   | `/api/nutrition` | Generate personalized nutrition |
| POST   | `/api/chat`      | Chat with the AI coach          |

Request body for generation endpoints:

```json
{
  "profile": {
    /* UserProfile */
  },
  "message": "optional (chat only)"
}
```

### Deploying the backend container

Any Docker-compatible host works. Recommended options:

- **Google Cloud Run** — `gcloud run deploy` from `backend/`.
- **Fly.io** — `fly launch` inside `backend/`.
- **Railway / Render** — point them at the `backend/Dockerfile`.
- **Vercel Fluid Compute (beta)** — supports Dockerfiles; point to `backend/Dockerfile`.

Set these environment variables on your host:

| Var                             | Value                                                      |
| ------------------------------- | ---------------------------------------------------------- |
| `GROQ_API_KEY`                  | Your Groq API key                                          |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | Full service-account JSON, single-line (preferred)         |
| `ALLOWED_ORIGINS`               | `https://<your-frontend>.vercel.app,http://localhost:3000` |

Alternatively mount the service-account file and set `GOOGLE_APPLICATION_CREDENTIALS` to its path.

## 3. Frontend (Vercel)

```powershell
cd frontend
Copy-Item .env.local.example .env.local
# Fill in NEXT_PUBLIC_FIREBASE_* and NEXT_PUBLIC_API_BASE_URL
npm install
npm run dev
```

Open <http://localhost:3000>.

### Deploy on Vercel

1. Push the repo to GitHub.
2. Import the project in Vercel and set the **Root Directory** to `frontend`.
3. Under **Environment Variables** add every `NEXT_PUBLIC_*` value from
   `.env.local` and set `NEXT_PUBLIC_API_BASE_URL` to the public URL of your
   deployed backend container.
4. Deploy. Vercel auto-detects Next.js — no extra config required.

> After the backend is live, add the Vercel URL to the backend's
> `ALLOWED_ORIGINS` env var and to **Firebase Auth → Settings → Authorized domains**.

## 4. Local development quickstart

```powershell
# terminal 1 — backend
cd backend
docker build -t fitness-ai-backend .
docker run --rm -p 8000:8000 --env-file .env fitness-ai-backend

# terminal 2 — frontend
cd frontend
npm install
npm run dev
```

## Notes

- Chat history is kept in-memory per backend process (see `_sessions` in
  [backend/app/service.py](backend/app/service.py)). For horizontal scaling swap in a Redis / Firestore
  backed `BaseChatMessageHistory`.
- Firestore stores `profile`, `workoutPlan`, `nutritionPlan`, and `chatHistory`
  under `users/{uid}` — visible only to that user via the rules in
  [firestore.rules](firestore.rules).
- The original Streamlit app remains under `src/` for reference.
