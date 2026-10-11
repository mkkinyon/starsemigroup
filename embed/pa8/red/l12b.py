import sys, time, pickle
exec(open('pqdec3.py').read().split('decomp("K1')[0])
P = [('mt','a','c'), ('mt','c','b')]
one = P + [('comm','x','c'), idf('x'), ('comm','x','b')]
two = P + [('comm','x','c'), idf('x'), ('comm','x','y'), idf('y'), ('comm','y','b')]
three = two[:-1] + [('comm','y','z'), idf('z'), ('comm','z','b')]
for n, H, e in ((1, one, 'x'), (2, two, 'y'), (3, three, 'z')):
    L1 = meetst('abc', 'b' + e, 'b'); L2 = meetst('bc' + e, 'ac', 'c')
    print(f"m={m} n={n} (with c|><|b): L1 {holds4(H, [], L1)}  L2 {holds4(H, [], L2)}", flush=True)
L1 = meetst('abc', 'by', 'b'); L2 = meetst('bcy', 'ac', 'c'); T2 = meetst('ab', 'bcy', 'bc')
G1 = ((-1, ('E', 'c')), (1, ('J', 'a', 'b')))
G2 = ((-1, ('J3', 'a', 'b', 'c')), (-1, ('T','c','u')), (-1, ('T','c','v')), (1, ('E','c')))
baseb = P + [('comm','y','b'), idf('y')]
def decomp2(name, g, pool_):
    pool_ = [cl for cl in pool_ if not trivially_implies(cl, g)]
    ok = holds4(baseb, pool_, g); print(f"m={m}: {name} from base(with c|><|b) + {len(pool_)} clauses: {ok}", flush=True)
    if ok:
        cur = list(pool_)
        for cl in list(cur):
            trial = [c2 for c2 in cur if c2 != cl]
            if holds4(baseb, trial, g): cur = trial
        for cl in cur: print('      ', fmt2(cl))
nobc = [cl for cl in S + V3 if (1, ('J','b','c')) not in cl]
print("--- derivations from clauses without +J(bc):")
decomp2("L1", L1, nobc); decomp2("L2", L2, nobc); decomp2("G1", G1, nobc + [L1, L2]); decomp2("G2", G2, nobc + [L1, L2])
print("--- G1, G2 from L1, L2 only:")
print("   G1:", holds4(baseb, [L1, L2], G1), "  G2:", holds4(baseb, [L1, L2], G2))
