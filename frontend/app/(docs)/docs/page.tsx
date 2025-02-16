const OverViewPage = () => {
  return (
    <>
      <h1 className="mb-4 text-4xl font-bold text-blue-400">
        SARDS Programming Language
      </h1>

      <p className="mb-6 text-lg text-gray-300">
        <strong>SARDS</strong> (Simple Abstract Recursive Dynamic Scripting) is
        a high-level, dynamically typed scripting language designed for
        simplicity, flexibility, and expressive power. It supports structured
        programming, functional paradigms, and interactive execution.
      </p>

      <h2 className="mb-3 text-2xl font-semibold text-green-400">
        Key Features
      </h2>
      <ul className="list-disc space-y-2 pl-6 text-gray-300">
        <li>
          <strong>✅ Dynamic & Flexible Typing:</strong> No need for explicit
          type declarations.
        </li>
        <li>
          <strong>🏗 Structured Control Flow:</strong> Supports{" "}
          <code className="rounded bg-gray-700 px-1">when</code>,{" "}
          <code className="rounded bg-gray-700 px-1">otherwise</code>, and
          loops.
        </li>
        <li>
          <strong>🔄 Looping Constructs:</strong>{" "}
          <code className="rounded bg-gray-700 px-1">Cycle</code> (for loop) and{" "}
          <code className="rounded bg-gray-700 px-1">whenever</code> (while
          loop).
        </li>
        <li>
          <strong>🎭 Functional & Procedural Programming:</strong> Define
          reusable methods.
        </li>
        <li>
          <strong>📜 Switch-Case Support:</strong> Uses{" "}
          <code className="rounded bg-gray-700 px-1">menu-choice</code> for
          pattern matching.
        </li>
        <li>
          <strong>⌨️ Interactive Input Handling:</strong> Uses{" "}
          <code className="rounded bg-gray-700 px-1">listen()</code> for user
          input.
        </li>
        <li>
          <strong>🛠 Error Handling & Debugging:</strong> Clear and readable
          error messages.
        </li>
        <li>
          <strong>🚀 Interactive Execution:</strong> Can run in REPL or via an
          API.
        </li>
      </ul>

      <h2 className="mt-6 mb-3 text-2xl font-semibold text-yellow-400">
        Example Code
      </h2>
      <pre className="overflow-x-auto rounded-lg bg-gray-800 p-4 text-gray-200">
        <code>
          when x &gt; 5 {"{"}
          <br />
          &nbsp;&nbsp;show("X is greater than 5")
          <br />
          {"}"} otherwise {"{"}
          <br />
          &nbsp;&nbsp;show("X is 5 or less")
          <br />
          {"}"}
        </code>
      </pre>

      <h2 className="mt-6 mb-3 text-2xl font-semibold text-purple-400">
        Why Use SARDS?
      </h2>
      <ul className="list-disc space-y-2 pl-6 text-gray-300">
        <li>
          🔹 <strong>Beginner-Friendly:</strong> Simple and easy-to-read syntax.
        </li>
        <li>
          🔹 <strong>Lightweight & Fast:</strong> No unnecessary overhead.
        </li>
        <li>
          🔹 <strong>Expressive & Powerful:</strong> Combines imperative and
          functional paradigms.
        </li>
        <li>
          🔹 <strong>Ideal for Learning:</strong> Great for understanding
          programming concepts.
        </li>
        <li>
          🔹 <strong>Automation & Scripting:</strong> Useful for quick tasks and
          logic execution.
        </li>
      </ul>

      <h2 className="mt-6 mb-3 text-2xl font-semibold text-red-400">
        Next Steps
      </h2>
      <p className="text-lg text-gray-300">
        📌{" "}
        <a href="#installation-guide" className="text-blue-400 hover:underline">
          Installation Guide
        </a>{" "}
        – Set up SARDS.
        <br />
        📌{" "}
        <a href="#basic-syntax" className="text-blue-400 hover:underline">
          Basic Syntax
        </a>{" "}
        – Learn the fundamentals.
        <br />
        📌{" "}
        <a href="#advanced-features" className="text-blue-400 hover:underline">
          Advanced Features
        </a>{" "}
        – Explore loops, methods, and more.
        <br />
        📌{" "}
        <a href="#api-integration" className="text-blue-400 hover:underline">
          API & Web Integration
        </a>{" "}
        – Run SARDS via API.
      </p>

      <p className="mt-6 text-center text-lg font-semibold text-green-400">
        Ready to start? 👉{" "}
        <a href="#quick-start" className="text-blue-400 hover:underline">
          Quick Start Guide
        </a>{" "}
        🚀
      </p>
    </>
  );
};
export default OverViewPage;
