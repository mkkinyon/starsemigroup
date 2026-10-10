import json, itertools
T=json.load(open('mk10_T.json')); n=10; th=lambda p,q:T[p][q]
mt=lambda x,y: th(y,x)==x and th(x,y)==y
comm=lambda x,y: th(x,y)==th(y,x)
ident=lambda x,a,c: th(a,x)==th(c,x)
# (W_n): a|><|c|><|b, c~x1~...~xn~b, all x_i identify a with c => a|><|b
for N in (1,2,3,4):
    bad=0
    for a,c,b in itertools.product(range(n),repeat=3):
        if not(mt(a,c) and mt(c,b) and not mt(a,b)): continue
        for xs in itertools.product(range(n),repeat=N):
            ch=[c]+list(xs)+[b]
            if all(comm(ch[i],ch[i+1]) for i in range(N+1)) and all(ident(x,a,c) for x in xs): bad+=1
    print(f"(W{N}) violations: {bad}")
# hybrid (R'_n): c~x1~..~xn all identify, y~a, th_{xn}(b)=th_y(b)
for N in (1,2,3):
    bad=[]
    for a,c,b in itertools.product(range(n),repeat=3):
        if not(mt(a,c) and mt(c,b) and not mt(a,b)): continue
        for xs in itertools.product(range(n),repeat=N):
            ch=[c]+list(xs)
            if all(comm(ch[i],ch[i+1]) for i in range(N)) and all(ident(x,a,c) for x in xs):
                for y in range(n):
                    if comm(y,a) and th(b,xs[-1])==th(b,y): bad.append((a,c,b)+xs+(y,))
    print(f"(R'_{N}) violations: {len(bad)}", bad[:6])
