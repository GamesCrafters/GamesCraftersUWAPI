import os
from .reader import clean
from .interpreter import uni_conversion
from .lexer import *

def parse(file_name, debug=False):
    """
    Given an ALANG file decompose the animation into something that can be passed to the server
    """
    with open(file_name) as f: s = f.read()
    read = clean(s)
    if debug:
        print("reading, ", s)
    # tokenize
    tokenized = tokenize(read)
    if debug:
        print("tokenized as, ", tokenized, len(tokenized))
    # dictionary ify to send
    uni_representation = uni_conversion(tokenized)
    return uni_representation
class CustomAnimations():
    def __init__(self, mapping: dict ={}):
        self.animation: dict = mapping # Mappings {"condition" : file name}
    def trigger(self, previous_position: str, current_position: str):
        parsed = self._parse_condition(previous_position, current_position)
        if (parsed):
            return parse(self.animation[parsed])
        return None
    def _parse_condition(self, previous_position: str, current_position: str) -> str:
        valid_keys = []
        for cond in self.animation.keys():
            print(cond, current_position)
            assert len(previous_position) == len(current_position)
            valid = True
            for i in range(len(cond)):
                condition_dc = cond[i] == "~"
                condition_pdc = cond[i] == "*" and current_position[i] == "x" or current_position[
                    i] == "o"
                condition_uneven = cond[i] == current_position[i]
                if (not condition_uneven and not (condition_dc or condition_pdc)):
                    valid = False
                    continue
            if (valid):
                valid_keys.append(cond)
        # TODO for now assume only one valid key per animation
        if (len(valid_keys) == 0):
            return None
        return self.animation[valid_keys[0]]
    
class DodgemAnimations(CustomAnimations):
    """
    Used to specify conditions for custom animations
    """
    def __init__(self, mapping: dict ={}):
        super().__init__(mapping)
    def trigger(self, previous_position: str, current_position: str):
        parsed = self._parse_condition(previous_position, current_position)
        if (parsed):
            return parse(self.animation[parsed])
        return None
    def _parse_condition(self, previous_position: str, current_position: str) -> str:
        assert len(previous_position) == len(current_position)
        before = 0
        after = 0
        for j in range(len(previous_position)):
            before += previous_position[j] == "o" or previous_position[j] == "x"
            after += current_position[j] == "o" or current_position[j] == "x"
        return "falling" if after < before else None