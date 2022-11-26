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
                    sub_to1 = list(filter(lambda x: x[0] == initial[0] and x[1] == a, to1))
                    sub_to2 = list(filter(lambda x: x[0] == initial[1] and x[1] == a, to2))
                    t = list(product(sub_to1, sub_to2))
                    curr = [(i[0][2], i[1][2]) for i in t]
                    post = post + curr

                else:
                    sub_to1 = list(filter(lambda x: x[0] == initial[0] and x[1] == a, to1))
                    sub_to2 = list(filter(lambda x: x[0] == initial[1] and x[1] == a, to2))
                    curr = [(initial[0], i[2]) for i in sub_to2] + [(i[2], initial[1]) for i in sub_to1]
                    post = post + curr

                ans = ans + [(initial, a, i) for i in curr]

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
    AP1 = ts1.get('AP')
    L1 = ts1.get('L')

    Act2 = ts2.get('Act')
    to2 = ts2.get('to')
    I2 = ts2.get('I')
    AP2 = ts2.get('AP')
    L2 = ts2.get('L')

    I = set(product(I1, I2))
    S, to = create_to_and_S(I, to1, to2, h, Act1.union(Act2))
    Act = Act1.union(Act2)
    AP = AP1.union(AP2)
    L = lambda s: L1(s[0]).union(L2(s[1]))
    return {'S': S, 'Act': Act, 'to': to, 'I': I, 'AP': AP, 'L': L}


peterson0 = {'Loc': {'crit', 'noncrit', 'wait'},
             'Act': {'', 'b0=True;x=1', 'b0=False'},
             'Eval': evaluate,
             'Effect': effect,
             'to': {('noncrit', 'True', 'b0=True;x=1', 'wait'), ('wait', 'x==0 or not b1', '', 'crit'),
                    ('crit', 'True', 'b0=False', 'noncrit')},
             'Loc0': {'noncrit'},
             'g0': 'not b0'}
peterson1 = {'Loc': {'crit', 'noncrit', 'wait'},
             'Act': {'', 'b1=True;x=0', 'b1=False'},
             'Eval': evaluate,
             'Effect': effect,
             'to': {('noncrit', 'True', 'b1=True;x=0', 'wait'), ('crit', 'True', 'b1=False', 'noncrit'),
                    ('wait', 'x==1 or not b0', '', 'crit')},
             'Loc0': {'noncrit'},
             'g0': 'not b1'}


def create_to_and_lock(Loc0, to1, to2):
    def help_dfs(initial, to1, to2, Loc):
        ans = []
        if initial not in Loc:
            Loc.add(initial)
            sub_to1 = list(filter(lambda x: x[0] == initial[0], to1))
            sub_to2 = list(filter(lambda x: x[0] == initial[1], to2))
            post = [(i[3], initial[1]) for i in sub_to1] + [(initial[0], i[3]) for i in sub_to2]
            ans = [(initial, i[1], i[2], (i[3], initial[1])) for i in sub_to1] + [
                (initial, i[1], i[2], (initial[0], i[3])) for i in sub_to2]
            for p in post:
                ans = ans + help_dfs(p, to1, to2, Loc)
        return ans

    Loc = set()
    to = []
    for l in Loc0:
        to = to + help_dfs(l, to1, to2, Loc)
    return Loc, set(to)


def interleave_program_graphs(pg1, pg2):
    Act1 = pg1.get('Act')
    Eval1 = pg1.get('Eval')
    Effect1 = pg1.get("Effect")
    to1 = pg1.get('to')
    Loc01 = pg1.get('Loc0')
    g01 = pg1.get('g0')
    # 2 nd pg
    Act2 = pg2.get('Act')
    Eval2 = pg2.get('Eval')
    Effect2 = pg2.get("Effect")
    to2 = pg2.get('to')
    Loc02 = pg2.get('Loc0')
    g02 = pg2.get('g0')

    Loc0 = set(product(Loc01, Loc02))
    Act = Act1.union(Act2)
    Eval = Eval1
    Effect = Effect1
    g0 = g01 + ' and ' + g02
    Loc, to = create_to_and_lock(Loc0, to1, to2)
    return {'Loc': Loc, 'Act': Act, 'Eval': Eval, 'Effect': Effect, 'to': to, 'Loc0': Loc0, 'g0': g0}


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    i = interleave_program_graphs(peterson0, peterson1)
    t = interleave_transition_systems(ts1, ts2, {'a', 'b'})

    j = 1
