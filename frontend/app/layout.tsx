import type { Metadata } from "next";
import localFont from "next/font/local";
import "../styles/globals.css";

const firaCode = localFont({
  src: "../fonts/FiraCode.ttf",
  display: "swap",
  style: "normal",
  variable: "--fira-code",
});

const inconsolata = localFont({
  src: "../fonts/Inconsolata.ttf",
  display: "swap",
  style: "normal",
  preload: true,
});

export const metadata: Metadata = {
  title: "SARDS",
  description: "sards programming language",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${firaCode.variable} ${inconsolata.className} relative antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
