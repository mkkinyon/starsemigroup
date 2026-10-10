import pickle, sys, itertools
from embed import PnData, find_embedding, check_embedding, semigroup_data

def props(T, star):
    n = len(T)
    P = [x for x in range(n) if star[x] == x and T[x][x] == x]
    E = [x for x in range(n) if T[x][x] == x]
    inverse = (len(E) == len(P))
    # Q1: r=prp & r=qrq => pq=qp
    q1 = True
    for p in P:
        for q in P:
            if T[p][q] != T[q][p]:
                if any(T[T[p][r]][p] == r and T[T[q][r]][q] == r for r in P):
                    q1 = False
    zero = any(all(T[z][x] == z and T[x][z] == z for x in range(n)) for z in range(n))
    one = any(all(T[z][x] == x and T[x][z] == x for x in range(n)) for z in range(n))
    return dict(n=n, nP=len(P), nE=len(E), inverse=inverse, Q1=q1, zero=zero, one=one)

def describe(T, star):
    n = len(T)
    P = [x for x in range(n) if star[x] == x and T[x][x] == x]
    lines = [f"  star = {star}, projections = {P}"]
    for x in range(n):
        lines.append("  " + " ".join(str(T[x][y]) for y in range(n)))
    return "\n".join(lines)

if __name__ == "__main__":
    fn = sys.argv[1]; nmax = int(sys.argv[2]); orders = [int(a) for a in sys.argv[3:]]
    allres = pickle.load(open(fn, "rb"))
    Ds = {n: PnData(n) for n in range(1, nmax + 1)}
    for order in orders:
        for idx, (T, star) in enumerate(allres[order]):
            pr = props(T, star)
            if pr['inverse']:
                continue
            if not pr['Q1']:
                continue
            deg = None
            for n in range(1, nmax + 1):
                if find_embedding(T, star, Ds[n]):
                    deg = n; break
            pr['deg'] = deg
            if deg is None or not pr['Q1']:
                print(f"order {order} #{idx}: {pr}")
                print(describe(T, star))
        print(f"DONE order {order}", flush=True)
