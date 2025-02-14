import type { Metadata } from "next";
import { Fira_Code, Poppins } from "next/font/google";
import "../styles/globals.css";

const firaCode = Fira_Code({
  subsets: ["latin"],
  display: "swap",
  variable: "--fira-code",
});

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["100", "200", "300", "400", "500", "600", "700", "800", "900"],
  preload: true,
  style: "normal",
  display: "swap",
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
    <html lang="en" className={`${firaCode.variable} scroll-smooth`}>
      <body className={`${poppins.className} relative antialiased`}>
        {children}
      </body>
    </html>
  );
}
