export const tokens = {
  color: {
    primary: { 950: "#10201E", 700: "#0B5F56", 600: "#0F766E", 100: "#DDF4EF", 50: "#EEF9F6" },
    neutral: { 950: "#141615", 800: "#2B2E2C", 600: "#5F625E", 400: "#9A9D97", 200: "#E4E1DA", 100: "#F0EEE8", 50: "#F7F6F2", white: "#FFFFFF" },
    signal: { blue: "#2F6EEA", amber: "#B86B16", violet: "#6D55D9", coral: "#D45F4C", cyan: "#0E7490" },
    semantic: { success: "#16825D", warning: "#B86B16", danger: "#C74637", info: "#2F6EEA" }
  },
  radius: { xs: "4px", sm: "6px", md: "8px", lg: "12px" },
  shadow: { sm: "0 1px 2px rgba(20,22,21,0.06)", md: "0 8px 24px rgba(20,22,21,0.08)", lg: "0 24px 70px rgba(20,22,21,0.12)" },
  space: { 1: "4px", 2: "8px", 3: "12px", 4: "16px", 5: "20px", 6: "24px", 8: "32px", 10: "40px", 12: "48px", 16: "64px" }
} as const;