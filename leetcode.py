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

#print(validate_paranthesis("([])"))


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

#print(mergetwolists(l1, l2))


def ret_id(inp):

    lst = {1,3,3,4,5,6,6,7,8,9,9}

    for i, elem in enumerate(lst):
        if elem == inp:
            temp.append(i)

    return temp

#print(ret_id(3))


def remove_duplicates(lst):
    t = len(lst)

    unique_lst = []

    for elem in lst:
        if elem not in unique_lst:
            unique_lst.append(elem)

    list_digits = unique_lst

    digits = len(list_digits)

    msg = str(digits) + ", nums = " + ''.join(str(list_digits))

    return msg

#print(remove_duplicates([0,0,3,3,3,3,3,3,4]))


def ret_occ(ac, paie):
    if ac in paie:
        print('ok') 

    print(paie.find(ac))


#print(ret_occ("bad","sadbutsad"))

def ret_word(inp):
    new_lst = inp.split(" ")
    print(new_lst)
    new_lst2 = []
    for elem in new_lst:
        if elem:
            new_lst2.append(elem)
    return new_lst2[len(new_lst2) - 1]


# print(ret_word("   fly me   to   the moon  "))


def ret_sum(a, b):

    a_int = 0
    b_int = 0

    for i, let in enumerate(a):
        if let == '1':
            a_int = a_int + pow(2,i)

    for j, let in enumerate(b):
        if let == '1':
            b_int = b_int + pow(2,j)


    c_int = a_int + b_int
    sum = bin(c_int)

    sum = sum.replace('0b', '')

    return sum

# print(ret_sum("1010","1011"))