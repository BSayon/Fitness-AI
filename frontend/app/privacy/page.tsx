import Link from "next/link";
import Image from "next/image";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy Policy — Zesayro",
  description:
    "How Zesayro collects, uses, stores, and protects your personal and health-related information.",
};

const LAST_UPDATED = "October 20, 2026";
const CONTACT_EMAIL = "bsayon313@gmail.com";

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="space-y-3">
      <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">
        {title}
      </h2>
      <div className="space-y-3 text-sm leading-relaxed text-slate-600 dark:text-slate-300">
        {children}
      </div>
    </section>
  );
}

export default function PrivacyPolicyPage() {
  return (
    <div className="mx-auto max-w-3xl">
      <div className="card space-y-10">
        <header className="space-y-3 text-center">
          <Image
            src="/logo.png"
            alt="Zesayro"
            width={56}
            height={56}
            className="mx-auto h-14 w-14 rounded-xl"
          />
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
            Privacy Policy
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Last updated: {LAST_UPDATED}
          </p>
        </header>

        <Section title="1. Introduction">
          <p>
            Zesayro (&quot;Zesayro&quot;, &quot;we&quot;, &quot;us&quot;, or
            &quot;our&quot;) provides an AI-powered fitness and nutrition
            assistant that creates personalized workout plans, nutrition
            guidance, and progress tracking. This Privacy Policy explains what
            information we collect, how we use it, who we share it with, and the
            choices you have. By creating an account or using Zesayro, you agree
            to the practices described here.
          </p>
        </Section>

        <Section title="2. Information we collect">
          <p>We collect the following categories of information:</p>
          <ul className="list-disc space-y-2 pl-6">
            <li>
              <strong className="text-slate-800 dark:text-slate-100">
                Account information.
              </strong>{" "}
              When you sign in with Google or email/password via Firebase
              Authentication, we receive your name, email address, profile photo
              (if provided by Google), and a unique user identifier (UID).
            </li>
            <li>
              <strong className="text-slate-800 dark:text-slate-100">
                Fitness profile.
              </strong>{" "}
              Information you enter to personalize your plans: age, gender,
              weight, height (and the resulting BMI), fitness level and goals,
              preferred activities, and weekly schedule.
            </li>
            <li>
              <strong className="text-slate-800 dark:text-slate-100">
                Health-related information.
              </strong>{" "}
              Dietary preferences, food allergies or intolerances, health
              conditions, current medications, daily water intake, and average
              sleep. You provide this voluntarily so the assistant can tailor
              guidance; you may leave any of these fields blank.
            </li>
            <li>
              <strong className="text-slate-800 dark:text-slate-100">
                Activity and progress data.
              </strong>{" "}
              Health-goal tracking entries you log (such as weight, water, sleep,
              and completed workouts), the plans we generate for you, and your
              chat conversations with the AI coach.
            </li>
            <li>
              <strong className="text-slate-800 dark:text-slate-100">
                Technical data.
              </strong>{" "}
              Standard information needed to operate the service securely, such
              as authentication tokens and timestamps.
            </li>
          </ul>
        </Section>

        <Section title="3. How we use your information">
          <ul className="list-disc space-y-2 pl-6">
            <li>To create and maintain your account.</li>
            <li>
              To generate personalized workout plans, nutrition guidance, and
              responses from the AI coach based on the profile you provide.
            </li>
            <li>
              To store your plans, chat history, and progress so they are
              available when you return.
            </li>
            <li>To display dashboards and track progress toward your goals.</li>
            <li>To secure, maintain, debug, and improve the service.</li>
          </ul>
          <p>
            We do <strong>not</strong> sell your personal information, and we do
            not use your health information for advertising.
          </p>
        </Section>

        <Section title="4. AI processing">
          <p>
            To generate plans and chat responses, the relevant parts of your
            fitness profile and your messages are sent to our
            large-language-model provider (Groq) for processing. This data is
            used only to produce your response. Zesayro&apos;s AI output is for
            general informational and educational purposes and is{" "}
            <strong>not medical advice</strong>. Always consult a qualified
            healthcare professional before making decisions about exercise,
            nutrition, medication, or any health condition.
          </p>
        </Section>

        <Section title="5. How your information is stored and shared">
          <p>
            Your data is stored in Google Cloud Firestore and managed through
            Firebase Authentication. We share information only with service
            providers that help us operate Zesayro:
          </p>
          <ul className="list-disc space-y-2 pl-6">
            <li>
              <strong className="text-slate-800 dark:text-slate-100">
                Google Firebase (Authentication &amp; Firestore)
              </strong>{" "}
              — identity and database storage.
            </li>
            <li>
              <strong className="text-slate-800 dark:text-slate-100">
                Groq
              </strong>{" "}
              — AI model processing for plan and chat generation.
            </li>
          </ul>
          <p>
            These providers process data on our behalf under their own terms and
            security practices. We may also disclose information if required by
            law or to protect the rights, safety, and security of our users and
            the service. Access to your Firestore record is restricted so that
            only your authenticated account can read or write it.
          </p>
        </Section>

        <Section title="6. Data retention">
          <p>
            We keep your information for as long as your account is active or as
            needed to provide the service. When you delete your account or
            request deletion, we remove your profile, plans, chat history, and
            tracking data, except where we are required to retain certain
            information to comply with legal obligations.
          </p>
        </Section>

        <Section title="7. Your rights and choices">
          <ul className="list-disc space-y-2 pl-6">
            <li>
              <strong className="text-slate-800 dark:text-slate-100">
                Access and update.
              </strong>{" "}
              You can view and edit your profile at any time from within the app.
            </li>
            <li>
              <strong className="text-slate-800 dark:text-slate-100">
                Deletion.
              </strong>{" "}
              You can request deletion of your account and associated data by
              contacting us at the address below.
            </li>
            <li>
              <strong className="text-slate-800 dark:text-slate-100">
                Withdraw information.
              </strong>{" "}
              You may remove optional health details (such as medications or
              conditions) from your profile at any time.
            </li>
          </ul>
          <p>
            Depending on your location, you may have additional rights under laws
            such as the GDPR or CCPA, including the right to access, correct,
            port, or restrict processing of your personal data.
          </p>
        </Section>

        <Section title="8. Security">
          <p>
            We rely on industry-standard safeguards provided by Google Firebase,
            including encrypted transport (HTTPS), authenticated API access, and
            per-user database access rules. No method of transmission or storage
            is completely secure, but we work to protect your information using
            reasonable technical and organizational measures.
          </p>
        </Section>

        <Section title="9. Children&apos;s privacy">
          <p>
            Zesayro is not intended for children under 13, and the app does not
            knowingly collect information from anyone under 13. If you believe a
            child has provided us with personal information, please contact us so
            we can remove it.
          </p>
        </Section>

        <Section title="10. International users">
          <p>
            Your information may be processed and stored on servers located in
            countries other than your own, including by our service providers.
            By using Zesayro, you consent to the transfer of your information to
            those locations.
          </p>
        </Section>

        <Section title="11. Changes to this policy">
          <p>
            We may update this Privacy Policy from time to time. When we make
            material changes, we will update the &quot;Last updated&quot; date at
            the top of this page. Your continued use of Zesayro after changes
            take effect constitutes acceptance of the revised policy.
          </p>
        </Section>

        <Section title="12. Contact us">
          <p>
            If you have questions about this Privacy Policy or your data, contact
            us at{" "}
            <a
              href={`mailto:${CONTACT_EMAIL}`}
              className="font-medium text-brand-600 hover:underline dark:text-brand-300"
            >
              {CONTACT_EMAIL}
            </a>
            .
          </p>
        </Section>

        <div className="border-t border-white/30 pt-6 text-center dark:border-white/10">
          <Link
            href="/"
            className="text-sm font-medium text-brand-600 hover:underline dark:text-brand-300"
          >
            ← Back to Zesayro
          </Link>
        </div>
      </div>
    </div>
  );
}
