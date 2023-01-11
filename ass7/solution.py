from abc import ABC, abstractmethod
from typing import Union
from itertools import product


class LTL(ABC):
    def _sub(self):
        return {self.simplify(), _Not_(self).simplify()}

    @abstractmethod
    def sub(self):
        pass

    def simplify(self):
        return self


class Literal(LTL):

    def __init__(self, x: Union[str, bool, int]):
        super().__init__()
        self.x = x

    def __repr__(self):
        return str(self.x)

    def tex(self):
        return str(self.x)

    def sub(self):
        return self._sub()

    def __eq__(self, other):
        return isinstance(other, Literal) and self.x == other.x or isinstance(other, bool) and self.x == other

    def __hash__(self):
        return hash(self.x)


class Unary(LTL):
    def __init__(self, phi: Union[LTL, str, bool, int], op: str, texop: str):
        super().__init__()
        self.phi = phi if isinstance(phi, LTL) else Literal(phi)
        self.op = op
        self.texop = texop

    def __repr__(self):
        return f'{self.op}({self.phi})'

    def tex(self):
        return f'{self.texop}({self.phi.tex()})'

    def sub(self):
        return self._sub() | self.phi.sub()

    def __eq__(self, other):
        return self.phi == other.phi and self.op == other.op and self.texop == other.texop

    def __hash__(self):
        return hash((self.phi, self.op, self.texop))


class Binary(LTL):
    def __init__(self, phi1: Union[LTL, str, bool, int], phi2: Union[LTL, str], op: str, texop: str):
        super().__init__()
        self.phi1 = phi1 if isinstance(phi1, LTL) else Literal(phi1)
        self.phi2 = phi2 if isinstance(phi2, LTL) else Literal(phi2)
        self.op = op
        self.texop = texop

    def __repr__(self):
        return f'({self.phi1} {self.op} {self.phi2})'

    def tex(self):
        return f'({self.phi1.tex()} {self.texop} {self.phi2.tex()})'

    def sub(self):
        return self._sub() | self.phi1.sub() | self.phi2.sub()

    def __eq__(self, other):
        return self.phi1 == other.phi1 and self.phi2 == other.phi2 and self.op == other.op and self.texop == other.texop

    def __hash__(self):
        return hash((self.phi1, self.phi2, self.op, self.texop))


class _Not_(Unary):
    def __init__(self, phi):
        super().__init__(phi, 'Not', '\\neg')

    def simplify(self):
        phi = self.phi.simplify()
        if isinstance(phi, _Not_):
            return phi.phi
        return _Not_(phi)


def Not(phi):
    return _Not_(phi).simplify()


class Next(Unary):
    def __init__(self, phi):
        super().__init__(phi, 'O', '\\mathbf{O}')


class Until(Binary):
    def __init__(self, phi1, phi2):
        super().__init__(phi1, phi2, 'U', '\\cup')


class And(Binary):
    def __init__(self, phi1, phi2):
        super().__init__(phi1, phi2, '/\\', '\\land')


class Eventually(Until):
    def __init__(self, phi):
        super().__init__(True, phi)


class Release(_Not_):
    def __init__(self, phi1, phi2):
        super().__init__(Until(Not(phi1), Not(phi2)))


class Always(_Not_):
    def __init__(self, phi):
        super().__init__(Eventually(Not(phi)))


class Or(_Not_):
    def __init__(self, phi1, phi2):
        super().__init__(And(Not(phi1), Not(phi2)))


class Implies(Or):
    def __init__(self, phi1, phi2):
        super().__init__(Not(phi1), phi2)


def get_all_subsets(B):
    res = [[]]
    for e in B:
        res += [sub + [e] for sub in res]
    return frozenset(frozenset(s) for s in res)


def implies(A_bool, B_bool):
    return (not A_bool) or B_bool


def if_and_only_if(A_bool, B_bool):
    return (implies(A_bool, B_bool) and implies(B_bool, A_bool))


