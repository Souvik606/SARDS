"use client";
import React, { useState } from "react";
import { Play, Trash } from "lucide-react";

const CodeEditor: React.FC = () => {
  const [code, setCode] = useState<string>("");
  const lineNumbers = code.split("\n").map((_, index) => index + 1);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setCode(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    const textarea = e.currentTarget;
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;

    // Handle bracket auto-closing
    if (["{", "[", "(", '"', "'"].includes(e.key)) {
      e.preventDefault();
      const closingPairs = {
        "{": "}",
        "[": "]",
        "(": ")",
        '"': '"',
        "'": "'",
      };

      const pair = closingPairs[e.key as keyof typeof closingPairs];
      const newValue =
        value.substring(0, start) + e.key + pair + value.substring(end);

      setCode(newValue);
      setTimeout(() => {
        textarea.selectionStart = start + 1;
        textarea.selectionEnd = start + 1;
      }, 0);
      return;
    }

    // Handle closing bracket skipping
    if (["}", "]", ")"].includes(e.key)) {
      if (value[start] === e.key) {
        e.preventDefault();
        textarea.selectionStart = start + 1;
        textarea.selectionEnd = start + 1;
        return;
      }
    }

    // Handle Enter key with smart indentation
    if (e.key === "Enter") {
      e.preventDefault();
      const before = value.substring(0, start);
      let after = value.substring(end);

      // Get current indentation
      const lineStart = before.lastIndexOf("\n") + 1;
      const currentLine = before.substring(lineStart);
      const indentMatch = currentLine.match(/^\s*/);
      const currentIndent = indentMatch ? indentMatch[0] : "";

      // Check if we're after an opening brace
      const lineEndsWithBrace = currentLine.trim().endsWith("{");
      const nextChar = value.substring(start, start + 1);
      const hasExistingCloser = nextChar === "}";

      let newContent = "";
      let newCursorPos = start;

      if (lineEndsWithBrace) {
        // Calculate indentation levels
        const newIndent = currentIndent + "\t";
        const closingIndent = currentIndent;

        // Handle existing closing brace
        if (hasExistingCloser) {
          newContent = `\n${newIndent}\n${closingIndent}}`;
          after = after.substring(1); // Remove existing closing brace
        } else {
          newContent = `\n${newIndent}`;
        }

        newCursorPos = start + newIndent.length + 1;
      } else {
        // Regular indentation
        newContent = `\n${currentIndent}`;
        newCursorPos = start + currentIndent.length + 1;
      }

      setCode(before + newContent + after);
      setTimeout(() => {
        textarea.selectionStart = newCursorPos;
        textarea.selectionEnd = newCursorPos;
      }, 0);
      return;
    }

    // Handle Tab key
    if (e.key === "Tab") {
      e.preventDefault();
      const newValue = value.substring(0, start) + "\t" + value.substring(end);
      setCode(newValue);
      setTimeout(() => {
        textarea.selectionStart = start + 1;
        textarea.selectionEnd = start + 1;
      }, 0);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-900">
      <div className="bg-gray-850 wrapper w-3/4 overflow-hidden rounded-lg border border-gray-700 shadow-lg">
        <div className="flex h-12 items-center justify-between border-b border-gray-700 bg-gray-800 px-4">
          <div className="text-lg font-semibold text-white">Playground</div>
          <div className="flex space-x-4">
            <button className="flex cursor-pointer items-center gap-2 rounded-full border border-teal-400 px-8 py-1 font-bold text-zinc-100 transition-all hover:bg-teal-400 hover:text-zinc-800">
              <Play className="inline size-3" fill="currentColor" />
              <span>Run</span>
            </button>
            <button className="border-danger-700 hover:bg-danger-700 flex cursor-pointer items-center gap-2 rounded-full border px-8 py-1 font-bold text-zinc-100 transition-all hover:text-zinc-800">
              <Trash className="inline size-3" fill="currentColor" />
              <span>Clear</span>
            </button>
          </div>
        </div>

        <div className="flex">
          <div className="bg-gray-800 p-4 pr-2 text-right font-mono text-sm text-gray-400 select-none">
            {lineNumbers.map((lineNumber) => (
              <div key={lineNumber}>{lineNumber}</div>
            ))}
          </div>

          <textarea
            className="bg-gray-850 h-96 flex-1 resize-none border-none p-4 font-mono text-sm text-white focus:outline-none"
            placeholder="// Start coding your .sards file here..."
            value={code}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
          />
        </div>
      </div>
    </div>
  );
};

export default CodeEditor;
