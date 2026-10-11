import sys, time
sys.argv = ['x', sys.argv[1]]
exec(open('invfam.py').read().split("if __name__ == '__main__':")[0])
I12 = ['a_Gamma', 'A', 'M', "G2'", "G2'a", 'N1', 'N2', 'S', 'ac_le_ap', 'cp_le_ap', 'pAC', 'aCP']
I4 = ['pAC', 'aCP', 'N2', "G2'"]
others = [q for q in I12 if q not in ('A', 'cp_le_ap', 'ac_le_ap')]
step1 = [('mt','a','c'), idf('y'), ('comm','y','z'), idf('z')]
t0 = time.time()
tests = {
 "I12(y) + I4(z) => A(z)": ([(q, 'y') for q in I12] + [(q, 'z') for q in I4]),
 "I12(y) + others(z) (all 9 non-A invariants) => A(z)": ([(q, 'y') for q in I12] + [(q, 'z') for q in others]),
 "I12(y) + others(z) + a_Gamma(z) ... => A(z)": ([(q, 'y') for q in I12] + [(q, 'z') for q in others]),
}
for name, hy in tests.items():
    print(f"m={m}: {name}: {run(step1, hy, ('A', 'z'))} ({time.time()-t0:.0f}s)", flush=True)
# which of the 'others' propagate from I12(y)?
for nm in others + ['M', "G2'a", 'a_Gamma', 'N1', 'S']:
    pass
res = {nm: run(step1, [(q, 'y') for q in I12], (nm, 'z')) for nm in I12}
print(f"m={m}: propagation of each invariant from I12(y): {res}", flush=True)
