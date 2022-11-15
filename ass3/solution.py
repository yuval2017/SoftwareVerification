# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from itertools import product


def create_initial_states(number_of_registers):
    i = tuple(([False] * number_of_registers))
    t = i + (True,)
    f = i + (False,)
    return {t, f}


def get_states(number_of_registers):
    i = list(product([True, False], repeat=number_of_registers))
    S = {s + (True,) for s in i}.union({s + (False,) for s in i})
    return S


def dfs_on_states(queue: list, update_registers):
    S = set()
    to = set()
    while queue:
        state = queue.pop(0)
        if state not in S:
            S.add(state)
            out_put_reg = update_registers(state)
            to_state_true = out_put_reg + (True,)
            to_state_false = out_put_reg + (False,)
            to.add((state, (True,), to_state_true))
            to.add((state, (False,), to_state_false))
            queue.append(to_state_true)
            queue.append(to_state_false)
    return S, to


def labels_eval(t: tuple, s: str, start, end):
    index = 1
    out = set()
    for i in range(start, end):

        if t[i]:
            out.add(s + str(index))
        index += 1
    return out


def transitionSystemFromCircuit(numberOfInputs, numberOfRegisters, numberOfOutputs, updateRegisters, computeOutputs):
    I = create_initial_states(numberOfRegisters)
    queue = list(I.copy())

    S, to = dfs_on_states(queue, updateRegisters)
    S = get_states(numberOfRegisters)
    AP = set()
    AP.update(['x' + str(i) for i in range(1, numberOfInputs + 1)])
    AP.update(['r' + str(i) for i in range(1, numberOfRegisters + 1)])
    AP.update(['y' + str(i) for i in range(1, numberOfOutputs + 1)])

    L = lambda s: labels_eval(computeOutputs(s), 'y', 0, numberOfInputs).union(
        labels_eval(s, 'x', numberOfRegisters, len(s))).union(labels_eval(s, 'r', 0, numberOfRegisters))
    return {'S': S, 'I': I, 'Act': {(True,), (False,)}, 'to': to, 'AP': AP, 'L': L}


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    SP = transitionSystemFromCircuit(1, 2, 1, lambda s: ((s[2] and s[1]) ^ s[0], s[2] ^ s[1]),
                                     lambda s: (s[0] and s[1] and s[2],))
    d = SP.get('L')((True, True, True))
    i = 1

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
