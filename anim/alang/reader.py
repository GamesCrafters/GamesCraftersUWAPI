import os
from typing import *

def clean(dirty: str)-> List[str]: 
    """
    Cleans dirty string and remove redundant characters
    """
    return [c for c in dirty if not (c == " " or c == "\n")]
