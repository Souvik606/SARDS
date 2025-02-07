---
title: Grammer Rules for SARDS
description: This file defines the grammar rules for the SARDS language. This file has no programmatic significance.
---

# Grammar Documentation

This document describes the grammar for a small programming language, outlining its syntax rules, operator precedence, and usage examples.

## Table of Contents

-   [Overview](#overview)
-   [Grammar Rules](#grammar-rules)
    -   [Multiline Block](#multiline-block)
    -   [Jump Statements](#jump-statements)
    -   [Statements](#statements)
    -   [Expressions](#expressions)
        -   [Comparison Expressions](#comparison-expressions)
        -   [Arithmetic Expressions](#arithmetic-expressions)
            -   [Term](#term)
            -   [Unary and Exponentiation](#unary-and-exponentiation)
        -   [Factor](#factor)
    -   [Function Calls and List Expressions](#function-calls-and-list-expressions)
    -   [Control Flow Constructs](#control-flow-constructs)
-   [Operator Precedence](#operator-precedence)
-   [Usage Examples](#usage-examples)

## Overview

This grammar defines a language that supports:

-   **Expressions:** Including arithmetic and logical operations.
-   **Statements:** Such as assignments, optionally prefixed with a declaration keyword.
-   **Control Flow Constructs:** Like conditionals (`if`/`elif`/`else`), loops (`while`/`for`), and function definitions.
-   **Compound Constructs:** Including function calls, list expressions, and jump statements for control flow.

## Grammar Rules

Below is the complete grammar definition:

```grammar
multiline: NEWLINE* (expression | statements | jump_statements) (NEWLINE* (expression | statements | jump_statements))* NEWLINE*

jump-statements: KEYWORD:yield expression | KEYWORD:proceed | KEYWORD:escape

statements: (KEYWORD:define)? IDENTIFIER EQUAL expression

expression: jump_statements | comp-expression ((KEYWORD:AND | OR) comp-expression)*

comp-expression: KEYWORD:NOT comp-expression | arith-expression ((EE | NEQ | LT | GT | LTE | GTE) arith-expression)*

arith-expression: term ((PLUS | MINUS) term)*

term: unary ((MUL | DIV) unary)* | function-call

unary: (PLUS | MINUS) factor | exponent

exponent: factor (EXP unary)*

factor: INT | FLOAT | STRING | IDENTIFIER | LPAREN expression RPAREN | if-expression | for-expression | while-expression | function-definition | list-expression

function-call: IDENTIFIER LPAREN (expression (COMMA expression)*)? RPAREN

list-expression: LPAREN3 (expression (COMMA expression)*)? RPAREN RPAREN3

while-expression: KEYWORD:whenever expression LPAREN2 (expression | statements) RPAREN2? NEWLINE multiline RPAREN2

for-expression: KEYWORD:Cycle IDENTIFIER EQUAL expression COLON expression (COLON expression)? LPAREN2 (expression | statements) RPAREN2? NEWLINE multiline RPAREN2

function-definition: KEYWORD:method IDENTIFIER? LPAREN (IDENTIFIER (COMMA IDENTIFIER)*)? RPAREN LPAREN2 (expression | statements) RPAREN2? NEWLINE multiline RPAREN2

if-expression: KEYWORD:when expression LPAREN2 ((expression | statements) RPAREN2 (elif-expression | else-expression)?)? (NEWLINE multiline RPAREN2 (elif-expression | else-expression))?

elif-expression: KEYWORD:orwhen expression LPAREN2 ((expression | statements) RPAREN2 (elif-expression | else-expression)?)? (NEWLINE multiline RPAREN2 (elif-expression | else-expression))?

else-expression: KEYWORD:otherwise LPAREN2 ((expression | statements) RPAREN2)? NEWLINE multiline RPAREN2
```

### Multiline Block

-   **Rule:**
    ```grammar
    multiline: NEWLINE* (expression | statements | jump_statements) (NEWLINE* (expression | statements | jump_statements))* NEWLINE*
    ```
-   **Description:**  
    A `multiline` block represents a sequence of expressions, statements, or jump statements. Newlines may precede, separate, or follow these items.

### Jump Statements

-   **Rule:**
    ```grammar
    jump-statements: KEYWORD:yield expression | KEYWORD:proceed | KEYWORD:escape
    ```
-   **Description:**  
    These statements are used to alter the control flow:
    -   `yield expression` can return or yield a value.
    -   `proceed` and `escape` provide additional control flow mechanisms.

### Statements

-   **Rule:**
    ```grammar
    statements: (KEYWORD:define)? IDENTIFIER EQUAL expression
    ```
-   **Description:**  
    This rule describes an assignment. The optional `define` keyword can be used to declare a variable while assigning it a value.

### Expressions

Expressions are constructed from several layers, each managing a subset of operations.

#### Comparison Expressions

-   **Rule:**
    ```grammar
    comp-expression: KEYWORD:NOT comp-expression | arith-expression ((EE | NEQ | LT | GT | LTE | GTE) arith-expression)*
    ```
-   **Description:**  
    This rule allows:
    -   Use of `NOT` for negating an expression.
    -   Application of comparison operators (equal, not equal, less than, etc.) between arithmetic expressions.

#### Arithmetic Expressions

-   **Rule:**
    ```grammar
    arith-expression: term ((PLUS | MINUS) term)*
    ```
-   **Description:**  
    Manages addition and subtraction between terms. Operations are **left-associative** (evaluated from left to right).

##### Term

-   **Rule:**
    ```grammar
    term: unary ((MUL | DIV) unary)* | function-call
    ```
-   **Description:**  
    Handles multiplication and division, which have higher precedence than addition/subtraction. Additionally, a function call is considered at this level.

##### Unary and Exponentiation

-   **Unary Rule:**
    ```grammar
    unary: (PLUS | MINUS) factor | exponent
    ```
-   **Exponentiation Rule:**
    ```grammar
    exponent: factor (EXP unary)*
    ```
-   **Description:**
    -   **Unary operators** (`+`, `-`) apply directly to a `factor`.
    -   **Exponentiation** (`EXP`) binds tighter than multiplication and addition.

#### Factor

-   **Rule:**
    ```grammar
    factor: INT | FLOAT | STRING | IDENTIFIER | LPAREN expression RPAREN | if-expression | for-expression | while-expression | function-definition | list-expression
    ```
-   **Description:**  
    The `factor` is the basic building block. It can be:
    -   A literal (integer, float, string)
    -   An identifier
    -   A parenthesized expression to enforce precedence
    -   A compound expression (such as conditionals, loops, or function definitions)

### Function Calls and List Expressions

-   **Function Call Rule:**
    ```grammar
    function-call: IDENTIFIER LPAREN (expression (COMMA expression)*)? RPAREN
    ```
-   **List Expression Rule:**
    ```grammar
    list-expression: LPAREN3 (expression (COMMA expression)*)? RPAREN RPAREN3
    ```
-   **Description:**
    -   A **function call** is an identifier followed by a list of expressions in standard parentheses.
    -   A **list expression** is delimited by distinct tokens (`LPAREN3` and `RPAREN3`) to differentiate it from regular grouped expressions.

### Control Flow Constructs

Several rules define control flow mechanisms, including loops and conditionals:

-   **While Expression:**
    ```grammar
    while-expression: KEYWORD:whenever expression LPAREN2 (expression | statements) RPAREN2? NEWLINE multiline RPAREN2
    ```
-   **For Expression:**
    ```grammar
    for-expression: KEYWORD:Cycle IDENTIFIER EQUAL expression COLON expression (COLON expression)? LPAREN2 (expression | statements) RPAREN2? NEWLINE multiline RPAREN2
    ```
-   **Function Definition:**
    ```grammar
    function-definition: KEYWORD:method IDENTIFIER? LPAREN (IDENTIFIER (COMMA IDENTIFIER)*)? RPAREN LPAREN2 (expression | statements) RPAREN2? NEWLINE multiline RPAREN2
    ```
-   **Conditional Expressions:**
    -   **If Expression:**
        ```grammar
        if-expression: KEYWORD:when expression LPAREN2 ((expression | statements) RPAREN2 (elif-expression | else-expression)?)? (NEWLINE multiline RPAREN2 (elif-expression | else-expression))?
        ```
    -   **Elif Expression:**
        ```grammar
        elif-expression: KEYWORD:orwhen expression LPAREN2 ((expression | statements) RPAREN2 (elif-expression | else-expression)?)? (NEWLINE multiline RPAREN2 (elif-expression | else-expression))?
        ```
    -   **Else Expression:**
        ```grammar
        else-expression: KEYWORD:otherwise LPAREN2 ((expression | statements) RPAREN2)? NEWLINE multiline RPAREN2
        ```
-   **Description:**  
    These constructs manage:

    -   Looping (`while-expression`, `for-expression`) using keywords like `whenever` and `Cycle`.
    -   Function definitions with the keyword `method`.
    -   Conditionals using `when`, `orwhen`, and `otherwise` for if/elif/else branching.

    Notice the use of specialized grouping tokens (`LPAREN2` and `RPAREN2`) for these control structures.

## Operator Precedence

The grammar enforces standard operator precedence:

1. **Parentheses (`()`):**  
   Expressions within parentheses are evaluated first.
2. **Unary Operators (`+`, `-`):**  
   Applied directly to the following factor.
3. **Exponentiation (`EXP`):**  
   Evaluated before multiplication and division.
4. **Multiplication and Division (`*`, `/`):**  
   Processed in the `term` rule.
5. **Addition and Subtraction (`+`, `-`):**  
   Evaluated in the `arith-expression` rule, with left-to-right associativity.

**Examples:**

-   `3 + 4 * 2` is parsed as `3 + (4 * 2)`.
-   `-5 + (6 / 2) * 3` applies the unary operator to `5`, then computes `(6 / 2)`, multiplies the result by `3`, and finally adds `-5`.
-   `(3 + 4) * 2` forces the addition to occur before the multiplication.

## Usage Examples

Here are some valid expressions and statements according to this grammar:

-   **Arithmetic Expression:**
    ```plaintext
    3 + 5 - 2
    ```
-   **Multiplication/Division:**
    ```plaintext
    3 * 4 / 2
    ```
-   **Combined Expression:**
    ```plaintext
    -5 + (6 / 2) * 3
    ```
-   **Function Call:**
    ```plaintext
    myFunction(3, 4 + 2)
    ```
-   **Conditional Expression (Simplified):**
    ```plaintext
    when condition ( doSomething() )
    NEWLINE
    multiline block...
    ```
