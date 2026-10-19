import { initializeApp, getApps, getApp, FirebaseApp } from "firebase/app";
import { getAuth, Auth } from "firebase/auth";

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
};

const hasConfig = Boolean(firebaseConfig.apiKey && firebaseConfig.appId);

// In the browser, missing env vars are a configuration error — fail loudly with
// an actionable message instead of the cryptic
// "onAuthStateChanged is not a function" that comes from an uninitialized auth.
if (typeof window !== "undefined" && !hasConfig) {
  const missing = [
    ["NEXT_PUBLIC_FIREBASE_API_KEY", firebaseConfig.apiKey],
    ["NEXT_PUBLIC_FIREBASE_APP_ID", firebaseConfig.appId],
    ["NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN", firebaseConfig.authDomain],
    ["NEXT_PUBLIC_FIREBASE_PROJECT_ID", firebaseConfig.projectId],
    ["NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID", firebaseConfig.messagingSenderId],
  ]
    .filter(([, v]) => !v)
    .map(([k]) => k);

  throw new Error(
    "Firebase is not configured. Create frontend/.env.local with your Firebase " +
      "Web App config (Firebase Console → Project settings → Your apps → Web app → " +
      "Config) and restart `npm run dev`. Missing: " +
      missing.join(", ")
  );
}

// During a server-side static prerender (no window) with no env, fall back to a
// null app so the build doesn't crash; it's never used server-side here.
const app: FirebaseApp | null = hasConfig
  ? getApps().length
    ? getApp()
    : initializeApp(firebaseConfig)
  : null;

export const auth: Auth = app ? getAuth(app) : ({} as Auth);
export default app;
