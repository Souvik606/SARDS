import React from "react";
import Sidebar from "@/components/Sidebar";

const DocsLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="wrapper grid grid-cols-[1fr_2.5fr]">
      <Sidebar />
      <main className="px-3 py-5">{children}</main>
    </div>
  );
};
export default DocsLayout;
