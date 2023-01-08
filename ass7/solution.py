# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from abc import ABC, abstractmethod
from typing import Union


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


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
