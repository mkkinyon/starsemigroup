import json
rows = """0,6,2,8,7,9,6,7,8,9,
8,1,2,5,9,5,6,7,8,9,
0,1,2,7,7,9,6,7,8,9,
8,1,7,3,4,5,6,7,8,9,
8,6,7,4,4,9,6,7,8,9,
8,1,7,5,9,5,6,7,8,9,
8,6,7,9,9,9,6,7,8,9,
8,6,7,7,7,9,6,7,8,9,
8,6,7,8,7,9,6,7,8,9,
8,6,7,9,9,9,6,7,8,9"""
v = [int(x) for x in rows.replace('\n','').split(',') if x.strip()!='']
T = [v[10*i:10*i+10] for i in range(10)]
json.dump(T, open('mk10_T.json','w'))
json.dump({'T':T,'names':['a','b','c','k','p','q','6','7','8','9']}, open('mk10.json','w'))
# sanity: idempotent, axioms
th = lambda p,q: T[p][q]
n=10
ok=True
for x in range(n):
    if T[x][x]!=x: ok=False
for x in range(n):
  for y in range(n):
    if T[T[y][x]][x]!=T[y][x] or T[T[x][y]][x]!=T[y][x]: ok=False; print('ax',x,y)
    for z in range(n):
      if T[T[T[z][x]][y]][x]!=T[z][T[y][x]]: ok=False; print('ax4',x,y,z)
      if T[T[T[T[z][x]][y]][x]][y]!=T[T[z][x]][y]: ok=False; print('ax5')
      if T[z][x]==z and T[z][y]==z and T[x][y]!=T[y][x]: ok=False; print('Q1',x,y,z)
print('axioms+Q1:', ok)
a,b,c,k,p,q=0,1,2,3,4,5
mt=lambda x,y: th(x,y)==x and th(y,x)==y
print('a|><|c',mt(a,c),'c|><|b',mt(c,b),'a|><|b',mt(a,b))
print('p~c',th(p,c)==th(c,p),'p~q',th(p,q)==th(q,p),'th_p(a)=th_p(c)',th(a,p)==th(c,p),'th_q(a)=th_q(c)',th(a,q)==th(c,q),'k~a',th(k,a)==th(a,k),'th_q(b)=th_k(b)',th(b,q)==th(b,k))
# order
le=lambda x,y: th(x,y)==x
print('order pairs:', [(x,y) for x in range(n) for y in range(n) if x!=y and le(x,y)])
print('comm pairs:', [(x,y) for x in range(n) for y in range(x+1,n) if th(x,y)==th(y,x)])
print('matched pairs:', [(x,y) for x in range(n) for y in range(x+1,n) if mt(x,y)])
