import sys, pickle, time; sys.path.insert(0,'.')
from enum_rss import *
def all_rss_stream_nontrivial(n, log=None):
    found = {}
    for star in involutions(n):
        if all(star[i] == i for i in range(n)):
            continue          # * = id  =>  commutative inverse semigroup: skip
        t = time.time(); cnt = [0]
        def cb(T, star=star):
            cnt[0] += 1
            key = canonical_fast(T, star)
            if key not in found:
                found[key] = ([row[:] for row in T], star)
            if log and cnt[0] % 200000 == 0:
                print(f"    ...{cnt[0]} tables, {len(found)} classes, {time.time()-t:.0f}s", file=log, flush=True)
        enumerate_rss(n, star, cb)
        if log:
            print(f"  n={n}, fixed points={sum(1 for i in range(n) if star[i]==i)}: {cnt[0]} tables, "
                  f"{len(found)} classes so far ({time.time()-t:.1f}s)", file=log, flush=True)
    return list(found.values())
if __name__ == "__main__":
    N = int(sys.argv[1])
    allres = pickle.load(open("rss_upto6_snapshot.pkl","rb"))
    t = time.time()
    allres[N] = all_rss_stream_nontrivial(N, log=sys.stdout)
    print(f"order {N} (nontrivial involution): {len(allres[N])} regular *-semigroups ({time.time()-t:.0f}s)", flush=True)
    with open(f"rss_nontriv{N}.pkl", "wb") as f:
        pickle.dump(allres, f)
