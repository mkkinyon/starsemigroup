import sys, time
sys.path.insert(0, '..')
from verify import rees, cyclic_group, square_band, rees0
from verify3 import group_over_band
from embed import PnData, find_embedding, check_embedding

def star_of(mul):
    # regular involution: use find_inversions from verify (first one)
    from verify import find_inversions
    invs = find_inversions(mul)
    return invs

def test(name, mul, star, nmax):
    for n in range(1, nmax+1):
        t=time.time()
        D = PnData(n)
        sols = find_embedding(mul, star, D)
        if sols:
            check_embedding(mul, star, sols[0], D)
            print(f"{name}: |S|={len(mul)} embeds in P_{n}  ({time.time()-t:.1f}s)"); return n
        print(f"   {name}: not in P_{n} ({time.time()-t:.1f}s)", flush=True)
    print(f"{name}: |S|={len(mul)} does not embed in P_n for n<={nmax}")

if __name__ == "__main__":
    nmax = int(sys.argv[1])
    Z2 = cyclic_group(2); Z3 = cyclic_group(3)
    # M[Z2;3,3;P] non flat: p01 = t
    M = rees(Z2, range(3), [[0,1,0],[1,0,0],[0,0,0]])
    invs = star_of(M); print("M[Z2;3,3] involutions:", len(invs))
    test("M[Z2;3,3;nonflat]", M, invs[0], nmax)
    M3 = rees(Z3, range(3), [[0,1,0],[2,0,0],[0,0,0]])
    invs = star_of(M3); print("M[Z3;3,3] involutions:", len(invs))
    test("M[Z3;3,3;nonflat]", M3, invs[0], nmax)
    # 48-element example 4.6
    P = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 2, 0, 0], [2, 0, 0, 0]]
    M4 = rees(Z3, range(4), P)
    invs = star_of(M4); print("Ex 4.6 involutions:", len(invs))
    test("Example 4.6 (48 el.)", M4, invs[0], nmax)
