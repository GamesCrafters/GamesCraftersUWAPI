from typing import *
from .alang_types import *
def tokenize(clean: List[str]) -> List[Token]:
    tokens = []
    while (len(clean) > 0):
        c = clean.pop(0)
        if (c == 'm' or c == 'r' or c == 's' or c == 'o' or c == 'i'):
            # direct tokens
            open_bracket = clean.pop(0)
            assert(open_bracket == "(")
            time: float = extractFloat(clean)
            assert(clean.pop(0) == ")")
            assert(clean.pop(0) == "_")
            r1 = extractInt(clean)
            r2 = 0
            if (not c == 'o' and not c == 'i'):
                assert(clean.pop(0) == "_")
                r2 = extractInt(clean)
            t: TokenDirect = TokenDirect()
            t.pattern = "d"
            t.t = time
            t.a = r1
            t.b = r2
            t.tag = c
            tokens.insert(-1, t)
        elif (c == 'w'):
            # single tokens
            open_bracket = clean.pop(0)
            assert(open_bracket == "(")
            time: float = extractFloat(clean)
            assert(clean.pop(0) == ")")
            r1 = extractInt(clean)
            if (c != 'w'):
                assert(clean.pop(0) == "_")
                r2 = extractInt(clean)
            t: TokenSingle = TokenSingle()
            t.t = time
            t.a = r1
            t.tag = c
            tokens.insert(-1, t)
        elif (c == '(' or c == '['):
            # grouping or sequence
            assert NotImplementedError("Currently Not Suppported")
        elif (c == ','):
            # whitelisted tokens
            assert NotImplementedError("Currently Not Suppported")
        else:
            # error case
            assert False, f"Error starting at: {c + clean}"
    tokens.reverse()
    return tokens
def extractInt(lst):
    """
    Extracting the Integer
    """
    integer_string = ""
    while(lst and lst[0].isdigit()):
        integer_string += lst.pop(0)
    return int(integer_string)

def extractFloat(lst):
    float_string = ""
    period = False
    while(lst and lst[0].isdigit() or (not period and lst[0] == '.')):
        if (not period and lst[0] == '.'):
            period = True
        elif (period and lst[0] == '.'):
            assert False, f"Error parsing float"
        float_string += lst.pop(0)
    return float(float_string)