import json
T=json.load(open('mk10_T.json')); n=10; th=lambda p,q:T[p][q]
nm='a b c k p q 6 7 8 9'.split()
for x in range(n): print(f"theta_{nm[x]}: " + ' '.join(f"{nm[y]}->{nm[th(y,x)]}" for y in range(n) if y!=x))
le=lambda x,y: th(x,y)==x
mt=lambda x,y: th(y,x)==x and th(x,y)==y
print('x<y :',[(nm[x],nm[y]) for x in range(n) for y in range(n) if x!=y and le(x,y)])
print('x~y :',[(nm[x],nm[y]) for x in range(n) for y in range(x+1,n) if th(x,y)==th(y,x)])
print('x|><|y :',[(nm[x],nm[y]) for x in range(n) for y in range(x+1,n) if mt(x,y) and x!=y])
print('identify a with c:',[nm[x] for x in range(n) if th(0,x)==th(2,x)])
