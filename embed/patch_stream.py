s=open("enum_rss.py").read()
s=s.replace("def enumerate_rss(n, star):", "def enumerate_rss(n, star, callback=None):")
s=s.replace("""        if k == len(order):
            results.append([row[:] for row in T])
            return""", """        if k == len(order):
            if callback is None:
                results.append([row[:] for row in T])
            else:
                callback(T)
            return""")
s += '''

def all_rss_stream(n, log=None):
    found = {}
    for star in involutions(n):
        t = time.time()
        cnt = [0]
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
'''
open("enum_rss.py","w").write(s)
