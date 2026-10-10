"""Violation matrix: which labelled conditions (conditions.in, plus W4) each known algebra violates."""
import sys, json, re, time
sys.path.insert(0,'/home/claude/pa8w/embed/pa8/w3')
# reuse the backtracking evaluator from evalcond2 by importing its functions
src=open('/home/claude/pa8w/embed/pa8/w3/evalcond2.py').read()
head=src.split("for text, label in clauses:")[0].replace("T = json.load(open(sys.argv[1])); n = len(T)","T=None; n=None")
exec(head)
extra=[("(C*A = A & A*C = C & C*B = B & B*C = C & X*C = C*X & X*Y = Y*X & Y*Z = Z*Y & Z*T = T*Z & T*B = B*T & A*X = C*X & A*Y = C*Y & A*Z = C*Z & A*T = C*T) -> (B*A = A & A*B = B)", "(W4)")]
conds=[(t,l) for t,l in clauses if '->' in t and l not in ('(Q1)',)]+extra
def violates(T, text):
    global n
    n=len(T)
    toks=tokenize(text.replace('.',' ')); k=toks.index('->'); hyp=atoms(toks[:k]); con=atoms(toks[k+1:])
    V=[]
    for a in hyp+con:
        s=set(); vars_of(a[0],s); vars_of(a[2],s)
        for v in sorted(s):
            if v not in V: V.append(v)
    def avars(a):
        s=set(); vars_of(a[0],s); vars_of(a[2],s); return s
    order=[]; remaining=list(V)
    while remaining:
        best=max(remaining,key=lambda v: sum(1 for a in hyp if avars(a)<=set(order+[v]))); order.append(best); remaining.remove(best)
    checks=[[a for a in hyp if avars(a)<=set(order[:i+1]) and not avars(a)<=set(order[:i])] for i in range(len(order))]
    def ev2(t,env):
        if t[0]=='v': return env[t[1]]
        return T[ev2(t[1],env)][ev2(t[2],env)]
    found=[False]
    def rec(i,env):
        if found[0]: return
        if i==len(order):
            if not all((ev2(l,env)==ev2(r,env))==(op=='=') for l,op,r in con): found[0]=True
            return
        for val in range(n):
            env[order[i]]=val
            if all((ev2(l,env)==ev2(r,env))==(op=='=') for l,op,r in checks[i]): rec(i+1,env)
        del env[order[i]]
    rec(0,{}); return found[0]
algs=json.load(open('algs.json')); labels=[l for _,l in conds]
M={}
for name,T in algs.items():
    M[name]={l: violates(T,t) for t,l in conds}
    print(f"{name:10} violates: {[l for l in labels if M[name][l]]}", flush=True)
json.dump({'labels':labels,'M':M},open('viol.json','w'))
