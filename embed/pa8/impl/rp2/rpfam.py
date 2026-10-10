"""Candidate family of (R'_n)-witnesses generalising M.K.'s order-10 model (n = 2).
Elements: a, c, b, x1..xn, k ; d, e0..en.  Binary table T[i][j] = theta_j(i)."""
import json, sys, itertools
def build(n):
    names=['a','c','b']+[f'x{i}' for i in range(1,n+1)]+['k','d']+[f'e{i}' for i in range(0,n+1)]
    I={s:i for i,s in enumerate(names)}; N=len(names)
    xs=[f'x{i}' for i in range(1,n+1)]; es=[f'e{i}' for i in range(0,n+1)]
    th={}  # th[(y,x)] = theta_x(y)
    for x in names: th[(x,x)]=x
    for y in names:
        if y!='a': th[(y,'a')]='a' if y=='c' else 'd'
        if y!='c': th[(y,'c')]='c' if y in ('a','b') else 'e0'
        if y!='b': th[(y,'b')]='b' if y in ('c','k',xs[-1]) else es[n]
        for i in range(1,n+1):
            xi=f'x{i}'
            if y==xi: continue
            if i<n:
                left=['a','c','d']+es[:i]+xs[:i-1]
                th[(y,xi)] = xi if y=='k' else (es[i-1] if y in left else es[i])
            else:
                th[(y,xi)] = xi if y in ('b','k') else es[n-1]
        if y!='k':
            th[(y,'k')] = {'a':'d','b':xs[-1],'c':'e0',es[n]:es[n-1]}.get(y, y)
        for e in ['d']+es:
            if y!=e: th[(y,e)]=e
    T=[[I[th[(names[i],names[j])]] for j in range(N)] for i in range(N)]
    return T,names
def check_axioms(T):
    n=len(T); bad=[]
    for x in range(n):
        if T[x][x]!=x: bad.append(('idem',x))
        for y in range(n):
            if T[T[y][x]][x]!=T[y][x]: bad.append(('ax2',x,y))
            if T[T[x][y]][x]!=T[y][x]: bad.append(('ax3',x,y))
            for z in range(n):
                if T[T[T[z][x]][y]][x]!=T[z][T[y][x]]: bad.append(('ax4',x,y,z))
                if T[T[T[T[z][x]][y]][x]][y]!=T[T[z][x]][y]: bad.append(('ax5',x,y,z))
                if T[z][x]==z and T[z][y]==z and T[x][y]!=T[y][x]: bad.append(('Q1',x,y,z))
    return bad
if __name__=='__main__':
    sys.path.insert(0,'/home/claude/pa8w/embed/pa8/wn'); from iso import iso
    for n in range(1,6):
        T,names=build(n); bad=check_axioms(T)
        print(f"n={n}: order {len(T)}, axiom violations: {len(bad)} {bad[:5]}")
        json.dump(T,open(f'R{n}_T.json','w')); json.dump({'T':T,'names':names},open(f'R{n}.json','w'))
    T2,_=build(2); M=json.load(open('mk10_T.json')); print('n=2 iso to MK model:', iso(T2,M))
