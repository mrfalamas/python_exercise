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


def mergetwolists(list1, list2):

    for elem in list2:
        list1.append(elem)

    for i in range(len(list1)):
        for j in range(len(list1) - i -1):
            if list1[j] > list1[j+1]:
                list1[j],list1[j+1] = list1[j+1], list1[j]

    return list1


l1 = [1, 3, 4]

l2 = [3, 1, 2]

print(mergetwolists(l1, l2))