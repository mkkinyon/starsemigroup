import sys, time, pickle
exec(open('meets.py').read().split("L = 'abcy'")[0])
Tst = meet(frozenset('ab'), frozenset('bcy'), frozenset('bc'))
S1, S2, S3 = pickle.load(open('inv4_m4_K4.pkl', 'rb'))     # clauses about (x; a, c) incl. J3(acx)
def ren_y(cl):
    out = []
    for s, a in cl:
        if a[0] == 'E': a = ('E', 'y' if a[1] == 'x' else a[1])
        elif a[0] == 'T': a = ('T', 'y' if a[1] == 'x' else a[1], a[2])
        elif a[0] == 'J': p, q = sorted(('y' if a[1] == 'x' else a[1], 'y' if a[2] == 'x' else a[2])); a = ('J', p, q)
        else: a = ('J3', 'a', 'c', 'y')
        out.append((s, a))
    return tuple(out)
pool_ = [ren_y(cl) for cl in S3]
five = [((-1,('E','y')), (1,('T','y','u')), (1,('J','a','c')), (-1,('T','a','u')), (1,('T','c','u'))),
        ((-1,('E','y')), (1,('T','y','u')), (1,('E','c')), (-1,('T','a','u')), (1,('T','c','u')), (1,('T','c','v')))]
pool_ += five
base = [('mt','a','c'), ('comm','y','b'), ('eq',('y','a'),('y','c'))]
t0 = time.time()
print(f"m={m}: T from a|><|c, y~b, y id + all {len(pool_)} chain-valid local clauses about y: {holds2(base, pool_, Tst)} ({time.time()-t0:.0f}s)", flush=True)
if holds2(base, pool_, Tst):
    cur = list(pool_)
    for cl in list(cur):
        trial = [c2 for c2 in cur if c2 != cl]
        if holds2(base, trial, Tst): cur = trial
    print(f"minimal set ({len(cur)}):")
    for cl in cur: print('   ', fmt2(cl) if 'fmt2' in dir() else cl)
