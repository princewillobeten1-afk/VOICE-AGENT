import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class", '[data-theme="dark"]'],
  content: [
    "./apps/**/*.{ts,tsx}",
    "./packages/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--vs-bg)",
        surface: "var(--vs-surface)",
        foreground: "var(--vs-text)",
        muted: "var(--vs-muted)",
        border: "var(--vs-border)",
        primary: "var(--vs-primary)",
        success: "var(--vs-success)",
        warning: "var(--vs-warning)",
        danger: "var(--vs-danger)",
        info: "var(--vs-info)",
      },
      borderRadius: {
        sm: "var(--vs-radius-sm)",
        md: "var(--vs-radius-md)",
      },
      boxShadow: {
        md: "var(--vs-shadow-md)",
        lg: "var(--vs-shadow-lg)",
      },
    },
  },
};

export default config;