import type { Metadata } from "next";
import { Cormorant_Garamond, Poppins } from "next/font/google";
import "../styles/globals.css";

// Refined serif for headings
const cormorantGaramond = Cormorant_Garamond({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--cormorant-garamond",
});

// Modern sans‑serif for body text
const poppins = Poppins({
  subsets: ["latin"],
  weight: ["400", "500", "700"],
  variable: "--poppins",
});

export const metadata: Metadata = {
  title: "SARDS",
  description: "SARDS programming language",
};

export default function RootLayout({
                                     children,
                                   }: {
  children: React.ReactNode;
}) {
  return (
      <html lang="en" className={`${cormorantGaramond.variable} scroll-smooth`}>
      <body className={`${poppins.className} relative antialiased`}>
      {children}
      </body>
      </html>
  );
}
