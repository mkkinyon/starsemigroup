import sys, time; sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed'); sys.path.insert(0, '/home/claude/pa8w')
from pc3_verify import valid
from qi_extract import valid as validH
m = int(sys.argv[1])
H = {(2,1): 1, (3,0): 4, (4,1): 4, (3,2): 5, (5,0): 5, (3,1): 6}
t = time.time(); print("V m =", m, validH(7, H, ('le', 4, 6), m), f"({time.time()-t:.0f}s)", flush=True)
t = time.time(); print("R2 m =", m, valid([('x','comm',1), ('x','sees',0,1), ('y','comm',0), ('xy','sees',2)], 2, m), f"({time.time()-t:.0f}s)", flush=True)
t = time.time(); print("P1 m =", m, valid([('x','comm',0), ('x','comm',1), ('x','seen',0,2), ('x','sees',1,3)], 3, m), f"({time.time()-t:.0f}s)", flush=True)
