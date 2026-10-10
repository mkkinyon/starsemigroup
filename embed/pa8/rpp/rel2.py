import sys, pickle, random
sys.path.insert(0,'/home/claude/pa8w/embed')
from pmon import mul
n=int(sys.argv[1]); inst=pickle.load(open(sys.argv[2],'rb')); memo={}
def m(p,q):
    k=(p,q)
    if k not in memo: memo[k]=mul(p,q,n)
    return memo[k]
th=lambda p,q: m(m(p,q),p)
tests={'wc=cw': lambda a,c,b,x,y: m(m(y,b),c)==m(c,m(y,b)),
       'waw=w': lambda a,c,b,x,y: th(m(y,b),a)==m(y,b),
       'wa=aw': lambda a,c,b,x,y: m(m(y,b),a)==m(a,m(y,b)),
       'vb=bv': lambda a,c,b,x,y: m(m(x,c),b)==m(b,m(x,c)),
       'va=av': lambda a,c,b,x,y: m(m(x,c),a)==m(a,m(x,c)),
       'ra=ar': lambda a,c,b,x,y: m(th(x,b),a)==m(a,th(x,b)),
       'rb=br': lambda a,c,b,x,y: m(th(x,b),b)==m(b,th(x,b)),
       'rc=cr': lambda a,c,b,x,y: m(th(x,b),c)==m(c,th(x,b)),
       'th_r(a)=th_r(c)': lambda a,c,b,x,y: th(th(x,b),a)==th(th(x,b),c),
       'th_r(b)=th_r(c)': lambda a,c,b,x,y: th(th(x,b),b)==th(th(x,b),c),
       'th_w(c)=w': lambda a,c,b,x,y: th(m(y,b),c)==m(y,b),
       'th_v(b)=v': lambda a,c,b,x,y: th(m(x,c),b)==m(x,c),
       'th_v(a)=v': lambda a,c,b,x,y: th(m(x,c),a)==m(x,c),
       'v~w': lambda a,c,b,x,y: th(m(x,c),m(y,b))==m(x,c) and th(m(y,b),m(x,c))==m(y,b),
       'th_w(v)=w': lambda a,c,b,x,y: th(m(y,b),m(x,c))==m(y,b),
       'th_v(w)=v': lambda a,c,b,x,y: th(m(x,c),m(y,b))==m(x,c),
       'ax=ay': lambda a,c,b,x,y: m(a,x)==m(a,y),
       'xa=ya': lambda a,c,b,x,y: m(x,a)==m(y,a),
       'xb=yb': lambda a,c,b,x,y: m(x,b)==m(y,b),
       'cx=cy': lambda a,c,b,x,y: m(c,x)==m(c,y),
}
S = inst if len(sys.argv)<4 else random.sample(inst,int(sys.argv[3]))
fails={k:0 for k in tests}
for I in S:
    for k,f in tests.items():
        if not f(*I): fails[k]+=1
for k,v in fails.items(): print(f"{k:20} fails {v}")
