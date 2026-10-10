import sys, pickle, collections
kinds=set(); GE=set(); DE=set()
for f in sys.argv[1:]:
    k,g,d=pickle.load(open(f,'rb')); kinds|=k; GE|=g; DE|=d
Gadj=collections.defaultdict(set); Dadj=collections.defaultdict(set)
for k1,k2 in GE: Gadj[k1].add(k2)
for k1,k2 in DE: Dadj[k1].add(k2)
def s(k): return f"{k[0]}[{','.join(k[1:4])},{k[4]}{k[5]}{k[6]}{k[7]},{k[8]},{k[9]}]"
T=[k for k in kinds if k[0]=='T']
# BFS with paths, both starts; report shortest hits with full kind sequence
q=collections.deque()
for t in T:
    for k in Gadj[t]: q.append(([t,k],'D'))
    for k in Dadj[t]: q.append(([t,k],'G'))
seen=set(); hits=[]
while q:
    path,mv=q.popleft()
    k=path[-1]
    key=(k,mv)
    if key in seen: continue
    seen.add(key)
    adj=Dadj if mv=='D' else Gadj
    for k2 in adj[k]:
        if k2[0]=='T':
            if len(path)>=3: hits.append(path+[k2])   # exclude trivial back-moves (length-2 walks T-K-T are 'back' moves to C_p itself... keep >=3 steps)
            continue
        q.append((path+[k2],'G' if mv=='D' else 'D'))
hits.sort(key=len)
print(len(hits),'hits')
for h in hits[:8]:
    print(' -> '.join(s(k) for k in h)); print()
