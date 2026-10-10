import sys, json; sys.path.insert(0, '/home/claude/pa8w')
from pc3_hit import full_valid_ones
cands = json.load(open('/home/claude/pa8w/cand9.json'))
n, K = int(sys.argv[1]), int(sys.argv[2])
for ci in range(len(cands)):
    print("=== order-9 candidate", ci, "===", flush=True)
    g = full_valid_ones(cands[ci], 4, n, K, m2=None, verbose=False)
    import pickle
    d = pickle.load(open(f'/home/claude/pa8w/pc3sig_4_{n}.pkl', 'rb')); atoms = d['atoms']
    from pathclose3 import fmt2
    V = ['p%d' % i for i in range(n + 1)]
    for H in g[:6]:
        print("  ", [fmt2(atoms[k], V) for k in range(len(atoms)) if H >> k & 1], flush=True)
    print("  total", len(g), flush=True)
