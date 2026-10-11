import sys, time
sys.argv = ['x', sys.argv[1]]
exec(open('invfam.py').read().split("if __name__ == '__main__':")[0])
I12 = ['a_Gamma', 'A', 'M', "G2'", "G2'a", 'N1', 'N2', 'S', 'ac_le_ap', 'cp_le_ap', 'pAC', 'aCP']
I5 = ['cp_le_ap', 'pAC', 'aCP', 'N2', "G2'"]
step2 = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y'), ('comm','y','z'), idf('z')]
t0 = time.time()
for nm in I5:
    r = run(step2, [(q, 'x') for q in I12] + [(q, 'y') for q in I12], (nm, 'z'))
    print(f"m={m}: I12(x), I12(y), x~y~z all id => {nm}(z): {r} ({time.time()-t0:.0f}s)", flush=True)
# and the real one-link start: c~x, x id, x~y, y id => I5(y) (i.e. position 2 — known True) vs. with x~c replaced by I12(x)
step1 = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
for nm in I5:
    r = run(step1, [(q, 'x') for q in I12], (nm, 'y'))
    print(f"m={m}: I12(x), x~y, y id => {nm}(y): {r}", flush=True)
