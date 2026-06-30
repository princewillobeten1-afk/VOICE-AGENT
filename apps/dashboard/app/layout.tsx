import type { Metadata } from "next";
import "@voicesense/ui/src/styles.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "VoiceSense Dashboard",
  description: "Create, test, deploy, and observe AI employees.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}