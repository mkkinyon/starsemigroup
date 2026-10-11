import sys, time, pickle
exec(open('tind.py').read().split("Tyz = ")[0])
def fmt2(cl):
    def f(lit):
        s, a = lit
        if a[0] == 'J3': t = f"J3({''.join(a[1:])})"
        else: t = f"E({a[1]})" if a[0] == 'E' else (f"T({a[1]},{a[2]})" if a[0] == 'T' else f"J({a[1]}{a[2]})")
        return t if s > 0 else '~' + t
    return ' | '.join(f(l) for l in cl)
def jset(a):   # atom -> (kind, set of letters) for join-type atoms, else None
    if a[0] == 'E': return frozenset([a[1]])
    if a[0] in ('J', 'J3'): return frozenset(a[1:])
    return None
def stronger_lit(l1, l2):
    """does literal l1 imply literal l2 by monotonicity of joins?"""
    (s1, a1), (s2, a2) = l1, l2
    if l1 == l2: return True
    P, Q = jset(a1), jset(a2)
    if P is None or Q is None or s1 != s2: return False
    return (P <= Q) if s1 > 0 else (P >= Q)
def trivially_implies(C, G):
    return all(any(stronger_lit(l1, l2) for l2 in G) for l1 in C)
Q2 = meetst('cy', 'ab', 'bc'); P2 = meetst('acy', 'bcy', 'cy'); T2 = meetst('ab', 'bcy', 'bc')
S, new = pickle.load(open('inv5_m4_K3.pkl', 'rb')); V3 = pickle.load(open('inv6_m5.pkl', 'rb'))
base = [('mt','a','c'), ('comm','y','b'), ('eq',('y','a'),('y','c'))]
for name, g in (("T2", T2), ("Q2", Q2), ("P2", P2)):
    pool_ = [cl for cl in S + V3 if not trivially_implies(cl, g)]
    t0 = time.time(); ok = holds4(base, pool_, g)
    print(f"m={m}: {name} from base + {len(pool_)} local clauses (trivial implicants removed): {ok} ({time.time()-t0:.0f}s)", flush=True)
    if ok:
        cur = list(pool_)
        for cl in list(cur):
            trial = [c2 for c2 in cur if c2 != cl]
            if holds4(base, trial, g): cur = trial
        print(f"   minimal set ({len(cur)}):")
        for cl in cur: print('      ', fmt2(cl))
