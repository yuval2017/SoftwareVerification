# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from itertools import product


class HashableDict(dict):
    def __hash__(self):
        return hash(frozenset(self.items()))


def effect(act, eta):
    eta = HashableDict(eta)
    exec(act, None, eta)
    return eta


def evaluate(cond, eta):
    return eval(cond, None, eta)


def transition_system_from_program_graph(pg, vars, labels):
    Loc = pg.get('Loc')
    Loc0 = pg.get('Loc0')
    Act = pg.get('Act')
    Eval = pg.get('Eval')
    Effect = pg.get('Effect')
    to = pg.get('to')
    g0 = pg.get('g0')


def create_to_and_S(I, to1, to2, h, Act):
    def help_dfs(initial, to1, to2, S, h):
        ans = []
        post = []
        if initial not in S:
            S.add(initial)
            for a in Act:
                if a in h:
                    sub_to1 = filter(lambda x: x[0] == initial[0] and x[1] == a, to1)
                    sub_to2 = filter(lambda x: x[0] == initial[1] and x[1] == a, to2)
                    to_list = list(product(sub_to1, sub_to2))
                    post = post + [(i[0][2], i[1][2]) for i in to_list]
                else:
                    sub_to1 = list(filter(lambda x: x[0] == initial[0] and x[1] == a, to1))
                    post = post + [(i[2], initial[1]) for i in sub_to1]
                    sub_to2 = list(filter(lambda x: x[0] == initial[1] and x[1] == a, to2))
                    post = post + [(initial[0], i[2]) for i in sub_to2]
                ans = ans + [(initial, a, i) for i in post]

            for p in post:
                t = help_dfs(p, to1, to2, S, h)
                ans = ans + t
        return ans

    S = set()
    to = []
    for i in I:
        to = to + help_dfs(i, to1, to2, S, h)
    return S, set(to)


def interleave_transition_systems(ts1, ts2, h):
    Act1 = ts1.get('Act')
    to1 = ts1.get('to')
    I1 = ts1.get('I')
    L1 = ts1.get('L')

    Act2 = ts2.get('Act')
    to2 = ts2.get('to')
    I2 = ts2.get('I')
    L2 = ts2.get('L')

    I = product(I1, I2)
    S, to = create_to_and_S(I, to1, to2, h, Act1.union(Act2))
    Act = Act1.union(Act2)
    L = lambda s: L1(s[0]).union(L2(s[1]))
    return {'S': S, 'Act': Act, 'to': to, 'I': I, 'L': L}


def interleave_program_graphs(pg1, pg2):
    Lock1 = pg1.get('Lock')
    Act1 = pg1.get('Act')
    Eval1 = pg1.get('Eval')
    Effect1 = pg1.get("Effect")
    to1 = pg1.get('to')
    Lock01 = pg1.get('Lock0')
    g01 = pg1.get('g0')
    # 2 nd pg
    Lock2 = pg2.get('Lock')
    Act2 = pg2.get('Act')
    Eval2 = pg2.get('Eval')
    Effect2 = pg2.get("Effect")
    to1 = pg2.get('to')
    Lock02 = pg2.get('Lock0')
    g02 = pg2.get('g0')

    Lock = product(Lock01, Lock02)
    Act = Act1.union(Act2)
    Effect1 = Effect1
    g0 = g01 + 'and' + g02





ts1 = {'S': {'s1', 's3', 's2'},
       'Act': {'b', 'd', 'a'},
       'to': {('s2', 'd', 's3'), ('s1', 'a', 's2'), ('s2', 'b', 's1')},
       'I': {'s1'}, 'AP': {'b', 'a'},
       'L': {}}
ts2 = {'S': {'s4', 's5'},
       'Act': {'b', 'a', 'c'},
       'to': {('s4', 'a', 's5'), ('s5', 'b', 's5'), ('s5', 'c', 's4')},
       'I': {'s4'}, 'AP': {'b', 'a'},
       'L': {}}


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    interleave_transition_systems(ts1, ts2, {'a', 'b'})
    j = 1
