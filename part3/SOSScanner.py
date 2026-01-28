import re
from functools import reduce
from time import time
import argparse
import pdb
import sys
sys.path.append("../part2/")
from tokens import tokens,Token,Lexeme
from typing import Callable,List,Tuple,Optional


# No line number this time
class ScannerException(Exception):
    pass

class SOSScanner:
    def __init__(self, tokens: List[Tuple[Token,str,Callable[[Lexeme],Lexeme]]]) -> None:
        self.tokens = tokens

    def input_string(self, input_string:str) -> None:
        self.istring = input_string

    def token(self) -> Optional[Lexeme]:
        # keep track of longest match
        while True:
            if len(self.istring) == 0:
                return None

            matches = []
            # try all tokens
            for tok, regex, action in self.tokens:
                m = re.match(regex, self.istring)
                if m:
                    matches.append((tok, m, action))

            if not matches:
                raise ScannerException()

            # get longest match
            longest = max(matches, key=lambda x: len(x[1][0]))

            # get return value 
            ret = longest[2](Lexeme(longest[0], longest[1][0]))

            # chop input string
            chop = len(ret.value)
            self.istring = self.istring[chop:]

            # return non ignore tokens
            if ret.token != Token.IGNORE:
                return ret

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()
    
    f = open(args.file_name)    
    f_contents = f.read()
    f.close()

    verbose = args.verbose

    s = SOSScanner(tokens)
    s.input_string(f_contents)

    start = time()
    while True:
        t = s.token()
        if t is None:
            break
        if (verbose):
            print(t)
    end = time()
    print("time to parse (seconds): ",str(end-start))
