"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";

const StarOnGithubBtn = () => {
  const [stars, setStars] = useState(0);

  useEffect(() => {
    const getRepoStars = async () => {
      try {
        const res = await fetch(
          `https://api.github.com/repos/Souvik606/SARDS`,
          { cache: "no-cache" }
        );
        if (!res.ok) {
          throw new Error(`Error fetching contributors: ${res.statusText}`);
        }
        const data = await res.json();
        setStars(data.stargazers_count);
      } catch (error) {
        console.error("Failed to fetch contributors:", error);
      }
    };
    getRepoStars();
  }, []);

  return (
    <Link
      target="_blank"
      rel="noopener noreferrer"
      className="group hover:fill-primary button border-muted-light text-primary-text bg-background-100 relative order-2 mt-1 flex h-14 w-full max-w-sm transform items-center justify-center gap-2 overflow-hidden rounded-md border px-4 py-2 font-mono text-sm font-medium whitespace-nowrap ring-offset-2 ring-offset-zinc-900 transition-all duration-300 hover:ring-2 sm:text-base"
      href="https://github.com/Souvik606/SARDS"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        className="size-4 shrink-0"
      >
        <path
          d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"
          fill="currentColor"
        ></path>
      </svg>
      Star on GitHub
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="lucide lucide-star group-hover:fill-primary size-4 shrink-0 fill-gray-500 stroke-transparent transition-colors"
      >
        <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path>
      </svg>
      {stars}
      <div className="bg-muted-dark absolute -top-[50px] -left-[75px] -z-10 h-[155px] w-8 rotate-[35deg] opacity-20 transition-all duration-500 ease-[cubic-bezier(0.19,1,0.22,1)] group-hover:left-[120%]"></div>
    </Link>
  );
};

export default StarOnGithubBtn;
