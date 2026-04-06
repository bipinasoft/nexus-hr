import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      boxShadow: {
        halo: "0 24px 80px rgba(15, 23, 42, 0.14)"
      },
      colors: {
        canvas: "#f3f5f8",
        ink: "#0f172a",
        brand: "#0f766e",
        aqua: "#0891b2",
        ember: "#ea580c",
        sand: "#fff8ef"
      },
      fontFamily: {
        display: ["var(--font-space-grotesk)"],
        body: ["var(--font-manrope)"]
      }
    }
  },
  plugins: []
};

export default config;

