import sys, pickle, time
from relrep import find_relrep
from analyse import props
fn = sys.argv[1]; mmax = int(sys.argv[2]); orders = [int(a) for a in sys.argv[3:]]
allres = pickle.load(open(fn, "rb"))
for order in orders:
    t = time.time(); cnt = {}
    for idx, (T, star) in enumerate(allres[order]):
        pr = props(T, star)
        deg = None
        for m in range(1, mmax + 1):
            if find_relrep(T, star, m):
                deg = m; break
        cnt[deg] = cnt.get(deg, 0) + 1
        if deg is None:
            print(f"order {order} #{idx}: not representable on <= {mmax} points; {pr}", flush=True)
    print(f"order {order}: {cnt} ({time.time()-t:.0f}s)", flush=True)
