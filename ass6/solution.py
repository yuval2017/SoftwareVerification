# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import re
from functools import reduce
from itertools import product, chain, combinations


def dfs(to, I, Q0, delta, L, upholds):
    def dfs_help(initial_state, states: set):
        if initial_state not in states:
            states.add(initial_state)
            curr_s, curr_q = initial_state
            t_st = list(filter(lambda x: x[0] == curr_s, to))
            sub_delta = list(filter(lambda x: x[0] == curr_q, delta))
            ans = set()
            for s, action, t in t_st:
                to_q = list(filter(lambda x: upholds(L(t), x[1]), sub_delta))
                data = [(initial_state, action, (t, x[len(x) - 1])) for x in to_q]
                ans = ans | set(data)
                for curr_initial_state in data:
                    curr_ans, curr_new_states = dfs_help(curr_initial_state[len(curr_initial_state) - 1], states)
                    ans = ans | curr_ans
                    states = curr_new_states | states
            return ans, states
        return set(), set()

    initial_states = set()
    optional_q = list(filter(lambda x: x[0] in Q0, delta))
    for initial_state in I:
        curr = list(filter(lambda x: upholds(L(initial_state), x[1]), optional_q))
        initial_states = initial_states | set([(initial_state, x[len(x) - 1]) for x in curr])

    to_ans = set()
    s_ans = set()
    for x in initial_states:
        curr_to_ans, curr_states_ans = dfs_help(x, s_ans)
        s_ans = s_ans | curr_states_ans
        to_ans = to_ans | curr_to_ans
    return initial_states, to_ans, s_ans


def TS_times_A(ts, a, upholds):
    S = ts.get('S')
    to = ts.get('to')
    L = ts.get('L')
    I = ts.get('I')

    q = a.get('q')
    delta = a.get('delta')
    Q0 = a.get('q0')

    initial_states, functions, states = dfs(to, I, Q0, delta, L, upholds)
    new_L = lambda s: s[0][1]
    act = ts.get('Act')
    return {'s': states, "act": act, 'to': functions, 'i': initial_states, 'ap': q, 'l': new_L}


def _get_literals(phi):
    symbols = {'and', 'or', 'not', '(', ')', ' '}
    return set(re.findall(r"[\w']+", phi)) - symbols


def _upholds(s, phi):
    """
    :param s: set of literals.
    :param phi: logical expression.
    :return: s |= phi

    for instance:
    upholds({'a'}, 'not(a or b) and not c') -> False
    upholds({'d'}, 'not(a or b) and not c') -> True
    upholds({'a', 'b', 'c'}, 'not(a or b) and not c') -> False
    """
    eta = {x: x in s for x in _get_literals(phi)}
    return eval(phi, None, eta)


ts = {'S': {'s1', 's5', 's0', 's2', 's3', 's4'}, 'Act': {'alpha', 'gamma', 'beta'},
      'to': {('s4', 'gamma', 's1'), ('s2', 'gamma', 's1'), ('s0', 'alpha', 's3'), ('s4', 'beta', 's5'),
             ('s5', 'beta', 's1'), ('s3', 'gamma', 's1'), ('s5', 'alpha', 's2'), ('s1', 'alpha', 's4'),
             ('s0', 'beta', 's1')}, 'I': {'s0'}, 'AP': {'a', 'b', 'c'}, 'L': lambda s:
    {'s0': {'a', 'b'}, 's1': {'a', 'b', 'c'}, 's2': {'b', 'c'}, 's3': {'a', 'c'}, 's4': {'a', 'c'},
     's5': {'a', 'c'}}[s]}

a = {'q': {'q3', 'q0', 'q1', 'q2'}, 'sigma': {'a', 'b', 'c'},
     'delta': {('q2', 'c', 'q0'), ('q1', 'a', 'q2'), ('q2', '(a or b) and not c', 'q3'),
               ('q2', 'not(a or b) and not c', 'q2'), ('q0', 'b and not c', 'q1'),
               ('q1', 'not(b and not c) and not a', 'q0'), ('q0', 'not(b and not c)', 'q0'),
               ('q1', 'b and not c and not a', 'q1')}, 'q0': {'q0'}, 'f': {'q3'}}


def print_hi(name):
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ans = TS_times_A(ts, a, _upholds)
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
