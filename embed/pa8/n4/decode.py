import json, itertools
C = json.load(open('/home/claude/pa8w/embed/pa8/cand9.json'))
def rel(T):
    n = len(T)
    mt = {(p,q) for p in range(n) for q in range(n) if p!=q and T[q][p]==p and T[p][q]==q}
    le = {(p,q) for p in range(n) for q in range(n) if p!=q and T[p][q]==p}
    cm = {(p,q) for p in range(n) for q in range(n) if p<q and T[p][q]==T[q][p]}
    return mt, le, cm
for k, T in enumerate(C):
    n = len(T); mt, le, cm = rel(T)
    print(f"=== cand {k}: matched pairs {sorted(p for p in mt if p[0]<p[1])}")
    print("    le:", sorted(le)); print("    comm:", sorted(cm))
    # induced paths of length 3,4 in matching graph with non-matched endpoints
    adj = {p: {q for q in range(n) if (p,q) in mt} for p in range(n)}
    for L in (3,4):
        paths = []
        for path in itertools.permutations(range(n), L+1):
            if all(path[i+1] in adj[path[i]] for i in range(L)) and (path[0],path[-1]) not in mt and path[0]<path[-1]:
                paths.append(path)
        print(f"    paths of length {L} with unmatched ends: {len(paths)}", paths[:12])
for line in open('/home/claude/pa8w/embed/pa8/qi_all9.jsonl'):
    d = json.loads(line); T = C[d['cand']]; mt, le, cm = rel(T)
    atoms = {(x,y): v for (x,y), v in d['H']}
    out = []
    for (x,y), v in sorted(atoms.items()):
        if v == x: out.append(f"{x}<={y}")
        elif v == y: out.append(f"{y}<={x}?? ({x}*{y}={y})")  # theta_y(x)=y means y <= ... actually y x y = y: half-matching
        else: out.append(f"{x}*{y}={v}")
    print(f"cand {d['cand']} concl {d['concl']}: ", ', '.join(out))
