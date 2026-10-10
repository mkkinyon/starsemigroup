import sys, pickle, random
sys.path.insert(0,'/home/claude/pa8w/embed')
from pmon import mul
n=int(sys.argv[1]); inst=pickle.load(open(sys.argv[2],'rb')); memo={}
def m(p,q):
    k=(p,q)
    if k not in memo: memo[k]=mul(p,q,n)
    return memo[k]
th=lambda p,q: m(m(p,q),p)
tests={'r<=v': lambda a,c,b,x,y: m(th(x,b),m(x,c))==th(x,b),
       'v<=y': lambda a,c,b,x,y: m(m(x,c),y)==m(x,c),
       'r=v': lambda a,c,b,x,y: th(x,b)==m(x,c),
       'cy=yc': lambda a,c,b,x,y: m(c,y)==m(y,c),
       'ay=ya': lambda a,c,b,x,y: m(a,y)==m(y,a),
       'w=bxb': lambda a,c,b,x,y: m(y,b)==th(b,x),
       'th_a(x)=th_a(y)': lambda a,c,b,x,y: th(a,x)==th(a,y),
       'th_c(y)=v': lambda a,c,b,x,y: th(c,y)==m(x,c),
       'th_c(y)=th_c(x)': lambda a,c,b,x,y: th(c,y)==th(c,x),
       'th_b(y)=th_b(x)': lambda a,c,b,x,y: th(b,y)==th(b,x),
       'x<=y': lambda a,c,b,x,y: m(x,y)==x,
       'r<=w': lambda a,c,b,x,y: m(th(x,b),m(y,b))==th(x,b),
       'th_y(x)=r': lambda a,c,b,x,y: th(y,x)==th(x,b),
       'th_x(y)=r': lambda a,c,b,x,y: th(x,y)==th(x,b),
       'th_y(v)=r': lambda a,c,b,x,y: th(y,m(x,c))==th(x,b),
       'th_x(w)=r': lambda a,c,b,x,y: th(x,m(y,b))==th(x,b),
       'xw=wx': lambda a,c,b,x,y: m(x,m(y,b))==m(m(y,b),x),
       'yv=vy': lambda a,c,b,x,y: m(y,m(x,c))==m(m(x,c),y),
       'w<=x': lambda a,c,b,x,y: m(m(y,b),x)==m(y,b),
       'v<=w?': lambda a,c,b,x,y: m(m(x,c),m(y,b))==m(x,c),
}
S = inst if len(sys.argv)<4 else random.sample(inst,int(sys.argv[3]))
fails={k:0 for k in tests}
for I in S:
    for k,f in tests.items():
        if not f(*I): fails[k]+=1
for k,v in fails.items(): print(f"{k:20} fails {v}")
