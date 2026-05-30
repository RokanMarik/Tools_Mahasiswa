import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Peta Bahasa Indonesia",
  description: "Peta interaktif persebaran bahasa daerah di Indonesia. Jelajahi 700+ bahasa dari Aceh sampai Papua.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <body className="min-h-screen">
        {children}
      </body>
    </html>
  );
}
