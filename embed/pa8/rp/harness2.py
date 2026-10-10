import sys, pickle
exec(open('harness.py').read().split("fails = {}; ex = {}; count = 0")[0])
fails = {}; ex = {}; count = 0
def chains_between(s, D):
    pass
for a, c, b, x, y in inst:
    if a == c: continue
    x = m(x, y)
    s = structure(a, c, b, x, y); count += 1
    Y = frozenset(range(n)) - s.sy
    ablocks = [(t, tr) for t, tr in top_blocks(a, n)]
    bblocks = [t for t, tr in top_blocks(b, n)]
    # S4g: Delta_i meets V_k only inside C_i (k = k(i)) and misses other V's
    for (Ai, Ci, Bi, G, Dl) in s.match:
        for V in s.V:
            if Ci <= V: check('S4g: Delta_i ∩ V_k(i) ⊆ C_i', (Dl & V) <= Ci, fails, ex, s)
            else: check('S4h: Delta_i ∩ V_k = ∅ (k≠k(i))', not (Dl & V), fails, ex, s)
        for U in s.U:
            if Ai <= U: check('S4i: Delta_i ∩ U_l(i) ⊆ A_i', (Dl & U) <= Ai, fails, ex, s)
            else: check('S4j: Delta_i ∩ U_l = ∅ (l≠l(i))', not (Dl & U), fails, ex, s)
            if Ai <= U: check('S4k: Delta_i ∩ U_l(i) ⊆ C_i', (Dl & U) <= Ci, fails, ex, s)
    # r-blocks: each meets at most one V and at most one U; T(r)-blocks inside one Gamma-class?
    for R in s.R:
        check('F4b: r-block meets ≤1 V', sum(1 for V in s.V if R & V) <= 1, fails, ex, s)
        check('F4d: r-block meets ≤1 U', sum(1 for U in s.U if R & U) <= 1, fails, ex, s)
        if R <= s.sx:
            check('F4e: r-block in supp x inside one Gamma-class', sum(1 for G in s.Gamma if R & G) <= 1, fails, ex, s)
    for R in s.RT:
        check('F4f: T(r)-block inside one Gamma-class', sum(1 for G in s.Gamma if R & G) <= 1, fails, ex, s)
        check('F4g: T(r)-block inside one Delta-class', sum(1 for G in s.Delta if R & G) <= 1, fails, ex, s)
    # Step 6': chain between a-blocks Y1,Y2 ⊆ supp y with interior a-blocks in Y => same Gamma class
    # build bipartite adjacency: a-blocks and b-blocks meeting
    ab_adj = {i: [j for j, Z in enumerate(bblocks) if ablocks[i][0] & Z] for i in range(len(ablocks))}
    ba_adj = {j: [i for i in range(len(ablocks)) if ablocks[i][0] & bblocks[j]] for j in range(len(bblocks))}
    inY = [ablocks[i][0] <= Y for i in range(len(ablocks))]
    insy = [ablocks[i][0] <= s.sy for i in range(len(ablocks))]
    # from each a-block in supp y, BFS through b-blocks and a-blocks in Y only, record reachable a-blocks in supp y
    for i0 in range(len(ablocks)):
        if not insy[i0]: continue
        seen_b = set(); frontier_a = [i0]; seen_a = {i0}; reach = set()
        while frontier_a:
            nxt = []
            for i in frontier_a:
                for j in ab_adj[i]:
                    if j in seen_b: continue
                    seen_b.add(j)
                    for i2 in ba_adj[j]:
                        if i2 == i0: continue
                        if insy[i2]: reach.add(i2)
                        elif inY[i2] and i2 not in seen_a: seen_a.add(i2); nxt.append(i2)
            frontier_a = nxt
        G0 = next(G for G in s.Gamma if ablocks[i0][0] <= G)
        for i2 in reach:
            check("Step6': a-blocks in supp y linked through Y lie in one Gamma-class", ablocks[i2][0] <= G0, fails, ex, s)
            if ablocks[i0][0] <= s.sx and ablocks[i2][0] <= s.sx:
                check("Step6'': same, both a-blocks inside supp x", ablocks[i2][0] <= G0, fails, ex, s)
print("instances (a!=c):", count)
for k, v in sorted(fails.items()): print(f"{v:6d} fail: {k}")
pickle.dump({k: (s.a, s.c, s.b, s.x, s.y) for k, s in ex.items()}, open('harness2_ex.pkl', 'wb'))
