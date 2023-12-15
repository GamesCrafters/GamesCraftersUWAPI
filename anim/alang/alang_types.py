from typing import *
class Token():
    def __init__(self):
        self.pattern = '*'
class TokenDirect(Token):
    def __init__(self, tag, time, a, b):
        self.pattern = 'd' # direct
        self.tag: str = tag
        self.t: float = time
        self.a: int = a 
        self.b: int = b
    def __init__(self):
        self.pattern = 'd' # direct
    def __repr__(self):
        return f"Direct ({self.tag} {self.t} {self.a} {self.b})"
class TokenSingle(Token):
    def __init__(self):
        self.pattern = 's' # single
    def __init__(self, tag, time, a):
        self.pattern: str = "s"  # single
        self.tag: str = tag
        self.t: float = time
        self.a: int = a
    def __repr__(self):
        return f"Single ({self.tag} {self.t} {self.a})"
class TokenSpline(Token):
    def __init__(self):
        self.pattern = 'c' # curve
    def __init__(self, tag, time, points):
        self.pattern: str = "c" # curve
        self.tag: str = tag
        self.t: float = time
        self.points: List[int] = points
    def interpolate(self, a):
        pass
    def __repr__(self):
        return f"Spline ..."
class TokenSet(Token):
    def __init__(self):
        super()
    def __init__(self, sequential: bool, list):
        self.seq = sequential
        if (self.seq):
            self.pattern = "l" # list
        else:
            self.pattern = "g" # group
        self.list = list