import sys, json, itertools, numpy as np, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from pathclose4b import atoms_for, fmt
from verify_hits import valid
n = 4; atoms = atoms_for(n); nat = len(atoms); RB = (nat + 7) // 8
C9 = json.load(open('/home/claude/pa8w/embed/pa8/cand9.json'))
negu = np.unique(np.fromfile('all_5_4.neg', dtype=np.uint8).reshape(-1, RB), axis=0)
exec(open('explain9.py').read().split("for c in (1, 3):")[0].split("negu = np.unique")[0].split("neg = np.fromfile")[0])  # imports only
from explain9 import rows_for  # noqa (explain9 runs at import; avoid) 
