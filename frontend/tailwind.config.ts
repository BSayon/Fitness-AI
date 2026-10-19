import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#ecfffb",
          100: "#cffef5",
          200: "#99fcea",
          300: "#54f3dc",
          400: "#1fe0c8",
          500: "#06c5ae",
          600: "#039e8f",
          700: "#097d73",
          800: "#0d635d",
          900: "#10524d",
        },
        accent: {
          400: "#38e0ff",
          500: "#1ccaf0",
          600: "#0aa6d6",
        },
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      backgroundImage: {
        "gradient-brand":
          "linear-gradient(135deg, #2bf5b8 0%, #0ad3c0 45%, #1ccaf0 100%)",
      },
      boxShadow: {
        glass: "0 8px 32px rgba(0, 0, 0, 0.12)",
        "glass-dark": "0 8px 32px rgba(0, 0, 0, 0.45)",
      },
    },
  },
  plugins: [],
};

export default config;
