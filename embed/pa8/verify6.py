import json, sys, time; sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed'); sys.path.insert(0, '/home/claude/pa8w')
from pc3_verify import valid
from qi_extract import valid as validH
conds = {
 'P1': (3, [('x','comm',0), ('x','comm',1), ('x','seen',0,2), ('x','sees',1,3)]),
 'P2': (3, [('x','comm',0), ('x','comm',2), ('x','sees',1,2), ('x','seen',1,3)]),
 'P2b': (3, [('x','comm',0), ('x','comm',2), ('x','seen',1,3), ('x','sees',2,3)]),
 'P1c': (3, [('x','comm',0), ('x','comm',1), ('x','comm',2), ('x','sees',0,2), ('x','sees',1,3)]),
 'Q4': (3, [('x','comm',0), ('x','seen',1,3), ('y','comm',0), ('y','comm',2), ('y','sees',1,2)]),
 'R2': (2, [('x','comm',1), ('x','sees',0,1), ('y','comm',0), ('xy','sees',2)]),
}
m = int(sys.argv[1])
for name, (n, H) in conds.items():
    t = time.time(); r = valid(H, n, m); print(name, "m =", m, r, f"({time.time()-t:.0f}s)", flush=True)
# diagram-type ones: E6 (cand 5) and E1 (cand 0), as partial tables T[x][y] = theta_y(x)
E6 = ({(1,7): 7, (5,1): 0, (5,2): 2, (6,2): 0, (6,5): 6, (6,7): 6, (7,2): 2}, ('mt', 0, 2))
E1 = ({(0,3): 0, (3,2): 0, (3,7): 7, (5,1): 0, (5,2): 2, (5,3): 3, (6,1): 6, (6,7): 6, (7,2): 2}, ('mt', 0, 2))
for name, (H, concl) in (('E6', E6), ('E1', E1)):
    t = time.time(); r = validH(8, H, concl, m); print(name, "m =", m, r, f"({time.time()-t:.0f}s)", flush=True)
