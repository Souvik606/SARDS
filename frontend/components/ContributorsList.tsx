import React, { FC } from "react";
import Link from "next/link";
import { Ellipsis } from "lucide-react";
import axios, { AxiosError } from "axios";

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

const getContributors = async ({
  owner,
  repo,
}: {
  owner: string;
  repo: string;
}) => {
  try {
    return await axios.get(
      `https://api.github.com/repos/${owner}/${repo}/contributors`
    );
  } catch (error: AxiosError | Error | any) {
    if (error.response) {
      console.error(error.response);
      throw new Error(error.response);
    } else {
      console.error("Unexpected Error:", error);
      throw new Error(error.message);
    }
  }
};

const ContributorsList: FC<ContributorsListProps> = async ({ owner, repo }) => {
  const { data } = await getContributors({ owner, repo });
  return (
    <div className="flex flex-wrap gap-4">
      {data.map((contributor: Contributor) => (
        <Link
          key={contributor.id}
          href={contributor.html_url}
          target="_blank"
          rel="noopener noreferrer"
          className="relative -ml-6 transition-all hover:z-50 hover:scale-110"
        >
          <div className="flex flex-col items-center">
            <img
              src={contributor.avatar_url}
              alt={contributor.login}
              className="border-background-400 peer size-10 rounded-full border-3 object-cover drop-shadow-md hover:border-4"
            />
            <p className="absolute bottom-full mt-1 hidden w-max text-sm peer-hover:block">
              {contributor.login}
            </p>
          </div>
        </Link>
      ))}
      <Link
        href={`https://github.com/${owner}/${repo}`}
        target="_blank"
        rel="noopener noreferrer"
        className="relative -ml-6 transition-all hover:z-50 hover:scale-110"
      >
        <div className="border-background-400 flex size-10 items-center justify-center rounded-full border-3 bg-zinc-800 text-zinc-600 drop-shadow-md hover:border-4">
          <Ellipsis className="text-secondary-text" />
        </div>
      </Link>
    </div>
  );
};

export default ContributorsList;
