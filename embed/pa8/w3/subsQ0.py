import sys, json, time, itertools
sys.path.insert(0,'/home/claude/pa8w/embed')
from pa_sat import solve
T=json.load(open('model11b.json')); n=11
st=lambda x,y: T[x][y]
def closure(S):
    S=set(S)
    while True:
        new={st(x,y) for x in S for y in S}|S
        if new==S: return frozenset(S)
        S=new
subs={closure(S) for k in range(1,n) for S in itertools.combinations(range(n),k)}
subs={S for S in subs if len(S)<n}
maxsubs=[S for S in subs if not any(S<S2 for S2 in subs)]
print('maximal proper subalgebras:', [sorted(S) for S in maxsubs], flush=True)
for S in maxsubs:
    S=sorted(S); idx={x:i for i,x in enumerate(S)}; Ts=[[idx[T[x][y]] for y in S] for x in S]
    for m in (4,5,6,7):
        t=time.time(); r=solve(Ts, m, distinct=True, verbose=False)
        print(f"sub {S}: m={m} {'EMBEDS' if r else 'no'} ({time.time()-t:.0f}s)", flush=True)
        if r: break
