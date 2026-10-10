import sys, time, pickle
exec(open('goal2.py').read().split("t = time.time()")[0])
S, new = pickle.load(open('inv5_m4_K3.pkl', 'rb'))
# greedy minimisation: try removing each clause, keep removal if closing still valid
cur = list(S); t0 = time.time()
assert valid_mt(weak, cur + [GOAL])
# remove the trivial ones first (those valid under weak hyps alone are harmless but keep them out of the minimal set)
for cl in list(cur):
    trial = [c2 for c2 in cur if c2 != cl]
    if valid_mt(weak, trial + [GOAL]): cur = trial
print(f"m={m}: minimal set of {len(cur)} local clauses with GOAL closing the path ({time.time()-t0:.0f}s):", flush=True)
for cl in cur: print('   ', fmt(cl), '  [x-link]' if cl in new else '  [weak]')
pickle.dump(cur, open(f'goal3_min_m{m}.pkl', 'wb'))
