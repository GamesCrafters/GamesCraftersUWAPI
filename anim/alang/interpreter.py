from typing import *
from .alang_types import *
def uni_conversion(chain: List[Token]) -> List[Dict]:
    """
    Convert Tokens to a way UNI can understand it given a chain of stuff
    """
    dict_list = []
    for t in chain:
        if (t.pattern is 'd'):
            # direct tokens
            dict_list.append({
                "tag": t.tag,
                "time": t.t,
                "a": t.a,
                "b": t.b}
                )
        elif (t.pattern == "s"):
            # single tokens
            dict_list.append({
                "tag": t.tag,
                "time": t.t,
                "a": t.a
                })
        elif (t.pattern == "l" or t.pattern == "g"):
            # grouping or sequence
            assert NotImplementedError("Currently Not Suppported")
        elif (t.pattern == "c"):
            # whitelisted tokens
            assert NotImplementedError("Currently Not Suppported")
    return dict_list