import sys, time, pickle
exec(open('goal2.py').read().split("t = time.time()")[0])
S, new = pickle.load(open('inv5_m4_K3.pkl', 'rb'))
G1 = ((-1, ('E', 'c')), (1, ('J', 'a', 'b')))
def minimise(goal, pool, label):
    cur = [cl for cl in pool if cl != goal]
    assert holds(weak, cur, goal), label + ': not even with all'
    for cl in list(cur):
        trial = [c2 for c2 in cur if c2 != cl]
        if holds(weak, trial, goal): cur = trial
    print(f"m={m}: {label}: minimal set of {len(cur)} local clauses implying it:", flush=True)
    for cl in cur: print('   ', fmt(cl), '  [x-link]' if cl in new else '  [weak]')
    return cur
# prefer clauses not involving b (so that they can be chain invariants): try pool = clauses without b first
nob = [cl for cl in S if not any('b' in a[1:] for s, a in cl)]
print(len(nob), 'clauses without b')
for goal, label in ((G1, 'G1'), (GOAL, 'GOAL')):
    if holds(weak, nob, goal): minimise(goal, nob, label + ' (from b-free clauses)')
    else:
        print(f"m={m}: {label} does not follow from the b-free clauses")
        minimise(goal, S, label + ' (all clauses)')
