import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Nusantara Basa — Peta Interaktif Bahasa Indonesia",
  description: "Jelajahi persebaran bahasa daerah Indonesia dari Aceh sampai Papua. Temukan keragaman linguistik Nusantara.",
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
