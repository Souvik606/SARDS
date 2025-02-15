import React from "react";
import Link from "next/link";
import { Milestone } from "lucide-react";

const NotFound = () => {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-5">
      <h1 className="font-code text-9xl font-black">404</h1>
      <p className="font-code text-3xl font-bold">
        Oops! you went the wrong way.
      </p>
      <Link href="/" className="text-lg opacity-75">
        <Milestone className="mr-3 inline size-8 rotate-y-180 align-middle text-emerald-200" />
        The right way is that side
      </Link>
    </div>
  );
};
export default NotFound;
