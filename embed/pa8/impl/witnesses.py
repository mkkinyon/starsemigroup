"""Collect the known non-embeddable algebras (tables T[i][j] = i*j) and compute which labelled conditions each violates."""
import sys, json, re, pickle, os, itertools, time
sys.path.insert(0,'/home/claude/pa8w/embed'); sys.path.insert(0,'/home/claude/pa8w/embed/pa8/wn')
E='/home/claude/pa8w/embed/pa8/'
algs={}
# P_7
P7names='a c b x u v w'.split()
rows='''a a u u u u u
c c c v v v v
w b b w w w w
u v v x u v v
u u u u u u u
v v v v v v v
w w w w w w w'''.split('\n')
th={p:dict(zip(P7names,r.split())) for p,r in zip(P7names,rows)}
algs['P7']=[[P7names.index(th[p][q]) for p in P7names] for q in P7names]
# frak P (order 6): a~c, b~c, b~d, w~z; theta_a(b)=theta_b(a)=w, theta_c(d)=theta_d(c)=z, theta_a(d)=w, theta_d(a)=z, theta_a(z)=theta_b(z)=w, theta_c(w)=theta_d(w)=z, theta_w=w, theta_z=z
N6='a b c d w z'.split()
def thP(p,q):
    if p==q: return p
    if p in 'wz': return p
    M={('a','c'),('c','a'),('b','c'),('c','b'),('b','d'),('d','b')}
    if (p,q) in M: return p
    return 'w' if p in 'ab' else 'z'
algs['frakP']=[[N6.index(thP(p,q)) for p in N6] for q in N6]
# P_8^1..7
P8=[json.loads(l)['A'] for l in open(E+'post8.log') if json.loads(l).get('embeds') is None]
for i,T in enumerate(P8): algs[f'P8^{i+1}']=T
# order-9: candidates and the (R')-witness
C9=json.load(open(E+'cand9.json'))
for i,T in enumerate(C9): algs[f'cand9[{i}]']=T
for f in ['post9_0.log','post9_1.log','post9_3.log']:
    for l in open(E+f):
        r=json.loads(l)
        if r.get('embeds') is None and r.get('minimal') and r.get('violates',[None])[0]=='Rprime': algs['R9']=r['A']
# P(Q0), MK's W3 model, P^ch_3, P^ch_4
algs['P(Q0)']=json.load(open(E+'w3/model11b.json')); algs['MK11']=json.load(open(E+'w3/model11.json'))
from family import build
for n in (3,4): algs[f'Pch{n}']=build(n)[0]
# P_9 (order 9, violates S, P2, Q): from pathclose_check P9 table
P9names='a b c d m n k w z'.split()
rows9='''a m a m m m m w w
m b b b m m m w w
c c c z n n z z z
k d z d k z k z z
m m m m m m m w w
n n n z n n z z z
k k z k k z k z z
w w w w w w w w w
z z z z z z z z z'''.split('\n')
th9={p:dict(zip(P9names,r.split())) for p,r in zip(P9names,rows9)}
algs['P9']=[[P9names.index(th9[p][q]) for p in P9names] for q in P9names]
json.dump(algs, open('algs.json','w'))
print({k:len(v) for k,v in algs.items()})
