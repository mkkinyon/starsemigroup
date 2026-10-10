import sys, time, itertools
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
base=[('mt','a','c'), ('mt','c','b')]
H={1:('mt','b','q'),2:('comm','p','c'),3:('comm','p','q'),4:('le','p','k'),5:('le','q','k'),6:('comm','k','a'),7:('comm','k','c'),
   8:('eq',('p','a'),('p','c')),9:('eq',('q','a'),('q','c')),10:('eq',('k','b'),'q'),11:('eq',('k','b'),('q','b'))}
cache={}
def ok(S,m=4):
    key=(frozenset(S),m)
    if key not in cache:
        try: cache[key]=valid(base+[H[i] for i in sorted(S)],('mt','a','b'),m)
        except ValueError: cache[key]=None
    return cache[key]
full=frozenset(H); print('full valid m=4:',ok(full),flush=True)
# enumerate subsets by increasing size; minimal = valid and no proper subset valid
minimal=[]
for r in range(1,len(H)+1):
    for S in itertools.combinations(sorted(H),r):
        S=frozenset(S)
        if any(M<=S for M in minimal): continue
        if ok(S): minimal.append(S); print('minimal (m=4):',sorted(S),[H[i] for i in sorted(S)],flush=True)
print(len(minimal),'minimal sets; checking at m=5')
for S in minimal: print(sorted(S),'m=5:',ok(S,5),flush=True)
