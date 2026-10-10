import sys, json
from mace4parse import parse_models
from pa_sat import solve
N,T,c = list(parse_models(open('mace_WnotS9.out').read()))[0]
for m in range(int(sys.argv[1]), int(sys.argv[2])+1):
    r = solve(T, m)
    if r:
        for p,b in enumerate(r): print(p,b)
        break
