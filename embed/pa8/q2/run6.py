import sys, pickle, importlib, random
sys.argv = ['x']
from hq import *
import hq
# monkeypatch run to sample u,y
def run_sampled(n, files, claims, maxshow=2, maxu=2, maxy=2, seed=0):
    P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
    rng = random.Random(seed); fails = {}; ex = {}; count = 0
    for f in files:
        for a, c, b, d, us, ys in pickle.load(open(f, 'rb')):
            if len({a, c, b, d}) < 4: continue
            us = list(us); ys = list(ys); rng.shuffle(us); rng.shuffle(ys)
            for u in us[:maxu]:
                for y in ys[:maxy]:
                    s = structure(P, n, a, c, b, d, u, y); s.ids = (a, c, b, d, u, y); count += 1
                    for name, fn in claims.items():
                        try: ok = fn(s)
                        except Exception as e: ok = False; name = name + ' [EXC ' + repr(e)[:40] + ']'
                        if not ok:
                            fails[name] = fails.get(name, 0) + 1
                            if name not in ex: ex[name] = s
    print(f"P_{n}: {count} instances")
    for name in claims: print(f"  {name:40s} fails {fails.get(name, 0)}")
    for name, s in list(ex.items())[:maxshow]:
        print("  example for", name)
        for nm, i in zip('acbduy', s.ids): print(f"    {nm} = {show(P, n, i)}")
hq.run = run_sampled
claims = {}
for mod in ['t1', 't6', 't7', 't8', 't10', 't18', 't21', 't22', 't23']:
    src = open(mod + '.py').read().split('claims = ')[0]
    g = {}; exec(src, g)
    for k, v in g.items():
        if k.startswith('C_'): claims[mod + ':' + k[2:]] = v
if __name__ == "__main__": files = ["instQ6_0.pkl", "instQ6_1.pkl", "instQ6_2.pkl"]
if __name__ == "__main__": run_sampled(6, files, claims, maxshow=6)
