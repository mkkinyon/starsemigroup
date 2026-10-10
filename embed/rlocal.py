"""Local block lemmas under the hypotheses of (R), tested in P(P_m)."""
import sys
from pa_embed2 import PPm
m=int(sys.argv[1]) if len(sys.argv)>1 else 4
D=PPm(m); N=D.N; tab=D.tab; th=lambda p,q: tab[q][p]; pr=D.projs
mt=lambda p,q: th(p,q)==p and th(q,p)==q
matched={p:[q for q in range(N) if mt(p,q)] for p in range(N)}
comm={p:set(q for q in range(N) if th(p,q)==th(q,p)) for p in range(N)}
def blocks(p):
    T=[];Nb=[]
    for b in pr[p]:
        top=frozenset(v for v in b if v<m)
        if not top: continue
        (T if any(v+m in b for v in top) else Nb).append(top)
    return T,Nb
def classes(p,q):
    par=list(range(m))
    def f(v):
        while par[v]!=v: par[v]=par[par[v]]; v=par[v]
        return v
    for bl in list(pr[p])+list(pr[q]):
        top=[v for v in bl if v<m]
        for v in top[1:]: par[f(top[0])]=f(v)
    return f
fails={'Nb meets 2 A':0,'Na meets 2 B':0,'B meets 2 A':0,'A meets 2 B':0,'Ai meets Bj':0,'Nb meets A and C':0,'Na meets B and C':0}
n=0
for c in range(N):
    for a in matched[c]:
        for b in matched[c]:
            for x in comm[c]:
                if x in comm[a] and th(x,b)==th(x,c):
                    n+=1
                    TA,NA=blocks(a); TB,NB=blocks(b); TC,NC=blocks(c)
                    fac=classes(a,c); fbc=classes(b,c)
                    pairs={}
                    for C in TC:
                        A=[A for A in TA if fac(min(A))==fac(min(C))][0]; B=[B for B in TB if fbc(min(B))==fbc(min(C))][0]; pairs[A]=B
                    for Z in NB:
                        if sum(1 for A in TA if Z&A)>=2: fails['Nb meets 2 A']+=1
                        if any(Z&A for A in TA) and any(Z&C for C in TC): fails['Nb meets A and C']+=1
                    for Y in NA:
                        if sum(1 for B in TB if Y&B)>=2: fails['Na meets 2 B']+=1
                        if any(Y&B for B in TB) and any(Y&C for C in TC): fails['Na meets B and C']+=1
                    for B in TB:
                        if sum(1 for A in TA if B&A)>=2: fails['B meets 2 A']+=1
                    for A in TA:
                        if sum(1 for B in TB if B&A)>=2: fails['A meets 2 B']+=1
                        for B in TB:
                            if A&B and pairs[A]!=B: fails['Ai meets Bj']+=1
print(m, n,'instances', fails)
