import sys, json, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid, violated_in
C6 = json.load(open('/home/claude/pa8w/embed/pa8/cand9.json'))[6]
concl = ('mt','a','b')
base = [('mt','a','d'), ('mt','d','b'), ('comm','b','i'), ('eq',('a','i'),'f'), ('eq',('i','f'),'c'), ('le','c','h'), ('eq',('h','f'),'g'), ('le','g','d')]
def test(name, H, mmax=6):
    t = time.time(); v = violated_in(C6, H, concl); r = []
    for m in range(4, mmax + 1):
        ok = valid(H, concl, m); r.append((m, ok))
        if not ok: break
    print(f"{name}: violated in cand6: {v is not None}  valid: {r}  [{time.time()-t:.0f}s]", flush=True)
    return v is not None, r
test("A' (comm form)", base)
for k in range(2, len(base)):
    H = base[:k] + base[k+1:]
    test(f"A' minus {base[k]}", H, mmax=5)
