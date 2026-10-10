"""Post-processing of the order-8 census (resumable).  For every finished chunk (chunk_*.done with a count), parse the
models, reduce up to isomorphism (canonical forms, kept in canon.pkl), and for each new algebra test the triangle
condition and embeddability: backtracking into P(P_m), m <= 4, then SAT for m = 5..MS.  Results: one JSON line per
algebra in pa8_post.log; the set of processed chunk names in chunks_done.txt.  Usage: python3 pa8_post.py [MS]"""
import sys, os, glob, json, pickle, time
HERE = os.path.dirname(os.path.abspath(__file__)); EMBED = os.path.dirname(HERE)
sys.path.insert(0, EMBED)
from mace4parse import parse_models
from layered_search import canon
from pa7_post import triangle_ok
from pa_embed2 import PPm, embed
from pa_sat import solve

MS = int(sys.argv[1]) if len(sys.argv) > 1 else 7
CAN = os.path.join(HERE, "canon.pkl"); LOG = os.path.join(HERE, "pa8_post.log"); DONE = os.path.join(HERE, "chunks_done.txt")
seen = pickle.load(open(CAN, "rb")) if os.path.exists(CAN) else set()
done = set(open(DONE).read().split()) if os.path.exists(DONE) else set()
Ds = {}
stats = dict(new=0, tri_fail=0, emb=0, nonemb=0)
for f in sorted(glob.glob(os.path.join(HERE, "chunk_*.out"))):
    name = os.path.basename(f)[:-4]
    if name in done or not os.path.exists(f[:-4] + ".done"): continue
    if open(f[:-4] + ".done").read().strip() == "skipped": done.add(name); continue
    t0 = time.time(); n_new = 0
    for N, T, c in parse_models(open(f).read()):
        key = canon(T)
        if key in seen: continue
        seen.add(key); n_new += 1; stats["new"] += 1
        A = [list(r) for r in key]
        tri = triangle_ok(A)
        rec = dict(chunk=name, A=A, triangle=tri, embeds=None)
        if tri:
            found = None
            for m in range(1, 5):
                if m not in Ds: Ds[m] = PPm(m)
                r = embed(A, Ds[m], limit=30)
                if r == "timeout": break
                if r is not None: found = m; break
            if found is None:
                for m in range(5, MS + 1):
                    if solve(A, m, verbose=False): found = m; break
            rec["embeds"] = found
            stats["emb" if found else "nonemb"] += 1
            if not found: print("CANDIDATE (no embedding into P(P_m), m <=", MS, "):", A, flush=True)
        else: stats["tri_fail"] += 1
        with open(LOG, "a") as g: g.write(json.dumps(rec) + "\n")
    done.add(name)
    pickle.dump(seen, open(CAN + ".tmp", "wb")); os.replace(CAN + ".tmp", CAN)
    open(DONE, "w").write("\n".join(sorted(done)) + "\n")
    print(f"{name}: {n_new} new algebras ({time.time()-t0:.0f}s); totals {stats}, {len(seen)} algebras so far", flush=True)
print("done:", stats, len(seen), "algebras up to isomorphism")
