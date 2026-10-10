import sys, time
from qi import test_qi
# letters: a=a0, e=a1, f=a2, b=b0, c=b1, d=b2
A = ['a','e','f']; B = ['b','c','d']
hyps = []
for i in range(3):
    for j in range(3):
        if i == j: continue
        hyps += [(A[i]+A[j], A[j]+A[i]), (A[i]+A[j], 'ae'), (B[i]+B[j], B[j]+B[i]), (B[i]+B[j], 'bc')]   # (a)
        hyps += [(A[i]+B[j]+A[i], A[i]), (B[j]+A[i]+B[j], B[j])]                                       # (c)
        mj = A[j]+B[j]
        hyps += [(B[i]+mj+B[i], 'bc'), (A[i]+mj+A[i], 'ae')]                                           # (d)
    hyps += [(A[i]+B[i], B[i]+A[i])]                                                                   # (b)
    hyps += [(A[i]+'bc'+A[i], A[i]+B[i]), (B[i]+'ae'+B[i], A[i]+B[i])]                                 # (d')
n = int(sys.argv[1])
t = time.time(); s = test_qi(n, "abcfed", hyps, ("ae", "bc"))
print(f"P_{n}: hexagon hypotheses & w != z: {'SATISFIABLE (theorem wrong!)' if s else 'unsatisfiable (consistent with theorem)'} ({time.time()-t:.0f}s)", flush=True)
if s: print(s[0])
