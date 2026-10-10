"""Find word identities in a,b,c,x that hold in P_m under the hypotheses of (R) but fail in T19."""
import sys, itertools
from pa_embed2 import PPm
from pmon import mul
from fourth import T19, NAMES
m=int(sys.argv[1]) if len(sys.argv)>1 else 4; L=int(sys.argv[2]) if len(sys.argv)>2 else 4
words=[w for l in range(1,L+1) for w in itertools.product('abcx',repeat=l)]
def evalw(w, val, mulf):
    r=val[w[0]]
    for ch in w[1:]: r=mulf(r,val[ch])
    return r
# T19 values
elems,T,st=T19(); idx={e:i for i,e in enumerate(elems)}
tv={'a':idx[('a','a')],'b':idx[('b','b')],'c':idx[('c','c')],'x':idx['x']}
t19={w:evalw(w,tv,lambda s,t:T[s][t]) for w in words}
# P_m instances
D=PPm(m); N=D.N; tab=D.tab; th=lambda p,q: tab[q][p]; pr=D.projs
mt=lambda p,q: th(p,q)==p and th(q,p)==q
matched={p:[q for q in range(N) if mt(p,q)] for p in range(N)}
comm={p:set(q for q in range(N) if th(p,q)==th(q,p)) for p in range(N)}
# candidate equal pairs: start with all pairs (w1<w2) that are unequal in T19; eliminate by instances
cands=set((w1,w2) for i,w1 in enumerate(words) for w2 in words[i+1:] if t19[w1]!=t19[w2])
n=0
for c in range(N):
    for a in matched[c]:
        for b in matched[c]:
            for x in comm[c]:
                if x in comm[a] and th(x,b)==th(x,c):
                    n+=1
                    val={'a':pr[a],'b':pr[b],'c':pr[c],'x':pr[x]}
                    ev={w:evalw(w,val,lambda s,t:mul(s,t,m)) for w in words}
                    cands={(w1,w2) for (w1,w2) in cands if ev[w1]==ev[w2]}
                    if not cands: break
print(n,'instances;', len(cands),'word pairs equal in all instances but not in T19')
for w1,w2 in sorted(cands,key=lambda p:(len(p[0])+len(p[1]),p)): print(''.join(w1),'=',''.join(w2))
