M=40
pts=[f'{l}{i}' for i in range(M) for l in 'pqrs']
def proj(T,N):
    blocks=[frozenset((p,s) for p in B for s in (0,1)) for B in T]
    for B in N:
        blocks.append(frozenset((p,0) for p in B)); blocks.append(frozenset((p,1) for p in B))
    cov=set(p for B in T+N for p in B); assert cov==set(pts), (set(pts)-cov, cov-set(pts))
    return frozenset(blocks)
R=range(M); R1=range(1,M); R2=range(2,M)
a=proj([['p0','s0'],['q0'],['r0']]+[[f'p{i}'] for i in R1]+[[f'r{i}'] for i in R1], [['q1']]+[[f's{i}',f'q{i+1}'] for i in range(1,M-1)]+[[f's{M-1}']])
b=proj([[f'q{i}'] for i in R]+[[f's{i}'] for i in R1], [['p0','s0']]+[[f'r{i}',f'p{i+1}'] for i in range(M-1)]+[[f'r{M-1}']])
c=proj([['q0'],['r0'],['s0','q1']]+[[f'r{i}'] for i in R1]+[[f'q{i}'] for i in R2], [['p0']]+[[f'p{i}',f's{i}'] for i in R1])
d=proj([[f'p{i}'] for i in R]+[[f's{i}'] for i in R1], [['q0','r0'],['s0','q1']]+[[f'r{i}',f'q{i+1}'] for i in range(1,M-1)]+[[f'r{M-1}']])
x=proj([], [['p0','s0'],['q0','r0'],['q1']]+[[f'p{i}',f'r{i}'] for i in R1]+[[f's{i}',f'q{i+1}'] for i in range(1,M-1)]+[[f's{M-1}']])
y=proj([[f'q{i}'] for i in R1]+[[f's{i}'] for i in R1], [['q0'],['p0','s0']]+[[f'r{i}',f'p{i+1}'] for i in range(M-1)]+[[f'r{M-1}']])
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
def far(bl): return any(int(p[1:])>=M-3 for (p,s) in bl)
def same(A,B): return not [bl for bl in A^B if not far(bl)]
print("a|><|c", same(th(a,c),a), same(th(c,a),c))
print("c|><|b", same(th(c,b),c), same(th(b,c),b))
print("b|><|d", same(th(b,d),b), same(th(d,b),d))
print("xa=ax", same(mult(x,a),mult(a,x)), " th_c(x)=th_d(x)", same(th(c,x),th(d,x)))
print("ya=ay", same(mult(y,a),mult(a,y)), " yb=by", same(mult(y,b),mult(b,y)), " th_y(c)=th_y(b)", same(th(y,c),th(y,b)))
print("conclusion a|><|d:", same(th(a,d),a), same(th(d,a),d))
