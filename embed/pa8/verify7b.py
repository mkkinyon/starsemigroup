"""Verify the unproved conditions (Q), (P2), (E6), (E1) in P(P_m) by SAT (variables not assumed distinct).
Usage:  python3 verify7b.py m NAME     with NAME in Q P2 E6 E1   (one condition per process; m = 7 takes hours).
Run from the pa8/ directory of the embed kit (or set EMBED_DIR to the embed/ directory)."""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); EMBED = os.environ.get("EMBED_DIR", os.path.dirname(HERE))
sys.path.insert(0, EMBED); sys.path.insert(0, HERE)
from pc3_verify import valid
from qi_extract import valid as validH
m = int(sys.argv[1]); name = sys.argv[2]
path = {'Q': (3, [('x','comm',0), ('x','seen',1,3), ('y','comm',0), ('y','comm',2), ('y','sees',1,2)]),
        'P2': (3, [('x','comm',0), ('x','comm',2), ('x','sees',1,2), ('x','seen',1,3)])}
diag = {'E6': ({(1,7): 7, (5,1): 0, (5,2): 2, (6,2): 0, (6,5): 6, (6,7): 6, (7,2): 2}, ('mt', 0, 2)),
        'E1': ({(0,3): 0, (3,2): 0, (3,7): 7, (5,1): 0, (5,2): 2, (5,3): 3, (6,1): 6, (6,7): 6, (7,2): 2}, ('mt', 0, 2))}
t = time.time()
if name in path: r = valid(path[name][1], path[name][0], m)
else: r = validH(8, diag[name][0], diag[name][1], m)
print(name, "m =", m, "valid:", r, f"({time.time()-t:.0f}s)", flush=True)
