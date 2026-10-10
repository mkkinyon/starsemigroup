import sys, json
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import violated_in
P = [('mt','a','c'), ('mt','c','b')]
def chain(pattern, end='b'):
    names = ['x','y','z','t'][:len(pattern)]
    H = P + [('comm',names[0],'c'), ('comm',names[-1],end)]
    for p,q in zip(names,names[1:]): H.append(('comm',p,q))
    for p,idn in zip(names,pattern): H.append(('eq',(p,idn),(p,'c')))
    return H
conds = {'W2(aa)':chain('aa'),'ab':chain('ab'),'ba':chain('ba'),'W3(aaa)':chain('aaa'),'aab':chain('aab'),'aba':chain('aba'),'abb':chain('abb'),'bba':chain('bba')}
E='/home/claude/pa8w/embed/pa8/'
algs=[]
for f in ['post9_0.log','post9_1.log','post9_3.log','post8.log']:
    for l in open(E+f):
        r=json.loads(l)
        if r.get('embeds') is None: algs.append((f,r))
print(len(algs),'non-embeddable algebras of order 8,9', flush=True)
from collections import Counter
cnt=Counter()
for f,r in algs:
    T=r['A']; viol=tuple(k for k,H in conds.items() if violated_in(T,H,('mt','a','b')))
    cnt[(viol, r.get('violates',[None])[0], r.get('minimal'))]+=1
    if viol: print(viol, r.get('violates',[None])[0], r.get('minimal'), flush=True)
for k,v in sorted(cnt.items(), key=lambda kv:-kv[1]): print(v, k)
