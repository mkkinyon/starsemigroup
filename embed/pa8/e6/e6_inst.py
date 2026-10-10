import pickle, numpy as np, itertools, sys, time
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pmon import mul
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]
comm = (T == T.T); le = (T == ar[:, None])
rows = []
# a c a = a: th(a,c)=a -> T[c,a]==a ; a d a = a ; d b d = d : T[b,d]==d ; cd=dc ; bcb = a(cd)a : T[c,b] == T[e,a] with e = T[d,c]
for c in range(N):
    ds = ar[comm[c, ar]]
    for d in ds:
        e = T[d, c]
        As = ar[(T[c, ar] == ar) & (T[d, ar] == ar)]
        if not len(As): continue
        Bs = ar[T[b_ := ar, d] == d] if False else ar[T[ar, d] == d]
        for a in As:
            ea = T[e, a]
            for b in Bs:
                if T[c, b] == ea: rows.append((a, b, c, d))
R = np.array(rows); a, b, c, d = R.T; e = T[d, c]
print("instances", len(R), "conclusion aea=a fails:", np.sum(T[e, a] != a), "distinct a,b,c,d:", np.sum((a != b) & (c != d) & (a != c) & (a != d) & (b != c) & (b != d)))
pickle.dump(R, open(f'instE{n}.pkl', 'wb'))
