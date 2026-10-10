import sys, itertools, time
from embed import PnData, find_embedding, check_embedding
from normalband import strong_semilattice_band
from enum_rss import is_rss

def test(name, T, star, nmax, Ds):
    for n in range(1, nmax + 1):
        t = time.time(); sols = find_embedding(T, star, Ds[n])
        if sols:
            check_embedding(T, star, sols[0], Ds[n]); print(f"{name}: |B|={len(T)} embeds in P_{n}"); return n
    print(f"{name}: |B|={len(T)} NOT in P_n, n<={nmax}"); return None

nmax = int(sys.argv[1]); Ds = {n: PnData(n) for n in range(1, nmax+1)}
# Y = {a1, a2, g, y, 0}: 0<y<a1, 0<g<a1, g<a2
Y = ['a1','a2','g','y','0']
order = {('0','y'),('0','g'),('0','a1'),('0','a2'),('y','a1'),('g','a1'),('g','a2')}
leq = lambda x,z: x==z or (x,z) in order
cases = []
# case 1: all singletons except A_y, A_0
A = {'a1':[1],'a2':[1],'g':[1],'y':[1,2],'0':[1,2]}
f = {('a1','g'):{1:1},('a2','g'):{1:1},('a1','y'):{1:1},('y','0'):{1:1,2:2},('g','0'):{1:1},('a1','0'):{1:1},('a2','0'):{1:1}}
cases.append(("case1", A, f))
# case 2: A_a1 = {1,2}, A_y = {1,2,3}, A_g={1,2}, A_a2={1,2}, A_0={1,2,3}
A = {'a1':[1,2],'a2':[1,2],'g':[1,2],'y':[1,2,3],'0':[1,2,3]}
f = {('a1','g'):{1:1,2:2},('a2','g'):{1:1,2:2},('a1','y'):{1:1,2:2},('y','0'):{1:1,2:2,3:3},('g','0'):{1:1,2:2},('a1','0'):{1:1,2:2},('a2','0'):{1:1,2:2}}
cases.append(("case2", A, f))
# case 3: a2 maps differently into g than a1 does not matter (images intersect anyway); twist y
A = {'a1':[1,2],'a2':[1],'g':[1,2],'y':[1,2],'0':[1,2]}
f = {('a1','g'):{1:1,2:2},('a2','g'):{1:2},('a1','y'):{1:2,2:1},('y','0'):{1:1,2:2},('g','0'):{1:1,2:2},('a1','0'):{1:1,2:2},('a2','0'):{1:2}}
cases.append(("case3", A, f))
for name, A, f in cases:
    T, star, elems = strong_semilattice_band(Y, leq, A, f)
    assert is_rss(T, star)
    test(name, T, star, nmax, Ds)
