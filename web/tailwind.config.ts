import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        earth: {
          50: "#faf6ed",
          100: "#f5f0e8",
          200: "#e8e0d0",
          300: "#e0d5c0",
          400: "#d4c5a9",
          500: "#c4b08a",
          600: "#6b5d4f",
          700: "#3d3225",
          800: "#2a2218",
          900: "#1a1510",
        },
        rumpun: {
          austronesia: "#c4703f",
          papua: "#8b3a3a",
          transNewGuinea: "#5a7247",
          lainnya: "#6b5b8a",
        },
        vitalitas: {
          aman: "#22c55e",
          rentan: "#eab308",
          terancam: "#f97316",
          kritis: "#ef4444",
        },
      },
      fontFamily: {
        sans: ["Plus Jakarta Sans", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
