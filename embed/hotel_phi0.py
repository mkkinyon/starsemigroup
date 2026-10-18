# Hilbert-hotel example: a |><| c |><| b, aba = a, bab != b, on points y, x_i, z_i, w_i (i < M), window check.
M=30
pts=['y']+[f'{l}{i}' for i in range(M) for l in 'xzw']
def proj(T,N):
    blocks=[frozenset((p,s) for p in B for s in (0,1)) for B in T]
    for B in N:
        blocks.append(frozenset((p,0) for p in B)); blocks.append(frozenset((p,1) for p in B))
    allp=set(p for B in T+N for p in B); assert allp==set(pts), set(pts)-allp
    return frozenset(blocks)
A=[['y','x0','z0']]+[[f'x{i}',f'z{i}'] for i in range(1,M)]
a=proj(A,[[f'w{i}'] for i in range(M)])
B=[['y','w0']]+[[f'x{i-1}',f'w{i}'] for i in range(1,M)]
b=proj(B,[[f'z{i}'] for i in range(M)]+[[f'x{M-1}']])   # x_{M-1} dangling at the window end
C=[[f'z{i}',f'w{i}'] for i in range(M)]
c=proj(C,[['y']]+[[f'x{i}'] for i in range(M)])
def mult(Pa,Pb):
    par={}
    def f(x):
        while par.setdefault(x,x)!=x: x=par[x]
        return x
    def u(p,q): par[f(p)]=f(q)
    for bl in Pa:
        l=[('u',p) if s==0 else ('m',p) for (p,s) in bl]
        for q in l[1:]: u(l[0],q)
    for bl in Pb:
        l=[('m',p) if s==0 else ('l',p) for (p,s) in bl]
        for q in l[1:]: u(l[0],q)
    cls={}
    for p in pts:
        cls.setdefault(f(('u',p)),set()).add((p,0)); cls.setdefault(f(('l',p)),set()).add((p,1))
    return frozenset(frozenset(v) for v in cls.values())
def th(p,q): return mult(mult(p,q),p)
def far(bl): return any(p[0] in 'xzw' and int(p[1:])>=M-2 for (p,s) in bl)
def diff(P,Q): return [bl for bl in P^Q if not far(bl)]
print("aca=a away from end:", diff(th(a,c),a)); print("cac=c:", diff(th(c,a),c))
print("cbc=c:", diff(th(c,b),c)); print("bcb=b:", diff(th(b,c),b))
print("aba=a:", diff(th(a,b),a))
v=th(b,a); print("bab vs b, differing blocks near start:", sorted(sorted(bl) for bl in diff(v,b))[:4])
