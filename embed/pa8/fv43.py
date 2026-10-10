import sys, json; sys.path.insert(0, '/home/claude/pa8w')
from pc3_hit import full_valid_ones
recs = [json.loads(l) for l in open('/home/claude/pa8w/post8.log')]
cands = [r["A"] for r in recs if r["embeds"] is None]
K = int(sys.argv[1])
for ci in [int(a) for a in sys.argv[2:]]:
    print("=== candidate", ci, "===", flush=True)
    full_valid_ones(cands[ci], 4, 3, K)
