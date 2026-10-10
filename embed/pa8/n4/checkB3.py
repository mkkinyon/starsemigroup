import sys, json, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid, violated_in
concl = ('mt','a','b')
B3 = [('mt','a','d'), ('mt','d','b'), ('comm','h','d'), ('eq',('h','a'),('h','d')), ('comm','i','b'), ('eq',('h','b'),('i','a'))]
Rp = [('mt','a','c'), ('mt','c','b'), ('comm','x','c'), ('eq',('x','a'),('x','c')), ('comm','y','a'), ('eq',('x','b'),('y','b'))]
t=time.time(); print("sanity (R') valid m=4,5:", [valid(Rp, concl, m) for m in (4,5)], f"{time.time()-t:.0f}s", flush=True)
E = '/home/claude/pa8w/embed/pa8/'
C9 = json.load(open(E+'cand9.json'))
print("B3 violated by order-9 candidates:", [k for k,T in enumerate(C9) if violated_in(T, B3, concl)], flush=True)
P8 = [json.loads(l)['A'] for l in open(E+'post8.log') if json.loads(l).get('embeds') is None]
print("B3 violated by P_8^k (k=1..7):", [k+1 for k,T in enumerate(P8) if violated_in(T, B3, concl)], flush=True)
# all embeddable census algebras must satisfy B3
algs = []
for k in range(1, 8): algs += json.load(open(E + f'ord{k}.json'))
for f in ['post8.log', 'post9_0.log', 'post9_1.log', 'post9_3.log']:
    for line in open(E + f):
        d = json.loads(line)
        if d.get('embeds') is not None: algs.append(d['A'])
t=time.time(); bad = 0
for j, T in enumerate(algs):
    if violated_in(T, B3, concl): bad += 1; print("  VIOLATED by embeddable algebra", j, T, flush=True)
print(f"census check: {len(algs)} embeddable algebras, {bad} violate B3  [{time.time()-t:.0f}s]", flush=True)
