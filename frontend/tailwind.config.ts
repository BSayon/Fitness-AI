import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#fff4ec",
          100: "#ffe5d0",
          200: "#ffc59d",
          300: "#ffa16a",
          400: "#ff7f3e",
          500: "#ff6b35",
          600: "#e0521f",
          700: "#b53f18",
          800: "#823017",
          900: "#4d1e0e",
        },
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      backgroundImage: {
        "gradient-brand":
          "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ff6b35 100%)",
      },
    },
  },
  plugins: [],
};

export default config;
