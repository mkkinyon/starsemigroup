import sys, pickle, collections
kinds=set(); GE=set(); DE=set()
for f in sys.argv[1:]:
    k,g,d=pickle.load(open(f,'rb')); kinds|=k; GE|=g; DE|=d
Gadj=collections.defaultdict(set); Dadj=collections.defaultdict(set)
for k1,k2 in GE: Gadj[k1].add(k2)
for k1,k2 in DE: Dadj[k1].add(k2)
def s(k): return f"{k[0]}[{','.join(k[1:4])},{k[4]}{k[5]}{k[6]}{k[7]},{k[8]},{k[9]}]"
T=[k for k in kinds if k[0]=='T']
frontier=set()
for t in T:
    for k in Gadj[t]: frontier.add((k,'D',1))
    for k in Dadj[t]: frontier.add((k,'G',1))
seen=set(frontier); order=list(frontier); hits=[]
while order:
    new=[]
    for k,mv,d in order:
        adj=Dadj if mv=='D' else Gadj
        for k2 in adj[k]:
            if k2[0]=='T': hits.append((d+1,k,mv,k2)); continue
            st=(k2,'G' if mv=='D' else 'D', d+1)
            if (k2,st[1]) not in {(a,b) for a,b,_ in seen}: seen.add(st); new.append(st)
    order=new
print(len(kinds),'kinds;',len(hits),'abstract walks reaching a T(c)-kind; shortest', min([h[0] for h in hits]) if hits else None)
for h in sorted(hits)[:6]: print(h[0], s(h[1]), h[2], '->', s(h[3]))
print('reachable:', len(seen))
