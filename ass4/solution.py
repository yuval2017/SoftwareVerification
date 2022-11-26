# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import networkx as nx
from itertools import product


class HashableDict(dict):
    def __hash__(self):
        return hash(frozenset(self.items()))


def create_initial_states(Loc0, g0, vars, Eval):
    vals = [i[1] for i in vars.items()]
    l_product_eta = product(*vals)
    guu = [HashableDict(zip(vars.keys(), i)) for i in l_product_eta]
    return frozenset(product(Loc0, filter(lambda x: Eval(g0, x), guu)))


def create_to(I, to, effect, Eval):
    def help(initial_state, done_set):
        ans = []
        if initial_state not in done_set:
            done_set.add(initial_state)
            eta = initial_state[1]
            l_s = list(filter(lambda s: s[0] == initial_state[0] and Eval(s[1], eta), to))
            ans = [(initial_state, x[2], (x[-1], HashableDict(effect(x[-2], eta)))) for x in l_s]
            for s in ans:
                ans = ans + help(s[-1], done_set)
        return ans

    ans = []
    S = set()
    for i in I:
        ans = ans + help(i, S)
    return S, frozenset(ans)


def transition_system_from_program_graph(pg, vars, labels):
    Loc = pg.get('Loc')
    Loc0 = pg.get('Loc0')
    Act = pg.get('Act')
    Eval = pg.get('Eval')
    Effect = pg.get('Effect')
    to = pg.get('to')
    g0 = pg.get('g0')

    I = create_initial_states(Loc0, g0, vars, Eval)
    AP = labels.union(Loc)
    S, to = create_to(I, to, Effect, Eval)
    L = lambda s: {s[0]}.union(filter(lambda label: Eval(label, s[1]), labels))
    return {'S': S, 'Act': Act, 'to': to, 'I': I, 'AP': AP, 'L': L}


def evaluate(cond, eta):
    return {
        'true': lambda eta: True,
        'ncoke > 0': lambda eta: eta['ncoke'] > 0,
        'nsprite > 0': lambda eta: eta['nsprite'] > 0,
        'ncoke=0 && nsprite=0': lambda eta: eta['ncoke'] == 0 and eta['nsprite'] == 0,
        'ncoke=2 && nsprite=2': lambda eta: eta['ncoke'] == 2 and eta['nsprite'] == 2,
    }[cond](eta)


def effect(act, eta):
    return {
        'coin': lambda eta: eta,
        'ret_coin': lambda eta: eta,
        'refill': lambda eta: {'ncoke': 2, 'nsprite': 2},
        'get_coke': lambda eta: {**eta, 'ncoke': eta['ncoke'] - 1},
        'get_sprite': lambda eta: {**eta, 'nsprite': eta['nsprite'] - 1},
    }[act](eta)

#ff
pg = {
    'Loc': {'start', 'select'},
    'Loc0': {'start'},
    'Act': {'coin', 'refill', 'get_coke', 'get_sprite', 'ret_coin'},
    'Eval': evaluate,
    'Effect': effect,
    'to': {
        ('start', 'true', 'coin', 'select'),
        ('start', 'true', 'refill', 'start'),
        ('select', 'ncoke > 0', 'get_coke', 'start'),
        ('select', 'nsprite > 0', 'get_sprite', 'start'),
        ('select', 'ncoke=0 && nsprite=0', 'ret_coin', 'start')
    },
    'g0': "ncoke=2 && nsprite=2",
}

vars = {'ncoke': range(3), 'nsprite': range(3)}

labels = {"ncoke > 0", "nsprite > 0"}


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gp = transition_system_from_program_graph(pg, vars, labels)
    ss = gp.get('L')(('select', {'ncoke': 1, 'nsprite': 1}))

    j = 1
