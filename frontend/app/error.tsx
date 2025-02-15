"use client";

import React from "react";
import Link from "next/link";
import { Milestone } from "lucide-react";

const Error = () => {
  return (
    <div className="wrapper m-auto flex min-h-screen flex-col items-center justify-center gap-5 text-center text-wrap">
      <h1 className="text-7xl font-black">Something went wrong!</h1>
      <h2 className="text-3xl font-medium">We are working on it! come back.</h2>
      <Link href="/" className="text-zinc-400">
        Go to a safe place <Milestone className="inline size-7 pl-2" />
      </Link>
    </div>
  );
};
export default Error;
