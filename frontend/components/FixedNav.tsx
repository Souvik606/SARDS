import React from "react";
import Link from "next/link";
import { Braces } from "lucide-react";

const FixedNav = () => {
  return (
    <nav className="fixed top-0 z-50 w-full border-b border-zinc-700/50 px-4 py-4 backdrop-blur-2xl sm:px-8">
      <div className="mx-auto w-full max-w-7xl">
        <div className="flex items-center justify-between">
          <div className="flex w-full items-center justify-between sm:w-auto sm:justify-start sm:space-x-8">
            <div className="relative z-50 flex h-12 w-full items-center justify-between sm:w-auto">
              <Link className="flex items-center gap-2" href="/">
                <Braces className="size-6" />
                <p className="font-semibold tracking-tight text-zinc-100">
                  SARDS
                </p>
              </Link>
              <button className="hover:text-primary-text z-50 p-2 text-zinc-400 sm:hidden">
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
                  className="lucide lucide-menu size-5"
                >
                  <line x1="4" x2="20" y1="12" y2="12"></line>
                  <line x1="4" x2="20" y1="6" y2="6"></line>
                  <line x1="4" x2="20" y1="18" y2="18"></line>
                </svg>
              </button>
            </div>
            <div className="hidden space-x-4 sm:flex dark:text-zinc-400">
              <Link className="hover:text-primary-text" href="/docs">
                Docs
              </Link>
              <Link className="hover:text-primary-text" href="/editor">
                Playground
              </Link>
            </div>
          </div>
          <div className="hidden items-center space-x-4 text-zinc-400 sm:flex">
            <div className="flex items-center gap-1.5">
              <Link className="hover:text-primary-text p-2" href="">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  className="size-5"
                >
                  <path
                    d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"
                    fill="currentColor"
                  ></path>
                </svg>
              </Link>
              <Link
                className="hover:text-primary-text p-2"
                href="https://github.com/Souvik606/SARDS"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  className="size-5"
                >
                  <path
                    d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"
                    fill="currentColor"
                  ></path>
                </svg>
              </Link>
              <Link
                className="hover:text-primary-text p-2"
                href="https://x.com/rahulc0dy"
              >
                <svg
                  width="22"
                  height="20"
                  viewBox="0 0 22 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  className="size-5"
                >
                  <path
                    d="M17.244 0.25H20.552L13.325 8.51L21.827 19.75H15.17L9.95603 12.933L3.99003 19.75H0.680028L8.41003 10.915L0.254028 0.25H7.08003L11.793 6.481L17.244 0.25ZM16.083 17.77H17.916L6.08403 2.126H4.11703L16.083 17.77Z"
                    fill="currentColor"
                  ></path>
                </svg>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};
export default FixedNav;
