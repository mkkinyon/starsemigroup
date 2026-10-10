"""Abstract shortest-walk search over kinds: C_p=E0 -G- E1 -D- E2 -G- E3 ... ending at a T(c)-kind, where consecutive
Gamma-classes and Delta-classes are distinct (shortest walk).  A kind adjacency K1~K2 in Gamma is allowed only if recorded.
Since we cannot track class identity abstractly, we only impose: E1 is Gamma-adjacent to a T-kind with GT; after that
each step uses recorded adjacencies.  Report whether a T-kind (other than via the first class) is reachable."""
import sys, pickle, collections
kinds=set(); GE=set(); DE=set()
for f in sys.argv[1:]:
    k,g,d=pickle.load(open(f,'rb')); kinds|=k; GE|=g; DE|=d
Gadj=collections.defaultdict(set); Dadj=collections.defaultdict(set)
for k1,k2 in GE: Gadj[k1].add(k2)
for k1,k2 in DE: Dadj[k1].add(k2)
T=[k for k in kinds if k[0]=='T']
# BFS over (kind, next-move) ; start: kinds Gamma-adjacent to a T kind (first move within Gamma_p), next move = Delta
start=set()
for t in T:
    for k in Gadj[t]: start.add((k,'D'))
seen=set(start); q=collections.deque((s,[t for t in T if s[0] in Gadj[t]][0:1]+[s[0]]) for s in start)
hits=[]
while q:
    (k,mv),path=q.popleft()
    adj=Dadj if mv=='D' else Gadj
    for k2 in adj[k]:
        if k2[0]=='T': hits.append(path+[k2]); continue
        st=(k2,'G' if mv=='D' else 'D')
        if st not in seen: seen.add(st); q.append((st,path+[k2]))
print(len(kinds),'kinds;',len(hits),'abstract walks reaching a T(c)-kind')
for h in hits[:10]:
    print(' -> '.join(str(k) for k in h))
