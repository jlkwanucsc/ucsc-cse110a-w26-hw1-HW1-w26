import string
import argparse
from time import time
from enum import Enum
from typing import Optional

class ScannerException(Exception):
    pass

class StringStream:
    def __init__(self, input_string: str) -> None:
        self.string = input_string

    def is_empty(self) -> bool:
        return len(self.string) == 0

    def peek_char(self) -> Optional[str]:
        if not self.is_empty():            
            return self.string[0]
        return None

    def eat_char(self) -> None:
        # take the first character off the string
        self.string = self.string[1:]

# put characters to ignore in this array        
IGNORE = [" ", "\n"]
NUMS   = [str(x) for x in range(10)]

# From: https://www.adamsmith.haus/python/answers/how-to-make-a-list-of-the-alphabet-in-python
alphabet_string = string.ascii_lowercase
CHARS = list(alphabet_string)

class Token(Enum):
    ADD    = "ADD"
    MULT   = "MULT"
    ASSIGN = "ASSIGN"
    SEMI   = "SEMI"
    ID     = "ID"
    NUM    = "NUM"

    # new token
    INCR   = "INCR" 

class Lexeme:
    def __init__(self, token:Token, value:str) -> None:
        self.token = token
        self.value = value

    def __str__(self):
        return "(" + str(self.token) + "," + "\"" + self.value + "\"" + ")"

class NaiveScanner:

    def __init__(self, input_string:str) -> None:
        self.ss = StringStream(input_string)

    def token(self) -> Optional[Lexeme]:

        # First handle the ignore case
        while self.ss.peek_char() in IGNORE:
            self.ss.eat_char()

        # If there is nothing to return, return None
        if self.ss.is_empty():
            return None

        # handle addition
        if self.ss.peek_char() == "+":
            # check for increment
            if len(self.ss.string) >= 2 and self.ss.string[1] == "+":
                self.ss.eat_char()
                self.ss.eat_char()
                return Lexeme(Token.INCR, "++")
            # otherwise just addition
            self.ss.eat_char()
            return Lexeme(Token.ADD, "+")

        # handle multiplication
        if self.ss.peek_char() == "*":
            self.ss.eat_char()
            return Lexeme(Token.MULT, "*")

        if self.ss.peek_char() == "=":
            self.ss.eat_char()
            return Lexeme(Token.ASSIGN, "=")

        if self.ss.peek_char() == ";":
            self.ss.eat_char()
            return Lexeme(Token.SEMI, ";")

        # handle identifiers
        if self.ss.peek_char() in CHARS:
            value = ""
            # get first character
            value += self.ss.peek_char()
            self.ss.eat_char()
            # get remaining characters
            while (self.ss.peek_char() in CHARS) or (self.ss.peek_char() in NUMS):
                value += self.ss.peek_char()
                self.ss.eat_char()
            return Lexeme(Token.ID, value)

        # handle numbers
        if (self.ss.peek_char() in NUMS) or (self.ss.peek_char() == "."):
            value = ""
            seen_dot = False

            # get leading dot portion
            if self.ss.peek_char() == ".":
                seen_dot = True
                value += "."
                self.ss.eat_char()
                if self.ss.peek_char() not in NUMS:
                    raise ScannerException("Malformed number: missing digits after '.'")
                while self.ss.peek_char() in NUMS:
                    value += self.ss.peek_char()
                    self.ss.eat_char()
                return Lexeme(Token.NUM, value)

            # get integer portion
            while self.ss.peek_char() in NUMS:
                value += self.ss.peek_char()
                self.ss.eat_char()

            # get trailing dot portion
            if (self.ss.peek_char() == ".") and (not seen_dot):
                seen_dot = True
                value += "."
                self.ss.eat_char()
                if self.ss.peek_char() not in NUMS:
                    raise ScannerException("Malformed number: missing digits after '.'")
                while self.ss.peek_char() in NUMS:
                    value += self.ss.peek_char()
                    self.ss.eat_char()

            return Lexeme(Token.NUM, value)

        # if we cannot match a token, throw an exception
        # you should implement a line number to pass
        # to the exeception
        raise ScannerException("Unrecognized character: " + str(self.ss.peek_char()))
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()
    
    f = open(args.file_name)    
    f_contents = f.read()
    f.close()

    verbose = args.verbose

    s = NaiveScanner(f_contents)

    start = time()
    while True:
        t = s.token()
        if t is None:
            break
        if (verbose):
            print(t)
    end = time()
    print("time to parse (seconds): ",str(end-start))
