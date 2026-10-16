"""Evaluate the K4 variants K4[h -> alpha] (k4weak4.pkl) on the known finite algebras: which variants are violated?"""
import json, pickle, itertools
d = pickle.load(open('k4weak4.pkl', 'rb')); names = d['terms']; out = d['out']
algs = json.load(open('../impl/algs.json'))
def mk(T):
    th = lambda p, q: T[q][p]
    def val(name, env):
        if len(name) == 1: return env[name]
        p, q = name[3], name[5]; return th(env[p], env[q])
    return th, val
HYP = {'aya=a': lambda th,a,b,c,y,z: th(a,y)==a, 'b<=z': lambda th,a,b,c,y,z: th(z,b)==b, 'y~c': lambda th,a,b,c,y,z: False,
       'th_z(y)=v': lambda th,a,b,c,y,z: th(z,y)==th(b,a), 'th_z(a)=u': lambda th,a,b,c,y,z: th(z,a)==th(a,b)}
for name, T in algs.items():
    n = len(T); th, val = mk(T); T2 = T
    comm = lambda p, q: T2[p][q] == T2[q][p]
    HYP['y~c'] = lambda th,a,b,c,y,z: comm(y,c)
    M = [[th(p,q)==p and th(q,p)==q for q in range(n)] for p in range(n)]
    base = [(a,b,c) for a in range(n) for c in range(n) if M[a][c] for b in range(n) if M[c][b] and not M[a][b]]
    hits = {}
    for h, lst in out.items():
        others = [k for k in HYP if k != h]
        for atom, cnt in lst:
            s, t = atom.split(' = ')
            for a, b, c in base:
                found = False
                for y in range(n):
                    for z in range(n):
                        if all(HYP[k](th,a,b,c,y,z) for k in others):
                            env = dict(a=a,b=b,c=c,y=y,z=z)
                            if val(s, env) == val(t, env): found = True; break
                    if found: break
                if found: hits.setdefault(h, []).append(atom); break
    print(f"{name:10} violated variants: " + '; '.join(f"[{h} -> {', '.join(v)}]" for h, v in hits.items()) if hits else f"{name:10} satisfies all variants")
