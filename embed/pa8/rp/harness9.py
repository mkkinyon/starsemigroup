import sys, pickle
exec(open('harness.py').read().split("fails = {}; ex = {}; count = 0")[0])
fails = {}; ex = {}; count = 0
def connected(blocks_a, blocks_b, start, goal):
    # bipartite adjacency by intersection; BFS
    front = [start]; seenA = {start}; seenB = set()
    while front:
        nxt = []
        for A in front:
            for Bk in blocks_b:
                if Bk in seenB or not (A & Bk): continue
                seenB.add(Bk)
                if Bk == goal: return True
                for A2 in blocks_a:
                    if A2 not in seenA and (A2 & Bk): seenA.add(A2); nxt.append(A2)
        front = nxt
    return False
for a, c, b, x, y in inst:
    if a == c: continue
    x = m(x, y)
    s = structure(a, c, b, x, y); count += 1
    cbl = [t for t, tr in top_blocks(c, n)]; bbl = [t for t, tr in top_blocks(b, n)]; abl = [t for t, tr in top_blocks(a, n)]
    for (Ai, Ci, Bi, G, Dl) in s.match:
        if Ai <= s.sy: continue
        cb_noNx = [E for E in cbl if not (E in s.Nc and E <= s.sx)]
        check('S33: i∉I: C_i ~ B_i in b∨c avoiding N(c)-blocks in supp x', connected(cb_noNx, bbl, Ci, Bi), fails, ex, s)
        cb_Y = [E for E in cbl if not (E & s.sy)]
        check('S34: i∉I: C_i ~ B_i in b∨c using only c-blocks in Y', connected(cb_Y, bbl, Ci, Bi), fails, ex, s)
        # rho-chain from A_i to B_i using only a-blocks in Y
        ab_Y = [E for E in abl if not (E & s.sy)]
        check('S35: i∉I: A_i ~ B_i in a∨b using only a-blocks in Y', connected(ab_Y, bbl, Ai, Bi), fails, ex, s)
    for (Ai, Ci, Bi, G, Dl) in s.match:
        if not (Ai <= s.sy): continue
        # i in I: A_i ~ B_i in rho: via which a-blocks? test: using only a-blocks in Gamma_i ∪ Y
        ab_ok = [E for E in abl if E <= G or not (E & s.sy)]
        check('S36: i∈I: A_i ~ B_i in a∨b using only a-blocks in Gamma_i or Y', connected(ab_ok, bbl, Ai, Bi), fails, ex, s)
        ab_ok2 = [E for E in abl if E <= G]
        check('S37: i∈I: A_i ~ B_i in a∨b using only a-blocks in Gamma_i', connected(ab_ok2, bbl, Ai, Bi), fails, ex, s)
print("instances (a!=c):", count)
for k, v in sorted(fails.items()): print(f"{v:6d} fail: {k}")
pickle.dump({k: (s.a, s.c, s.b, s.x, s.y) for k, s in ex.items()}, open('harness9_ex.pkl', 'wb'))
