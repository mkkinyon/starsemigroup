import sys, json, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid, violated_in
C6 = json.load(open('/home/claude/pa8w/embed/pa8/cand9.json'))[6]
concl = ('mt','a','b')
def test(name, H, mmax=6):
    t = time.time(); v = violated_in(C6, H, concl); r = []
    if v is None: print(f"{name}: NOT violated in cand6", flush=True); return
    for m in range(4, mmax + 1):
        ok = valid(H, concl, m); r.append((m, ok))
        if not ok: break
    print(f"{name}: violated in cand6: True  valid: {r}  [{time.time()-t:.0f}s]", flush=True)
P = [('mt','a','d'), ('mt','d','b')]
test("B1: h~d, th_h(a)=th_h(d), i~b, th_i(a)=th_i(d), th_h(b)=th_i(a)", P + [('comm','h','d'), ('eq',('h','a'),('h','d')), ('comm','i','b'), ('eq',('i','a'),('i','d')), ('eq',('h','b'),('i','a'))])
test("B2: h~d, th_h(a)=th_h(d), i~b, th_i(a)=th_i(d)", P + [('comm','h','d'), ('eq',('h','a'),('h','d')), ('comm','i','b'), ('eq',('i','a'),('i','d'))])
test("B3: h~d, th_h(a)=th_h(d), i~b, th_h(b)=th_i(a)", P + [('comm','h','d'), ('eq',('h','a'),('h','d')), ('comm','i','b'), ('eq',('h','b'),('i','a'))])
test("B4: h~d, i~b, th_i(a)=th_i(d), th_h(b)=th_i(a)", P + [('comm','h','d'), ('comm','i','b'), ('eq',('i','a'),('i','d')), ('eq',('h','b'),('i','a'))])
test("B5: h~d, h~i, i~b, th_h(a)=th_h(d), th_i(a)=th_i(d)", P + [('comm','h','d'), ('comm','h','i'), ('comm','i','b'), ('eq',('h','a'),('h','d')), ('eq',('i','a'),('i','d'))])
test("B6: h~d, h~i, i~b, th_h(b)=th_i(a)=th_i(d)", P + [('comm','h','d'), ('comm','h','i'), ('comm','i','b'), ('eq',('h','b'),('i','a')), ('eq',('i','a'),('i','d'))])
