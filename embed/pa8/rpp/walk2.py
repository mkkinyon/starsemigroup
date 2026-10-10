import sys, pickle, collections
kinds=set(); GE=set(); DE=set()
for f in sys.argv[1:]:
    k,g,d=pickle.load(open(f,'rb')); kinds|=k; GE|=g; DE|=d
Gadj=collections.defaultdict(set); Dadj=collections.defaultdict(set)
for k1,k2 in GE: Gadj[k1].add(k2)
for k1,k2 in DE: Dadj[k1].add(k2)
def s(k): return f"{k[0]}[{k[1]},{k[2]},{k[3]}{k[4]},{k[5]},{k[6]}]"
T=[k for k in kinds if k[0]=='T']
print("T(c)-kinds:"); [print('  ',s(t)) for t in sorted(T)]
level={}
frontier=set()
for t in T:
    for k in Gadj[t]: frontier.add((k,'D'))
seen=set(frontier); order=list(frontier)
while order:
    new=[]
    for k,mv in order:
        adj=Dadj if mv=='D' else Gadj
        for k2 in adj[k]:
            st=(k2,'G' if mv=='D' else 'D')
            if st not in seen: seen.add(st); new.append(st)
    order=new
print("\nreachable (kind, next move):")
for k,mv in sorted(seen): print('  ',s(k),'next',mv, '  G-nbrs:',sorted(set(s(j) for j in Gadj[k])) if mv=='G' else '  D-nbrs:',sorted(set(s(j) for j in Dadj[k])) if mv=='D' else '')
