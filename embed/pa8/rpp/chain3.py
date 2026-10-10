import sys, time, itertools
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
P = [('mt','a','c'), ('mt','c','b')]
def chain(pattern, end='b'):
    names = ['x','y','z','t'][:len(pattern)]
    H = P + [('comm',names[0],'c'), ('comm',names[-1],end)]
    for p,q in zip(names,names[1:]): H.append(('comm',p,q))
    for p,idn in zip(names,pattern): H.append(('eq',(p,idn),(p,'c')))
    return H
n=int(sys.argv[1])
for pattern in itertools.product('ab', repeat=n):
    H = chain(pattern); t=time.time()
    v4 = valid(H, ('mt','a','b'), 4)
    deg = v4 and (valid(H, ('eq','a','c'), 4) or valid(H, ('eq','b','c'), 4))
    v5 = valid(H, ('mt','a','b'), 5) if v4 and not deg else None
    print(f"chain c~{'~'.join(['x','y','z','t'][:n])}~b, identifications {''.join(pattern)}=c: m4 {v4}, degenerate {deg}, m5 {v5} ({time.time()-t:.0f}s)", flush=True)
