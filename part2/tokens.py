from enum import Enum

class Token(Enum):
    ID     = "ID"
    NUM    = "NUM"
    IGNORE = "IGNORE"

    # new tokens
    HNUM   = "HNUM"
    INCR   = "INCR"
    PLUS   = "PLUS"
    MULT   = "MULT"
    SEMI   = "SEMI"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    ASSIGN = "ASSIGN"
    IF     = "IF"
    ELSE   = "ELSE"
    WHILE  = "WHILE"
    INT    = "INT"
    FLOAT  = "FLOAT"

class Lexeme:
    def __init__(self, token:Token, value:str) -> None:
        self.token = token
        self.value = value

    def __str__(self):
        return "(" + str(self.token) + "," + "\"" + self.value + "\"" + ")"

def idy(l:Lexeme) -> Lexeme:
    return l

# identify and check for keywords
def id_action(l:Lexeme) -> Lexeme:
    keywords = {
        "if": Token.IF,
        "else": Token.ELSE,
        "while": Token.WHILE,
        "int": Token.INT,
        "float": Token.FLOAT,
    }
    tok = keywords.get(l.value)
    if tok is not None:
        return Lexeme(tok, l.value)
    return l

# list of tokens for the scanner
tokens = [
    (Token.IGNORE, r"[ \t\n]+", idy),
    (Token.INCR,   r"\+\+", idy),
    (Token.PLUS,   r"\+",   idy),
    (Token.MULT,   r"\*",   idy),
    (Token.SEMI,   r";",    idy),
    (Token.LPAREN, r"\(",   idy),
    (Token.RPAREN, r"\)",   idy),
    (Token.LBRACE, r"\{",   idy),
    (Token.RBRACE, r"\}",   idy),
    (Token.ASSIGN, r"=",    idy),
    (Token.HNUM, r"0[xX][0-9a-fA-F]+", idy),
    (Token.NUM, r"(?:[0-9]+(?:\.[0-9]+)?)|(?:\.[0-9]+)", idy),
    (Token.ID, r"[A-Za-z][A-Za-z0-9]*", id_action),
]
