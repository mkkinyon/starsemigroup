import json, sys
C = json.load(open('/home/claude/pa8w/embed/pa8/cand9.json')); nm = 'abcdefghi'
for k in map(int, sys.argv[1:]):
    T = C[k]; n = 9; th = lambda p, q: T[q][p]
    print(f"=== cand {k}: table theta_p(q) (rows p, cols q)")
    print("   " + "  ".join(nm))
    for p in range(n): print(nm[p], " ", "  ".join(nm[th(p,q)] for q in range(n)))
    bottom = [nm[p] for p in range(n) if all(th(p,q)==p for q in range(n))]
    mt = [nm[p]+'~'+nm[q] for p in range(n) for q in range(n) if p<q and th(p,q)==p and th(q,p)==q]
    cm = [nm[p]+nm[q] for p in range(n) for q in range(n) if p<q and th(p,q)==th(q,p) and not (th(p,q)==p and th(q,p)==q)]
    le = [nm[p]+'<='+nm[q] for p in range(n) for q in range(n) if p!=q and th(q,p)==p]
    print("bottom:", bottom, "| matched:", mt, "| commute:", cm, "| <=:", le)