def get_q(clouser):
    def max_check(B):
        return all(implies((phi not in B), (Not(phi) in B)) for phi in clouser)

    def locality_trace_check(B):
        unarity_exprs = set(filter(lambda x: isinstance(x, Until), clouser))
        return all(
            implies((phi.phi2 in B), (phi in B)) and implies(((phi in B) and (phi.phi2 not in B)), phi.phi1 in B) for
            phi in unarity_exprs)

    def logic_trace_check(B):
        true_is_in_closer = any(Literal(True) == phi for phi in clouser)
        and_exprs = frozenset(filter(lambda x: isinstance(x, And), clouser))
        return all(((implies((phi in B), ((phi.phi1 in B) and (phi.phi2 in B))),
                     implies(((phi.phi1 in B) and (phi.phi2 in B)), (phi in B)))) for phi in and_exprs) and (all(
            implies((phi in B), (Not(phi) not in B)) for phi in B)) and (
                   implies(true_is_in_closer, (Literal(True) in B)))

    subsets = get_all_subsets(clouser)
    return frozenset(
        filter(lambda B: max_check(B) and logic_trace_check(B) and locality_trace_check(B), subsets))


def get_to(q_0, q, closure):
    def check_cond_1(B):
        next_exprs = filter(lambda phi: isinstance(phi, Next), closure)
        return frozenset(
            filter(lambda B_tag: all(if_and_only_if((phi in B), (phi.phi in B_tag)) for phi in next_exprs), q))

    def check_cond_2(B):
        unarity_exprs = frozenset(filter(lambda x: isinstance(x, Until), closure))
        cond1 = frozenset(filter(
            lambda B_tag: all(implies(((phi in B) and (phi.phi2 not in B)), (phi in B_tag)) for phi in unarity_exprs),
            q))
        cond2 = frozenset(filter(
            lambda B_tag: all(
                implies(((phi not in B) and (phi.phi1 in B)), (phi not in B_tag)) for phi in unarity_exprs),
            q))
        ans = cond1 & cond2
        return ans

    def dfs_helper(initial, q_set):
        delta = frozenset()
        A = frozenset(filter(lambda x: isinstance(x, Literal), (initial.difference({Literal(True)}))))
        if initial not in q_set:
            q_set = q_set | {initial}
            all_to_opt = check_cond_1(initial) & check_cond_2(initial)
            for curr_q in all_to_opt:
                curr_q, curr_delta = dfs_helper(curr_q, q_set)
                delta = delta | curr_delta
                q_set = q_set | curr_q
            return q_set, (delta | frozenset([(initial, A, B_tag) for B_tag in all_to_opt]))
        return frozenset(), frozenset()

    ans_q = frozenset()
    ans_delta = frozenset()
    for initial in q_0:
        curr_q, curr_delta = dfs_helper(initial, ans_q)
        ans_delta = ans_delta | curr_delta
        ans_q = ans_q | curr_q
    return ans_q, ans_delta


def get_f(closure, q):
    unarity_exprs = frozenset(filter(lambda x: isinstance(x, Until), closure))
    ans = frozenset()
    for unarity in unarity_exprs:
        curr = frozenset(filter(lambda B: (unarity not in B) or (unarity.phi2 in B), q))
        ans = ans | {curr}
    return ans


def ltl_to_gnba(phi):
    clouser = phi.sub()
    q = get_q(clouser)
    q_0 = frozenset(filter(lambda B: (phi in B), q))
    q_new, delta = get_to(q_0, q, clouser)
    sigma = frozenset([str(literal) for literal in frozenset(filter(lambda phi: isinstance(phi, Literal), clouser))])
    f = get_f(clouser, q)

    def out_put_convert(elements, func):
        return frozenset([func(e) for e in elements])

    set_to_string_func = lambda B: frozenset([str(y) for y in B])

    string_delta = frozenset(
        [(set_to_string_func(B), set_to_string_func(A), set_to_string_func(B_tag)) for B, A, B_tag in delta])
    string_f = frozenset([out_put_convert(Bis, set_to_string_func) for Bis in f])

    return {'q': out_put_convert(q, set_to_string_func), 'sigma': out_put_convert(sigma, str), 'delta': string_delta,
            'q0': out_put_convert(q, set_to_string_func), 'f': string_f}


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


