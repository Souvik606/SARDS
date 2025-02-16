"use client";

import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";

type SidebarLink = {
  name: string;
  href: string;
};

type SidebarSection = {
  title: string;
  links: SidebarLink[];
};

const sidebarLinks: SidebarSection[] = [
  {
    title: "Introduction",
    links: [
      { name: "Overview", href: "#overview" },
      { name: "Installation", href: "#installation" },
      { name: "Quick Start", href: "#quick-start" },
    ],
  },
  {
    title: "Language Features",
    links: [
      { name: "Syntax", href: "#syntax" },
      { name: "Data Types", href: "#data-types" },
      { name: "Control Flow", href: "#control-flow" },
      { name: "Functions", href: "#functions" },
    ],
  },
  {
    title: "Advanced Topics",
    links: [
      { name: "Pattern Matching", href: "#pattern-matching" },
      { name: "Error Handling", href: "#error-handling" },
      { name: "Performance Optimization", href: "#performance" },
    ],
  },
];

export default function Sidebar() {
  const [openSections, setOpenSections] = useState<Record<string, boolean>>(
    sidebarLinks.reduce(
      (acc, section) => ({ ...acc, [section.title]: true }),
      {}
    )
  );

  const toggleSection = (title: string) => {
    setOpenSections((prev) => ({ ...prev, [title]: !prev[title] }));
  };

  return (
    <aside className="sticky top-0 bottom-0 border-r border-gray-700 bg-zinc-900 p-4 text-white">
      <h1 className="mb-4 text-xl font-bold text-cyan-200">SARDS Docs</h1>

      <nav className="space-y-4">
        {sidebarLinks.map((section) => (
          <div key={section.title}>
            <button
              onClick={() => toggleSection(section.title)}
              className="flex w-full items-center justify-between rounded-lg px-2 py-2 text-left font-semibold text-gray-300 hover:bg-gray-800"
            >
              {section.title}
              {openSections[section.title] ? (
                <ChevronDown className="h-5 w-5" />
              ) : (
                <ChevronRight className="h-5 w-5" />
              )}
            </button>
            {openSections[section.title] && (
              <ul className="mt-1 pl-4">
                {section.links.map((link) => (
                  <li key={link.name}>
                    <a
                      href={link.href}
                      className="block rounded-lg px-3 py-1.5 text-gray-400 transition hover:bg-gray-800 hover:text-blue-400"
                    >
                      {link.name}
                    </a>
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </nav>
    </aside>
  );
}
