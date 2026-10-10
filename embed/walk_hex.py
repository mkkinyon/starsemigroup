"""Walk construction.  Triangle: a_i |><| b_{i+1}; free pairs (a_i, b_{i-1}).
Starting from the free pair (a_i, b_{i-1}) (indices mod 3):
  forward:  F1 = theta_{b_{i-1}}(a_i),  F2 = theta_{a_{i+1}}(F1),  F3 = theta_{b_i}(F2), F4 = theta_{a_{i+2}}(F3), ...
  backward: G1 = theta_{a_i}(b_{i-1}),  G2 = theta_{b_{i+1}}(G1),  G3 = theta_{a_{i-1}}(G2), G4 = theta_{b_{i}}(G3), ...
(alternately 'project onto the free partner' and 'transport through a matched pair').
Candidate hexagon (offset k): A-side (below b's) = {F1,F3,G2}, B-side (below a's) = {F2,G1,G3}
with the pairs (F1,G3), (F3,G1), (G2,F2) commuting and the other pairs matched;
more generally use F_{k+1},F_{k+3},G_{k+2} | F_{k+2},G_{k+1},G_{k+3}."""
import re, sys
from termeval import make_eval
from mace4parse import parse_models
from uniform_hex import configurations

def nxt(i): return i % 3 + 1
def prv(i): return (i - 2) % 3 + 1

def chain_terms(i, length):
    F = []; cur = f"a{i}"; who = ("b", prv(i))          # F1 below b_{i-1}
    for k in range(length):
        cur = f"({cur} * {who[0]}{who[1]})"; F.append((cur, who))
        if who[0] == "b":   # transport b_j -> a_{j-1}  (a_{j-1} |><| b_j)
            who = ("a", prv(who[1]))
        else:               # project a_j -> b_{j-1}   (free pair)
            who = ("b", prv(who[1]))
    G = []; cur = f"b{prv(i)}"; who = ("a", i)           # G1 below a_i
    for k in range(length):
        cur = f"({cur} * {who[0]}{who[1]})"; G.append((cur, who))
        if who[0] == "a":   # transport a_j -> b_{j+1}  (a_j |><| b_{j+1})
            who = ("b", nxt(who[1]))
        else:               # project b_j -> a_{j+1}   (free pair (a_{j+1}, b_j))
            who = ("a", nxt(who[1]))
    return F, G

def hexagon_from(F, G, k):
    """A = {F_{k+1}, F_{k+3}, G_{k+2}}, B = {F_{k+2}, G_{k+1}, G_{k+3}}, grouped by index of the vertex they lie under."""
    X = [F[k], F[k + 2], G[k + 1]]; Y = [F[k + 1], G[k], G[k + 2]]
    # pair up by index: X entries are under (side s, idx j); partner in Y under the other side with same idx
    A = {x[1][1]: x[0] for x in X}; B = {y[1][1]: y[0] for y in Y}
    if set(A) != {1, 2, 3} or set(B) != {1, 2, 3}: return None
    return A, B

def hex_eqs(A, B):
    eqs = []
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            if i != j:
                eqs.append((f"{A[i]} * {A[j]}", f"{A[1]} * {A[2]}"))
                eqs.append((f"{B[i]} * {B[j]}", f"{B[1]} * {B[2]}"))
                eqs.append((f"{B[j]} * {A[i]}", A[i])); eqs.append((f"{A[i]} * {B[j]}", B[j]))
        eqs.append((f"{A[i]} * {B[i]}", f"{B[i]} * {A[i]}"))
    return eqs

def is_hexagon(ev, e, A, B):
    if any(ev(l, e) != ev(r, e) for l, r in hex_eqs(A, B)): return False
    wa = ev(f"{A[1]} * {A[2]}", e); zb = ev(f"{B[1]} * {B[2]}", e)
    w = ev("a1 * a2", e); z = ev("b1 * b2", e)
    return {wa, zb} == {w, z}

if __name__ == "__main__":
    files = sys.argv[1:] or ["mace_tri17.out", "mace_tri15.out", "mace_uni17b.out", "mace_tri19.out", "mace_uni37.out"]
    L = 6
    for fn in files:
        for N, T, c in parse_models(open(fn).read()):
            ev = make_eval(lambda x, y: T[x][y])
            confs = configurations(N, ev, only_wz=True)
            if not confs:
                print(f"{fn}: no configuration with w != z"); continue
            from collections import Counter
            stats = Counter()
            for e in confs:
                ok = set()
                for i in (1, 2, 3):
                    F, G = chain_terms(i, L)
                    for k in range(L - 2):
                        hb = hexagon_from(F, G, k)
                        if hb and is_hexagon(ev, e, *hb): ok.add((i, k))
                stats[tuple(sorted(ok))] += 1
            print(f"{fn}: {len(confs)} configurations with w != z; (start pair i, offset k) giving a hexagon -> count:")
            for key, v in sorted(stats.items(), key=lambda kv: -kv[1]): print("    ", key, v)