class HashableSet(set):
    def __hash__(self):
        return hash(frozenset(*self))

    # Press the green button in the gutter to run the script.


def get_ts():
    def function_creator(B, contidion, q):
        A = frozenset(filter(lambda x: isinstance(x, Literal), (B.difference({Literal(True)}))))
        tis = frozenset(filter(lambda B_tag: contidion(B_tag), q))
        return frozenset(map(lambda B_tag: (frozenset(B), A, frozenset(B_tag)), tis))

    a = Literal('a')
    b = Literal('b')
    t = Literal(True)
    a_until_b = Until(a, b)
    phi = Until(t, Not(a_until_b))
    B_1 = frozenset((a, Not(b), Not(a_until_b), phi, t))
    B_2 = frozenset((a, Not(b), a_until_b, phi, t))
    B_3 = frozenset((a, b, a_until_b, phi, t))
    B_4 = frozenset((Not(a), b, a_until_b, phi, t))
    B_5 = frozenset((Not(a), Not(b), Not(a_until_b), phi, t))
    B_6 = frozenset((Not(a), b, a_until_b, Not(phi), t))
    B_7 = frozenset((a, b, a_until_b, Not(phi), t))
    B_8 = frozenset((a, Not(b), a_until_b, Not(phi), t))
    q = {B_1, B_2, B_3, B_4, B_5, B_6, B_7, B_8}
    q_0 = frozenset(filter(lambda B: (phi in B), q))
    f = {frozenset((B_1, B_5, B_6, B_7, B_8)), frozenset((B_1, B_3, B_4, B_5, B_6, B_7))}

    B_1_funcion = function_creator(B_1, (lambda B_tag: a_until_b not in B_tag), q)
    B_2_function = function_creator(B_2, (lambda B_tag: (a_until_b in B_tag) and (phi in B_tag)), q)
    B_3_function = function_creator(B_3, (lambda B_tag: phi in B_tag), q)
    B_4_function = function_creator(B_4, (lambda B_tag: phi in B_tag), q)
    B_5_function = function_creator(B_5, (lambda B_tag: True), q)
    B_6_function = function_creator(B_6, (lambda B_tag: phi not in B_tag), q)
    B_7_function = function_creator(B_7, (lambda B_tag: phi not in B_tag), q)
    B_8_function = function_creator(B_8, (lambda B_tag: (a_until_b in B_tag) and (phi not in B_tag)), q)
    sigma = {a, b, t}
    delta = B_1_funcion | B_2_function | B_3_function | B_4_function | B_5_function | B_6_function | B_7_function | B_8_function

    closure = phi.sub()

    def out_put_convert(elements, func):
        return frozenset([func(e) for e in elements])

    set_to_string_func = lambda B: frozenset([str(y) for y in B])

    string_delta = frozenset(
        [(set_to_string_func(B), set_to_string_func(A), set_to_string_func(B_tag)) for B, A, B_tag in delta])
    string_f = frozenset([out_put_convert(Bis, set_to_string_func) for Bis in f])

    return {'q': out_put_convert(q, set_to_string_func), 'sigma': out_put_convert(sigma, str), 'delta': string_delta,
            'q0': out_put_convert(q, set_to_string_func), 'f': string_f}


if __name__ == '__main__':
    print_hi('PyCharm')
    exp = Not(Always(Until('a', 'b')))
    print(exp)
    s = {1, 2, 3}
    a = Literal('a')
    b = Literal('b')
    t = Literal(True)
    a_until_b = Until(a, b)
    phi = Until(t, Not(a_until_b))
    curr_try = ltl_to_gnba(phi)
    q_get = curr_try.get('q')
    i = 3
    ts = get_ts()
    i = 1
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
