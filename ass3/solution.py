# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from itertools import product


def create_initial_states(number_of_registers, num_of_inputs):
    i1 = tuple(product([True, False], repeat=num_of_inputs))
    i = tuple(([False] * number_of_registers))
    return {i + ii1 for ii1 in i1}


def get_states(number_of_registers, num_of_inputs):
    i = set(product([True, False], repeat=number_of_registers + num_of_inputs))
    return i


def dfs_on_states(queue: list, update_registers, num_of_inputs):
    S = set()
    to = set()
    i1 = tuple(product([True, False], repeat=num_of_inputs))
    while queue:
        state = queue.pop(0)
        if state not in S:
            S.add(state)
            out_put_reg = update_registers(state)
            for ii1 in i1:
                to_state_true = out_put_reg + ii1
                to.add((state, ii1, to_state_true))
                queue.append(to_state_true)
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
    I = create_initial_states(numberOfRegisters, numberOfInputs)
    queue = list(I.copy())

    S, to = dfs_on_states(queue, updateRegisters, numberOfInputs)
    S = get_states(numberOfRegisters, numberOfInputs)
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
