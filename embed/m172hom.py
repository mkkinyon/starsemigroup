"""All kernels of homomorphisms M172 -> P(P_m)."""
import sys, time, itertools
from pa_embed2 import PPm
T = [[0,0,0,3,3,3],[0,1,0,3,3,5],[0,0,2,3,4,5],[0,0,0,3,3,3],[0,0,2,3,4,3],[0,1,2,3,3,5]]
names = {0:'w',1:'a',2:'b',3:'z',4:'d',5:'c'}
k = 6
m = int(sys.argv[1]); D = PPm(m); tab = D.tab; N = D.N
kernels = {}
img = [-1]*k
def forced():
    for x in range(k):
        if img[x] < 0: continue
        for y in range(k):
            if img[y] < 0: continue
            if img[T[x][y]] < 0: return T[x][y], tab[img[x]][img[y]]
    return None
def consistent():
    for x in range(k):
        if img[x] < 0: continue
        for y in range(k):
            if img[y] < 0: continue
            z = img[T[x][y]]
            if z >= 0 and z != tab[img[x]][img[y]]: return False
    return True
def rec(depth):
    if all(v >= 0 for v in img):
        ker = tuple(sorted((names[x], names[y]) for x in range(k) for y in range(x+1, k) if img[x] == img[y]))
        if ker not in kernels: kernels[ker] = list(img)
        return
    f = forced()
    if f is not None:
        z, v = f; img[z] = v
        if consistent(): rec(depth+1)
        img[z] = -1; return
    x = next(i for i in range(k) if img[i] < 0)
    for v in (D.reps if depth == 0 else range(N)):
        img[x] = v
        if consistent(): rec(depth+1)
        img[x] = -1
t = time.time(); rec(0)
print(f"P(P_{m}): {len(kernels)} kernels ({time.time()-t:.0f}s)")
for ker in sorted(kernels, key=len): print("  identified:", ker if ker else "none (embedding)")
