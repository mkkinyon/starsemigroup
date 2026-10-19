"""Independent check of H_infinity (Remark rem:hinf) as defined in the paper.
Elements: ('W',), ('Z',), ('m',i), ('e',i,n), ('f',i,n).  th(y,x) = theta_y(x).
Levels are checked up to L; by the gap-compression argument a quasi-identity with k chain-valued
variables and term depth d holds in H_inf iff it holds on levels <= (k-1)(2d+1)."""
import itertools, sys
MATCH={(1,2),(2,1),(2,3),(3,2),(3,1)}   # (e-index, f-index), matched level by level; (1,3) shifted
def th(y,x):
    """theta_y(x)"""
    if y[0] in 'WZm': return y
    if x[0] in 'WZm':
        ky,i=y[0],y[1]
        if ky=='e':
            if x[0]=='W': return x
            if x[0]=='Z': return ('m',i)
            return x if x[1]==i else ('W',)
        else:
            if x[0]=='Z': return x
            if x[0]=='W': return ('m',i)
            return x if x[1]==i else ('Z',)
    ky,i,m=y; kx,j,n=x
    if ky==kx:
        if i==j: return (ky,i,max(m,n))
        return ('W',) if ky=='e' else ('Z',)
    if i==j: return ('m',i)
    if ky=='f':   # theta_{f_{i,m}}(e_{j,n})
        if (j,i) in MATCH: return ('f',i,max(m,n))
        assert (j,i)==(1,3); return ('f',3,max(m,n-1))
    else:         # theta_{e_{i,m}}(f_{j,n})
        if (i,j) in MATCH: return ('e',i,max(m,n))
        assert (i,j)==(1,3); return ('e',1,max(m,n+1))
def elems(L):
    return [('W',),('Z',)]+[('m',i) for i in (1,2,3)]+[(k,i,n) for n in range(L+1) for k in 'ef' for i in (1,2,3)]
def axioms(L):
    E=elems(L); bad=0
    for p in E:
        assert th(p,p)==p
        for q in E:
            pq=th(p,q)
            if th(p,pq)!=pq: bad+=1; print('PA2',p,q)
            if th(p,th(q,p))!=pq: bad+=1; print('PA3',p,q)
            # (PC): th(p,r)=r=th(q,r) -> th(p,q)=th(q,p)
            for r in E:
                if th(p,r)==r and th(q,r)==r and th(p,q)!=th(q,p): bad+=1; print('PC',p,q,r)
                # theta_p theta_q theta_p = theta_{theta_p(q)}
                if th(p,th(q,th(p,r)))!=th(pq,r): bad+=1; print('PA4',p,q,r)
                # theta_q theta_p theta_q theta_p = theta_q theta_p
                if th(q,th(p,th(q,th(p,r))))!=th(q,th(p,r)): bad+=1; print('PA5',p,q,r)
    return bad
def matched(p,q): return th(p,q)==p and th(q,p)==q
def comm(p,q): return th(p,q)==th(q,p)
def hexagon(L):
    """search hexagon configurations (H1)-(H3), E = all six pairs, with w != z"""
    E=elems(L); found=[]
    # a1 |><| b2, b3 ; a2 |><| b1, b3 ; a3 |><| b1, b2
    M={p:[q for q in E if matched(p,q)] for p in E}
    for a1 in E:
        for b2 in M[a1]:
            for b3 in M[a1]:
                if not comm(b2,b3): continue
                z=th(b2,b3)
                for a2 in M[b3]:
                    if not comm(a1,a2): continue
                    w=th(a1,a2)
                    for b1 in M[a2]:
                        if not (comm(b1,b2) and comm(b1,b3) and th(b1,b2)==z and th(b1,b3)==z): continue
                        if not comm(a2,b2): continue
                        for a3 in M[b1]:
                            if not (matched(a3,b2) and comm(a1,a3) and comm(a2,a3) and th(a1,a3)==w and th(a2,a3)==w): continue
                            if comm(a1,b1) and comm(a3,b3) and w!=z: found.append((a1,a2,a3,b1,b2,b3,w,z))
    return found
def triangle(L):
    E=elems(L); found=[]
    M={p:[q for q in E if matched(p,q)] for p in E}
    for a1 in E:
        for b2 in M[a1]:
            for a3 in M[b2] if False else E:
                pass
    # direct: the paper's instance
    a=[('e',1,0),('e',2,0),('e',3,0)]; b=[('f',1,0),('f',2,0),('f',3,0)]
    ok = matched(a[0],b[1]) and matched(a[1],b[2]) and matched(a[2],b[0])
    ok = ok and all(comm(a[i],a[j]) for i in range(3) for j in range(3)) and all(comm(b[i],b[j]) for i in range(3) for j in range(3))
    ok = ok and all(comm(a[i],b[i]) for i in range(3))
    w=th(a[0],a[1]); z=th(b[0],b[1])
    ok = ok and th(a[1],a[2])==w and th(a[0],a[2])==w and th(b[1],b[2])==z and th(b[0],b[2])==z
    return ok, w, z
if __name__=='__main__':
    L=int(sys.argv[1])
    print('axioms+PC violations at L=%d:'%L, axioms(L))
    print('triangle instance OK, w, z:', triangle(L))
    Lh=int(sys.argv[2]) if len(sys.argv)>2 else 6
    print('hexagon configs with w!=z at L=%d:'%Lh, hexagon(Lh)[:3])
