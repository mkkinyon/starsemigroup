"""Probe for a common generalisation of (R'), (P1), (Q) in the 2-auxiliary path-closing language on P_4.
Atoms over (p0,p1,p2,p3,X,Y). For each condition C and substitution sigma (X,Y -> terms of C's variables,
path -> path), S(C,sigma) = atoms true on all instances of C. G = intersection over the three conditions is
valid iff no bad tuple (non-closed path, any X,Y) satisfies all atoms of G."""
import pickle, itertools, sys, time
import numpy as np
P, T = pickle.load(open('tab4.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]            # theta_x(p)
Mt = (T.T == ar[:, None]) & (T == ar[None, :])   # Mt[p,q]: theta_p(q)=p and theta_q(p)=q
comm = (T == T.T)                                  # comm[p,q]: theta_q(p) == theta_p(q)  <=> pq=qp
le = (T == ar[:, None])                           # le[q,p]: theta_p(q)=q  <=> q<=p
# ---- atoms: functions of arrays p0,p1,p2,p3,X,Y (all same shape) -> bool array
ATOMS = {}
def A(name, f): ATOMS[name] = f
for i in range(4):
    A(f'X~p{i}', lambda p, i=i: comm[p['X'], p[i]]); A(f'Y~p{i}', lambda p, i=i: comm[p['Y'], p[i]])
    A(f'X<=p{i}', lambda p, i=i: le[p['X'], p[i]]); A(f'Y<=p{i}', lambda p, i=i: le[p['Y'], p[i]])
    A(f'p{i}<=X', lambda p, i=i: le[p[i], p['X']]); A(f'p{i}<=Y', lambda p, i=i: le[p[i], p['Y']])
    A(f'thX(p{i})=thY(p{i})', lambda p, i=i: th(p['X'], p[i]) == th(p['Y'], p[i]))
    A(f'thp{i}(X)=thp{i}(Y)', lambda p, i=i: th(p[i], p['X']) == th(p[i], p['Y']))
A('X~Y', lambda p: comm[p['X'], p['Y']]); A('X<=Y', lambda p: le[p['X'], p['Y']]); A('Y<=X', lambda p: le[p['Y'], p['X']])
for i, j in itertools.combinations(range(4), 2):
    A(f'thX(p{i})=thX(p{j})', lambda p, i=i, j=j: th(p['X'], p[i]) == th(p['X'], p[j]))
    A(f'thY(p{i})=thY(p{j})', lambda p, i=i, j=j: th(p['Y'], p[i]) == th(p['Y'], p[j]))
    A(f'thp{i}(X)=thp{j}(X)', lambda p, i=i, j=j: th(p[i], p['X']) == th(p[j], p['X']))
    A(f'thp{i}(Y)=thp{j}(Y)', lambda p, i=i, j=j: th(p[i], p['Y']) == th(p[j], p['Y']))
    if j - i >= 2:
        A(f'p{i}~p{j}', lambda p, i=i, j=j: comm[p[i], p[j]])
        A(f'p{i}|><|p{j}', lambda p, i=i, j=j: Mt[p[i], p[j]])
    A(f'thX(p{i})=thp{j}(X)', lambda p, i=i, j=j: th(p['X'], p[i]) == th(p[j], p['X']))
    A(f'thX(p{j})=thp{i}(X)', lambda p, i=i, j=j: th(p['X'], p[j]) == th(p[i], p['X']))
NAMES = list(ATOMS); NA = len(NAMES)
def sig(p):
    return np.stack([ATOMS[n](p) for n in NAMES], axis=-1)   # shape (..., NA)
# ---- all paths of length 3 (consecutive matched, consecutive distinct)
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
paths = [(a, b, c, d) for a in range(N) for b in nb[a] for c in nb[b] for d in nb[c]]
paths = np.array(paths); closed = Mt[paths[:, 0], paths[:, 3]]
print("paths:", len(paths), "closed:", closed.sum(), flush=True)
XX, YY = np.meshgrid(ar, ar, indexing='ij'); XX = XX.ravel(); YY = YY.ravel()
def tuples(path, X=None, Y=None):
    a, b, c, d = path
    X = XX if X is None else X; Y = YY if Y is None else Y
    return {0: np.full_like(X, a), 1: np.full_like(X, b), 2: np.full_like(X, c), 3: np.full_like(X, d), 'X': X, 'Y': Y}
# bad signatures: from non-closed paths (all X,Y)
rng = np.random.default_rng(1)
t0 = time.time(); bad = set()
NC = paths[~closed]; NC = NC[rng.choice(len(NC), size=min(4000, len(NC)), replace=False)]
for path in NC:
    S = sig(tuples(path)); bad.update(map(bytes, np.packbits(S, axis=1)))
bad = np.unpackbits(np.frombuffer(b''.join(bad), dtype=np.uint8).reshape(len(bad), -1), axis=1)[:, :NA].astype(bool)
print("distinct bad signatures:", len(bad), f"({time.time()-t0:.0f}s)", flush=True)
pickle.dump((NAMES, bad, paths, closed), open('probe_bad.pkl', 'wb'))
def valid(G):   # G: bool mask over atoms
    return not np.any(np.all(bad[:, G], axis=1))
# ---- conditions: instances (path + own auxiliaries), and term lists for X,Y
CAP = 150000
def inst_Q():
    A_, B_, C_, D_, X_, Y_ = [], [], [], [], [], []
    for path in paths[closed]:
        a, b, c, d = path
        xs = ar[comm[ar, a] & (th(b, ar) == th(d, ar))]; ys = ar[comm[ar, a] & comm[ar, c] & (th(ar, b) == th(ar, c))]
        if len(xs) and len(ys):
            X, Y = np.meshgrid(xs, ys, indexing='ij'); X = X.ravel(); Y = Y.ravel()
            A_.append(np.full_like(X, a)); B_.append(np.full_like(X, b)); C_.append(np.full_like(X, c)); D_.append(np.full_like(X, d)); X_.append(X); Y_.append(Y)
    arrs = [np.concatenate(L) for L in (A_, B_, C_, D_, X_, Y_)]
    n = len(arrs[0]); sel = rng.choice(n, size=min(CAP, n), replace=False)
    return [v[sel] for v in arrs], n
def inst_P1():
    A_, B_, C_, D_, X_ = [], [], [], [], []
    for path in paths[closed]:
        a, b, c, d = path
        xs = ar[comm[ar, a] & comm[ar, b] & (th(a, ar) == th(c, ar)) & (th(ar, b) == th(ar, d))]
        if len(xs):
            A_.append(np.full_like(xs, a)); B_.append(np.full_like(xs, b)); C_.append(np.full_like(xs, c)); D_.append(np.full_like(xs, d)); X_.append(xs)
    arrs = [np.concatenate(L) for L in (A_, B_, C_, D_, X_)]
    n = len(arrs[0]); sel = rng.choice(n, size=min(CAP, n), replace=False)
    arrs = [v[sel] for v in arrs]; return arrs + [arrs[4]], n
def inst_Rp():
    inst = pickle.load(open('/home/claude/pa8w/rp/inst4.pkl', 'rb')); idx = {p: i for i, p in enumerate(P)}
    return [(idx[a], idx[c], idx[b], idx[x], idx[y]) for a, c, b, x, y in inst]
# terms available for X,Y in each condition: functions of (path, x, y) arrays
TERMS = {
 'Q': {'x': lambda a,b,c,d,x,y: x, 'y': lambda a,b,c,d,x,y: y, 'xy': lambda a,b,c,d,x,y: th(x, y), 'yx': lambda a,b,c,d,x,y: th(y, x),
       'xp0': lambda a,b,c,d,x,y: th(x, a), 'yp0': lambda a,b,c,d,x,y: th(y, a), 'yp2': lambda a,b,c,d,x,y: th(y, c),
       'thp1(x)': lambda a,b,c,d,x,y: th(b, x), 'thx(p1)': lambda a,b,c,d,x,y: th(x, b), 'thy(p1)': lambda a,b,c,d,x,y: th(y, b),
       'thx(p2)': lambda a,b,c,d,x,y: th(x, c), 'thx(p3)': lambda a,b,c,d,x,y: th(x, d), 'thy(p3)': lambda a,b,c,d,x,y: th(y, d),
       'p0': lambda a,b,c,d,x,y: a, 'p1': lambda a,b,c,d,x,y: b, 'p2': lambda a,b,c,d,x,y: c, 'p3': lambda a,b,c,d,x,y: d},
 'P1': {'x': lambda a,b,c,d,x,y: x, 'xp0': lambda a,b,c,d,x,y: th(x, a), 'xp1': lambda a,b,c,d,x,y: th(x, b),
        'thx(p2)': lambda a,b,c,d,x,y: th(x, c), 'thx(p3)': lambda a,b,c,d,x,y: th(x, d), 'thp2(x)': lambda a,b,c,d,x,y: th(c, x), 'thp3(x)': lambda a,b,c,d,x,y: th(d, x),
        'p0': lambda a,b,c,d,x,y: a, 'p1': lambda a,b,c,d,x,y: b, 'p2': lambda a,b,c,d,x,y: c, 'p3': lambda a,b,c,d,x,y: d},
}
# R': variables (a,c,b,x,y); path embeddings: (a,c,b,b), (a,c,c,b), (a,a,c,b)
TERMS_R = {'x': lambda a,c,b,x,y: x, 'y': lambda a,c,b,x,y: y, 'xy': lambda a,c,b,x,y: th(x, y), 'v=xc': lambda a,c,b,x,y: th(x, c),
           'u=ya': lambda a,c,b,x,y: th(y, a), 'r=xbx': lambda a,c,b,x,y: th(x, b), 'thy(c)': lambda a,c,b,x,y: th(y, c), 'thb(x)': lambda a,c,b,x,y: th(b, x),
           'tha(x)': lambda a,c,b,x,y: th(a, x), 'a': lambda a,c,b,x,y: a, 'c': lambda a,c,b,x,y: c, 'b': lambda a,c,b,x,y: b}
def S_of(arrs, terms):
    a, b, c, d, x, y = arrs; acc = {}
    tv = {n: terms[n](a, b, c, d, x, y) for n in terms}
    for tX in terms:
        for tY in terms:
            p = {0: a, 1: b, 2: c, 3: d, 'X': tv[tX], 'Y': tv[tY]}
            acc[(tX, tY)] = np.all(sig(p), axis=0)
    return acc
t0 = time.time()
IQ, nQ = inst_Q(); IP, nP = inst_P1(); IR = inst_Rp()
print("instances: Q", nQ, "P1", nP, "R'", len(IR), f"({time.time()-t0:.0f}s)", flush=True)
SQ = S_of(IQ, TERMS['Q']); print("S_Q done", f"({time.time()-t0:.0f}s)", flush=True)
SP = S_of(IP, TERMS['P1']); print("S_P1 done", f"({time.time()-t0:.0f}s)", flush=True)
# R' instances: group into arrays for speed
IRa = np.array(IR)
SR = {}
for emb_name, emb in [('accb', lambda a, c, b: (a, c, c, b)), ('acbb', lambda a, c, b: (a, c, b, b)), ('aacb', lambda a, c, b: (a, a, c, b))]:
    a, c, b, x, y = [IRa[:, k] for k in range(5)]
    base = (a, c, b, x, y); path = emb(a, c, b)
    tv = {n: TERMS_R[n](*base) for n in TERMS_R}
    for tX in TERMS_R:
        for tY in TERMS_R:
            p = {0: path[0], 1: path[1], 2: path[2], 3: path[3], 'X': tv[tX], 'Y': tv[tY]}
            SR[(emb_name, tX, tY)] = np.all(sig(p), axis=0)
print("S_R' done", f"({time.time()-t0:.0f}s)", flush=True)
pickle.dump((NAMES, SQ, SP, SR), open('probe_S.pkl', 'wb'))
# ---- search: G = SQ[s1] & SP[s2] & SR[s3]; valid?
found = []
cnt = 0
for k1, m1 in SQ.items():
    for k2, m2 in SP.items():
        m12 = m1 & m2
        if not valid(m12): continue   # monotone: if m12 invalid, subsets invalid
        for k3, m3 in SR.items():
            G = m12 & m3; cnt += 1
            if valid(G): found.append((k1, k2, k3, G))
print("valid triples:", len(found), "of", cnt, f"({time.time()-t0:.0f}s)")
pickle.dump(found, open('probe_found.pkl', 'wb'))
# report maximal ones (by atom set inclusion), fewest atoms first
Gs = {}
for k1, k2, k3, G in found: Gs.setdefault(bytes(np.packbits(G)), []).append((k1, k2, k3))
maxl = []
for key, subs in Gs.items():
    G = np.unpackbits(np.frombuffer(key, dtype=np.uint8))[:NA].astype(bool)
    maxl.append((G.sum(), [NAMES[i] for i in np.nonzero(G)[0]], subs[:3], len(subs)))
maxl.sort(key=lambda t: t[0])
for k, atoms, subs, ns in maxl[:15]: print(k, atoms, subs, ns)
