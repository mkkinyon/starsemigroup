from pmon import Pn, partition_monoid, projections, star, mul
n = 3
P = Pn(n); E = [x for x in partition_monoid(n) if mul(x,x,n)==x]; Pr = projections(n)
print(len(E), "idempotents,", len(Pr), "projections")
cands = {
 "ep=p": lambda p,e: P.mul(e,p)==p,
 "pe*=p": lambda p,e: P.mul(p,P.star(e))==p,
 "e*pe=p": lambda p,e: P.prod(P.star(e),p,e)==p,
 "p(ee*)=p": lambda p,e: P.prod(p,e,P.star(e))==p,
 "(ee*)p=p": lambda p,e: P.prod(e,P.star(e),p)==p,
 "(e*e)p=p": lambda p,e: P.prod(P.star(e),e,p)==p,
 "p(e*e)=p": lambda p,e: P.prod(p,P.star(e),e)==p,
 "pe*p=p": lambda p,e: P.prod(p,P.star(e),p)==p,
 "e*p=pe*": lambda p,e: P.mul(P.star(e),p)==P.mul(p,P.star(e)),
 "ep=pe": lambda p,e: P.mul(e,p)==P.mul(p,e),
}
ok = {k: True for k in cands}
cnt=0
for p in Pr:
    for e in E:
        if P.mul(p,e)==p:
            cnt+=1
            for k,f in cands.items():
                if ok[k] and not f(p,e):
                    ok[k]=False
print(cnt, "pairs with pe=p")
for k,v in ok.items(): print(f"  pe=p => {k}: {v}")
