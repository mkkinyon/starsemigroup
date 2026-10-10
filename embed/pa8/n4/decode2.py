import json
C = json.load(open('/home/claude/pa8w/embed/pa8/cand9.json'))
names = 'abcdefghi'
def pretty(T, H, concl):
    atoms = {(x,y): v for (x,y), v in H}
    out = []; used = set()
    for (x,y), v in sorted(atoms.items()):
        if (x,y) in used: continue
        if v == x and atoms.get((y,x)) == y: out.append(f"{names[x]}⋈{names[y]}"); used.add((y,x))
        elif v == x: out.append(f"{names[x]}≤{names[y]}")
        elif v == y: out.append(f"{names[y]}{names[x]}{names[y]}={names[y]}")
        elif atoms.get((y,x)) == v: out.append(f"{names[x]}{names[y]}={names[y]}{names[x]}={names[v]}"); used.add((y,x))
        else: out.append(f"{names[y]}{names[x]}{names[y]}={names[v]}")
    c = concl
    cs = f"{names[c[1]]}⋈{names[c[2]]}" if c[0]=='mt' else f"{names[c[1]]}≤{names[c[2]]}"
    return ', '.join(out) + '  ⇒  ' + cs
for line in open('/home/claude/pa8w/embed/pa8/qi_all9.jsonl'):
    d = json.loads(line)
    vars_ = sorted({x for (x,y),v in d['H'] for x in (x,y,v)} | set(d['concl'][1:]))
    print(f"cand {d['cand']} ({len(vars_)} vars, {d['n']} atoms): ", pretty(C[d['cand']], d['H'], d['concl']))
