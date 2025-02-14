"use client";
import React, { useState } from "react";

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
        if (['{', '[', '(', '"', "'"].includes(e.key)) {
            e.preventDefault();
            const closingPairs = {
                '{': '}',
                '[': ']',
                '(': ')',
                '"': '"',
                "'": "'"
            };

            const pair = closingPairs[e.key as keyof typeof closingPairs];
            const newValue =
                value.substring(0, start) +
                e.key +
                pair +
                value.substring(end);

            setCode(newValue);
            setTimeout(() => {
                textarea.selectionStart = start + 1;
                textarea.selectionEnd = start + 1;
            }, 0);
            return;
        }

        // Handle closing bracket skipping
        if (['}', ']', ')'].includes(e.key)) {
            if (value[start] === e.key) {
                e.preventDefault();
                textarea.selectionStart = start + 1;
                textarea.selectionEnd = start + 1;
                return;
            }
        }

        // Handle Enter key with smart indentation
        if (e.key === 'Enter') {
            e.preventDefault();
            const before = value.substring(0, start);
            let after = value.substring(end);

            // Get current indentation
            const lineStart = before.lastIndexOf('\n') + 1;
            const currentLine = before.substring(lineStart);
            const indentMatch = currentLine.match(/^\s*/);
            const currentIndent = indentMatch ? indentMatch[0] : '';

            // Check if we're after an opening brace
            const lineEndsWithBrace = currentLine.trim().endsWith('{');
            const nextChar = value.substring(start, start + 1);
            const hasExistingCloser = nextChar === '}';

            let newContent = '';
            let newCursorPos = start;

            if (lineEndsWithBrace) {
                // Calculate indentation levels
                const newIndent = currentIndent + '\t';
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
        if (e.key === 'Tab') {
            e.preventDefault();
            const newValue =
                value.substring(0, start) +
                '\t' +
                value.substring(end);
            setCode(newValue);
            setTimeout(() => {
                textarea.selectionStart = start + 1;
                textarea.selectionEnd = start + 1;
            }, 0);
        }
    };

    return (
        <div className="flex items-center justify-center h-screen bg-gray-900">
            <div className="w-3/4 max-w-5xl bg-gray-850 rounded-lg shadow-lg overflow-hidden border border-gray-700">
                <div className="bg-gray-800 h-12 flex items-center justify-between px-4 border-b border-gray-700">
                    <div className="text-lg font-semibold text-white">Playground</div>
                    <div className="flex space-x-4">
                        <button className="bg-emerald-600 hover:bg-emerald-700 text-white font-medium px-8 py-3 rounded-full">
                            Run
                        </button>
                        <button className="bg-orange-100 text-orange-600 font-medium px-8 py-2 rounded-full">
                            Clear
                        </button>
                    </div>
                </div>

                <div className="flex">
                    <div className="bg-gray-800 text-gray-400 text-sm font-mono p-4 pr-2 text-right select-none">
                        {lineNumbers.map((lineNumber) => (
                            <div key={lineNumber}>{lineNumber}</div>
                        ))}
                    </div>

                    <textarea
                        className="flex-1 h-96 bg-gray-850 text-white font-mono text-sm p-4 border-none focus:outline-none resize-none"
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