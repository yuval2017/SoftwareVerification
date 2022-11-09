# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from functools import reduce
from itertools import product, chain, combinations


def pre(TS, C, a=None):
    set_C = [C] if type(C) is str else set(C)
    set_to = TS.get("to")
    ans = reduce(func_help_pre(set_C, a), set_to, set())
    return ans


def func_help_pre(C, a):
    def help_pre(ans, curr):
        t1, t2, t3 = curr
        if (t3 in C) and ((a is None) or (a == t2)):
            ans.add(t1)
        return ans
    return help_pre


def post(TS, C, a=None):
    set_C = [C] if type(C) is str else set(C)
    set_to = TS.get("to")
    ans = reduce(func_help_post(set_C, a), set_to, set())
    return ans


def func_help_post(C, a):
    def help_post(ans, curr):
        t1, t2, t3 = curr
        if (t1 in C) and ((a is None) or (a == t2)):
            ans.add(t3)
        return ans
    return help_post


def is_action_deterministic(TS):
    I = TS.get("I")
    S = TS.get("S")
    Act = TS.get("Act")
    return len(I) <= 1 and all(len(post(TS, s, a)) <= 1 for s, a in product(S, Act))


def is_label_deterministic(TS):
    I = TS.get("I")
    S = TS.get("S")
    AP = TS.get("AP")
    L = TS.get("L")
    return len(I) <= 1 and all(
        len(list(filter(lambda s_tag: L(s_tag) == A, post(TS, s)))) <= 1 for s, A in product(S, power_set(AP)))


def power_set(AP):
    lst = list(AP)
    ans = [[]]
    for element in lst:
        curr = [a + [element] for a in ans]
        ans += curr
    return list(map(lambda s: set(s) if s else {}, ans))


TS = {
    "S": {"s1", "s2", "s3"},
    "I": {"s1"},
    "Act": {"a", "b", "c"},
    "to": {("s1", "a", "s2"), ("s1", "a", "s1"), ("s1", "b", "s2"),
           ("s2", "c", "s3"), ("s3", "c", "s1")},
    "AP": {"p", "q"},
    "L": lambda s: {"p"} if s == "s1" else {} if s == "s2" else {}
}


def print_hi(name):
    ans = power_set(TS.get("AP"))
    ans = post(TS,{"s1","s2","s3"},"a")
    i = 1
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
