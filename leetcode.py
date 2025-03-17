"""This module is used for exercising python small algorithms"""


def validate_paranthesis(in_str):
    """function that validates paranthesis"""
    in_stack = []
    mapping = {
        "(":")",
        "[":"]",
        "{":"}"
    }

    for s in in_str:
        if s in mapping:
            in_stack.append(s)
        else:
            last_char = in_stack.pop()
            if s == mapping[last_char]:
                # it is good
                print(last_char + " matched with " + s)
            else:
                return False

    if len(in_stack) == 0:
        return True
    else:
        return False

inp_str = "([])"




