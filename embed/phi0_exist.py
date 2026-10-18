import re, subprocess, sys
src=open('/home/claude/repo/starsemigroup/notes/conditions.in').read()
body=src[src.index('formulas(assumptions).'):src.index('end_of_list.')]
forms=re.findall(r'((?:(?!# label).)*?)# label\("([^"]*)"\)\.', body, re.S)
F={lab:'\n'.join(l for l in txt.strip().split('\n') if not l.strip().startswith('%')).strip() for txt,lab in forms}
hdr="""set(prolog_style_variables).
op(400, infix, "*").
assign(max_seconds, %d).
formulas(assumptions).
X*X = X.  (Y*X)*X = Y*X.  (X*Y)*X = Y*X.  ((Z*X)*Y)*X = Z*(Y*X).  (((Z*X)*Y)*X)*Y = (Z*X)*Y.
(Z*X = Z & Z*Y = Z) -> X*Y = Y*X.
e*X = X.  X*e = X.
c*a = a. a*c = c. c*b = b. b*c = c.
%s
end_of_list.
formulas(goals).
%s
end_of_list.
"""
def hyps(lab, consts):
    f=F[lab]
    # formula is (H) -> (concl); take H, replace variables by the given constants
    H=f[:f.rindex('->')].strip()
    assert H.startswith('(') and H.endswith(')'); H=H[1:-1]
    # variables in the condition
    vs=sorted(set(re.findall(r'\b[A-Z][A-Za-z0-9]*\b',H)))
    exist=[v for v in vs if v not in consts]
    for v in vs:
        if v in consts: H=re.sub(r'\b%s\b'%v, consts[v], H)
    g=H
    for v in exist: g='exists %s (%s)'%(v,g) if g.startswith('exists') else 'exists %s (%s)'%(v,g)
    return g+'.'
secs=int(sys.argv[1]) if len(sys.argv)>1 else 60
tests={'(Hm)':{'A':'a','B':'b','C':'c'},'(Hm\')':{'A':'a','B':'b','C':'c'},'(Ab)':{'A':'a','B':'b','C':'c'},
 '(W2)':{'A':'a','B':'b','C':'c'},'(W3)':{'A':'a','B':'b','C':'c'},"(A2')":{'A':'a','B':'b','C':'c'},
 '(K5)':{'A':'a','B':'b','C':'c'},'(K6)':{'A':'a','B':'b','C':'c'},"(R'2)":{'A':'a','B':'b','C':'c'},"(R'3)":{'A':'a','B':'b','C':'c'},
 '(A1)':{'A':'a','B':'b','C':'c'},'(A2)':{'A':'a','B':'b','C':'c'},'(P1)':{'P0':'a','P1':'c','P2':'b','P3':'d'},
 '(E1)':{'A':'a','B':'b','C':'c'},'(E6)':{'A':'a','B':'b','C':'c'}}
for lab,consts in tests.items():
    for half,name in (('b*a = a.','ab'),('a*b = b.','ba')):
        extra=half
        if lab=='(P1)': extra='d*c = c. c*d = d. '+half.replace('b','d')  # path a c b d: use Phi0 on a,c,d? skip
        if lab=='(P1)': continue
        g=hyps(lab,consts)
        inp=hdr%(secs,extra,g)
        fn='ex_%s_%s.in'%(re.sub(r'[^A-Za-z0-9]','_',lab),name); open(fn,'w').write(inp)
        r=subprocess.run(['/home/claude/bin/prover9','-f',fn],capture_output=True,text=True)
        st='PROVED' if 'THEOREM PROVED' in r.stdout else 'no proof'
        print(f'{lab:7s} Phi0-hyp theta_{name[0]}({name[1]})={name[0]}: {st}', flush=True)
