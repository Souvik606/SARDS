from Lexer import *

while True:
    text=input('code > ')
    tokens,errors=run('<stdin>',text)

    if errors: print(errors.to_string())
    else: print(tokens)