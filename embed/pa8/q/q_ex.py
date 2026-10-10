import pickle, numpy as np, sys
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed'); sys.path.insert(0, '/home/claude/pa8w/rp')
from pmon import mul
from blocks import top_blocks, join_classes
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); n = 4
R = pickle.load(open('instQ4.pkl', 'rb'))
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
def show(p): return ' '.join(('T' if tr else 'N') + ''.join(map(str, sorted(t))) for t, tr in top_blocks(p, n))
cnt = 0
for row in R:
    a, c, b, d, x, y = [P[i] for i in row]
    if m(a, d) != m(m(m(a, c), b), d) and len(set(row[:4])) == 4:
        cnt += 1
        if cnt <= 3:
            print("---"); 
            for nm, p in zip('acbdxy', (a, c, b, d, x, y)): print(f"  {nm} = {show(p)}")
            print("  rho:", join_classes([a, d], n), " pi:", join_classes([a, c, b, d], n))
print("instances with ad != acbd and distinct path:", cnt)
