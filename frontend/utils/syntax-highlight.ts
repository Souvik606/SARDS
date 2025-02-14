import hljs from "highlight.js/lib/core";

hljs.registerLanguage("sards", function (hljs) {
  return {
    name: "sards",
    keywords: {
      keyword:
        "define and or not when orwhen otherwise Cycle whenever method yield escape proceed menu choice fallback",
    },
    contains: [
      // Comments (assuming // is for single-line comments)
      { className: "comment", begin: /\/\/.*/ },

      // Strings (both single and double quotes)
      { className: "string", begin: /"(?:\\.|[^"\\])*"/ },
      { className: "string", begin: /'(?:\\.|[^'\\])*'/ },

      // Numbers (integers and floats)
      { className: "number", begin: /\b\d+(\.\d+)?\b/ },

      // Keywords (highlighting control structures)
      {
        className: "keyword",
        begin:
          /\b(define|and|or|not|when|orwhen|otherwise|Cycle|whenever|method|yield|escape|proceed|menu|choice|fallback)\b/,
      },

      // Function definitions and calls
      {
        className: "function",
        begin: /\b[a-zA-Z_]\w*(?=\s*\()/, // Matches function names like show(...)
      },

      // Identifiers (variables)
      {
        className: "variable",
        begin: /\b[a-zA-Z_]\w*\b/,
      },

      // Operators (=, +, -, *, /, etc.)
      {
        className: "operator",
        begin: /=|\+|-|\*|\/|%|==|!=|<=|>=|<|>/,
      },

      // Punctuation and brackets
      {
        className: "punctuation",
        begin: /[{}[\];(),.:]/,
      },
    ],
  };
});
