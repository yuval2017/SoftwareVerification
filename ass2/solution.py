# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import networkx as nx


def create_graph(TS):
    G = nx.DiGraph()
    set_to = TS.get("to")
    I = TS.get("I")
    S = TS.get("S")
    G.add_edges_from([(si, sj) for si, act, sj in set_to])
    set_reachable_vertices = set()
    for s_0 in I:
        curr_reachable = set()
        reach(G,s_0,curr_reachable)
        set_reachable_vertices = set_reachable_vertices.union(curr_reachable)
    vertices_to_remove = S.difference(set_reachable_vertices)
    G.remove_nodes_from(vertices_to_remove)
    return G

def reach(G,init_ver,reachable_vertices):
    if not init_ver in reachable_vertices:
        reachable_vertices.add(init_ver)
        adj = list(G.successors(init_ver))
        for a in adj:
            reach(G, a, reachable_vertices)

TS = {
    "S": {"s1", "s2", "s3","s4","s5"},
    "I": {"s1"},
    "Act": {"a", "b", "c"},
    "to": {("s1", "a", "s2"), ("s1", "a", "s1"), ("s1", "b", "s2"),
           ("s2", "c", "s3"), ("s3", "c", "s1"), ("s4", "c" , "s5"),("s5", "c" , "s4") },
    "AP": {"p", "q"},
    "L": lambda s: {"tick"} if s == "s1" else {"tick"} if s == "s2" else {""}
}


def property0(TS):
    L = TS.get("L")
    I = TS.get("I")
    G = create_graph(TS)
    return any(dfs_property0(G, s0, set(), lambda pred: ("crit1" in L(pred) and "crit2" in L(pred))) for s0 in I)


def dfs_property0(G, init_ver, set_found, func):
    if not init_ver in set_found:
        set_found.add(init_ver)
        if (func(init_ver)):
            return True
        adj = list(G.successors(init_ver))
        return any(dfs_property0(G, a, set_found, func) for a in adj)
    return False


def property1(TS):
    L = TS.get("L")
    I = TS.get("I")
    G = create_graph(TS)
    return all(dfs_property1(G, s0, set(), boll_func(L)) for s0 in I)


def boll_func(L):
    def func(pred, adj):
        return all(("even" not in L(pred)) or ("even" in L(pred) and "prime" not in L(suc)) for suc in adj)

    return func


def dfs_property1(G, init_ver, set_found, func):
    if not init_ver in set_found:
        set_found.add(init_ver)
        adj = list(G.successors(init_ver))
        if not func(init_ver, adj):
            return False
        return all(dfs_property1(G, suc, set_found, func) for suc in adj)
    return True


def property2(TS):
    L = TS.get("L")
    I = TS.get("I")
    G = create_graph(TS)
    return all(dfs_property2(G, s0, set(), lambda adj: len(adj) != 0) for s0 in I) and all(any("tick" in L(s_i) for s_i in c) for c in nx.simple_cycles(G))


def dfs_property2(G, init_ver, set_found, func):
    if not init_ver in set_found:
        set_found.add(init_ver)
        adj = list(G.successors(init_ver))
        if not func(adj):
            return False
        return all(dfs_property2(G, suc, set_found, func) for suc in adj)
    return True


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    i = property2(TS)
    j = 1

