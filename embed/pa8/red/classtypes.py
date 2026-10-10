"""Types of classes of eps_p v eps_c for p = x (c~x) and p = y (second chain element), on the (W_2) instances in P_4."""
import sys, pickle
from collections import Counter
exec(open('blocktypes.py').read().split("def sig(")[0])
def cls_list(parts):
    J = classes(parts); seen = set(); out = []
    for u in range(n):
        if u in seen: continue
        K = {v for v in range(n) if J(u, v)}; seen |= K; out.append(K)
    return out
def ctype(K, p, c, a):
    Sp, Sc, Sa = supp(p), supp(c), supp(a)
    pb = [(bl, k) for bl, k in blocks(p) if bl & K]; cb = [(bl, k) for bl, k in blocks(c) if bl & K]
    U, L = K & Sp, K & Sc
    nT_p = sum(1 for bl, k in pb if k == 'T'); nN_p = len(pb) - nT_p
    nT_c = sum(1 for bl, k in cb if k == 'T'); nN_c = len(cb) - nT_c
    shape = ('U=K' if U == K else ('U=0' if not U else 'U<K')) + ',' + ('L=K' if L == K else ('L=0' if not L else 'L<K')) + (',U=L' if U == L else ',U!=L')
    Jac = classes([part(a), part(c)]); ngam = len({next(i for i, G in enumerate(cls_list([part(a), part(c)])) if u in G) for u in K})
    return (shape, f'p:{nT_p}T{nN_p}N', f'c:{nT_c}T{nN_c}N', f'#Gamma={ngam}', 'meetsSa' if K & Sa else '-')
cx = Counter(); cy = Counter(); ex = {}
for a, c, b, x, y in inst:
    for K in cls_list([part(x), part(c)]): cx[ctype(K, x, c, a)] += 1
    for K in cls_list([part(y), part(c)]):
        t = ctype(K, y, c, a); cy[t] += 1; ex.setdefault(t, (a, c, x, y, K))
print("classes of eps_x v eps_c:"); [print('  ', t, v) for t, v in sorted(cx.items())]
print("classes of eps_y v eps_c:"); [print('  ', t, v, '' if t in cx else '  <-- NEW') for t, v in sorted(cy.items())]
pickle.dump(ex, open('classtypes_ex.pkl', 'wb'))
