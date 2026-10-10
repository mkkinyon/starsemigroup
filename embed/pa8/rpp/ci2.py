"""All minimal valid (m=4) hypothesis sets in the commutation/identification language with 2 auxiliaries x,y:
atoms p~q (p in {x,y}, q in {a,b,c,other aux}) and th_p(q)=th_p(q') (q,q' in {a,b,c}); path a~c~b; conclusion a~b.
Monotone: supersets of valid sets are valid; we enumerate subsets by size and record minimal valid ones."""
import sys, time, itertools, pickle
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
P = [('mt','a','c'), ('mt','c','b')]
atoms = [('comm',p,q) for p in 'xy' for q in 'abc'] + [('comm','x','y')] + [('eq',(p,q),(p,r)) for p in 'xy' for q,r in (('a','b'),('a','c'),('b','c'))]
print(len(atoms), 'atoms', flush=True)
minimal = []; cache = {}
def ok(S):
    key = frozenset(S)
    if key in cache: return cache[key]
    try: r = valid(P + [atoms[i] for i in S], ('mt','a','b'), 4)
    except ValueError: r = None
    cache[key] = r; return r
t0 = time.time()
for size in range(1, 7):
    found = 0
    for S in itertools.combinations(range(len(atoms)), size):
        if any(set(Mn) <= set(S) for Mn in minimal): continue
        # symmetry x<->y: canonical only
        r = ok(S)
        if r: minimal.append(S); found += 1; print(f"size {size}: ", [atoms[i] for i in S], f"[{time.time()-t0:.0f}s]", flush=True)
    print(f"-- size {size} done: {found} new minimal sets ({len(cache)} SAT calls, {time.time()-t0:.0f}s)", flush=True)
    pickle.dump(minimal, open('ci2_minimal.pkl', 'wb'))
