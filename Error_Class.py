"""
Module: Position and Error_tracking

This module provides utility classes for tracking the position of characters in an input text
and handling errors encountered during tokenization or parsing.

Classes:
- Position: Maintains the current position in the input text, including index, line, and column.
- Error: Serves as a base class for error handling, storing details about errors that occur.
- IllegalCharError: A specific error subclass for handling illegal character occurrences.
"""

class Position:
    """Tracks the current position in the input text, including index, line, and column."""

    def __init__(self, index, line, col, file_name, file_text):
        self.index = index  # The current character index in the input text.
        self.line = line  # The current line number in the input text.
        self.col = col  # The current column number in the input text.
        self.file_name = file_name  # The name of the file being processed.
        self.file_text = file_text  # The full content of the file being processed.

    def advance(self, current_char):
        """
        Moves the position forward by one character.

        If the character is a newline ('\n'), it increments the line number
        and resets the column number. Otherwise, it simply increments the column number.

        Parameters:
        - current_char (str): The character currently being processed.

        Returns:
        - Position: The updated position object.
        """
        self.index += 1
        self.col += 1
        if current_char == '\n':
            self.line += 1
            self.col = 0
        return self

    def copy(self):
        """
        Creates and returns a copy of the current position.

        Returns:
        - Position: A new instance of Position with the same values.
        """
        return Position(self.index, self.line, self.col, self.file_name, self.file_text)

class Error:
    """Represents a general error encountered during tokenization or parsing."""

    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start  # The starting position of the error.
        self.pos_end = pos_end  # The ending position of the error.
        self.error_name = error_name  # The name/type of the error.
        self.details = details  # Additional details about the error.

    def to_string(self):
        """
        Formats and returns the error message.

        Returns:
        - str: A formatted error message containing the error name, details,
               and file location information.
        """
        return f'{self.error_name}: {self.details}\nFile {self.pos_start.file_name}, line {self.pos_start.line + 1}'

class IllegalCharError(Error):
    """Handles errors caused by illegal characters in the input text."""

    def __init__(self, pos_start, pos_end, details):
        """
        Initializes an IllegalCharError instance.

        Parameters:
        - pos_start (Position): The starting position of the illegal character.
        - pos_end (Position): The ending position of the illegal character.
        - details (str): Additional information about the error.
        """
        super().__init__(pos_start, pos_end, 'Illegal Character', details)
