import React from "react";
import CodeEditor from "@/components/Editor";
import FixedNav from "@/components/FixedNav";

const EditorPage = () => {
  return (
    <>
      <FixedNav />
      <div className="group flex min-h-screen flex-col items-center justify-center gap-5 bg-neutral-900 md:gap-10">
        <h2 className="wrapper skew-y-2 text-center text-5xl font-bold transition-all duration-300 group-focus-within:skew-0 group-focus-within:text-xl group-focus-within:opacity-30 hover:skew-0">
          Welcome to the Shards playground
        </h2>
        <CodeEditor />
      </div>
    </>
  );
};
export default EditorPage;
