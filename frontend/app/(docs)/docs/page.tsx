"use client";

import React, { useEffect } from "react";

const DocsPage = () => {
  const [title, setTitle] = React.useState<string>("Documentation");

  useEffect(() => {
    document.title = title;
  }, [title]);

  return (
    <div>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
    </div>
  );
};
export default DocsPage;
