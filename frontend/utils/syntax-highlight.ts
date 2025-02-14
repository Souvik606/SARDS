import hljs from "highlight.js/lib/core";

hljs.registerLanguage("sards", (hljs) => {
  return {
    name: "sards",
    keywords: {
      keyword:
        "define and or not when orwhen otherwise Cycle whenever method yield escape proceed menu choice fallback",
    },
    contains: [
      // Numbers (integer and floating point)
      { className: "number", begin: /\b\d+(\.\d+)?\b/ },
      // Strings: support both double and single quotes
      {
        className: "string",
        variants: [
          { begin: /"/, end: /"/ },
          { begin: /'/, end: /'/ },
        ],
      },
      // Comments: support single-line (//) and multi-line (/* */) comments
      {
        className: "comment",
        variants: [
          { begin: /\/\//, end: /$/ },
          { begin: /\/\*/, end: /\*\// },
        ],
      },
      // Function names: match identifiers followed by an opening parenthesis (allowing whitespace)
      { className: "function", begin: /\b[a-zA-Z_]\w*(?=\s*\()/ },
      // Operators: include arithmetic, assignment, and comparison operators
      { className: "operator", begin: /[+\-*/=<>!%]+/ },
      // Punctuation: common brackets, braces, commas, semicolons, and periods
      { className: "punctuation", begin: /[{}[\];(),.:]/ },
      // Variables: simple identifier pattern
      { className: "variable", begin: /\b[a-zA-Z_]\w*\b/ },
    ],
  };
});
