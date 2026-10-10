import sys, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
P = [('mt','a','c'), ('mt','c','b')]
def chain(names):
    H = P + [('comm',names[0],'c'), ('comm',names[-1],'b')]
    for p,q in zip(names,names[1:]): H.append(('comm',p,q))
    for p in names: H.append(('eq',(p,'a'),(p,'c')))
    return H
for arg in sys.argv[1:]:
    k, m = map(int, arg.split(':')); names = ['x','y','z','t','s'][:k]
    t0=time.time(); print(f"W_{k} m={m}: {valid(chain(names), ('mt','a','b'), m)} ({time.time()-t0:.0f}s)", flush=True)
