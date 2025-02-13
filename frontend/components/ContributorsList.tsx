"use client";

import React, { FC, useEffect, useState } from "react";
import Link from "next/link";

interface Contributor {
  id: number;
  login: string;
  avatar_url: string;
  html_url: string;
}

interface ContributorsListProps {
  owner: string;
  repo: string;
}

const ContributorsList: FC<ContributorsListProps> = ({ owner, repo }) => {
  const [contributors, setContributors] = useState<Contributor[]>([]);

  useEffect(() => {
    async function fetchContributors() {
      try {
        const res = await fetch(
          `https://api.github.com/repos/${owner}/${repo}/contributors`
        );
        if (!res.ok) {
          throw new Error(`Error fetching contributors: ${res.statusText}`);
        }
        const data: Contributor[] = await res.json();
        setContributors(data);
      } catch (error) {
        console.error("Failed to fetch contributors:", error);
      }
    }

    fetchContributors();
  }, [owner, repo]);

  return (
    <div className="flex flex-wrap gap-4">
      {contributors.map((contributor) => (
        <Link
          key={contributor.id}
          href={contributor.html_url}
          target="_blank"
          rel="noopener noreferrer"
        >
          <div className="flex flex-col items-center">
            <img
              src={contributor.avatar_url}
              alt={contributor.login}
              className="size-12 rounded-full object-cover"
            />
            <p className="mt-1 text-sm">{contributor.login}</p>
          </div>
        </Link>
      ))}
    </div>
  );
};

export default ContributorsList;
