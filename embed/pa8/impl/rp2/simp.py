import sys, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
base=[('mt','a','c'), ('mt','c','b')]
cands={
 'V1: c~x~z, x,z identify, z|><|b': base+[('comm','x','c'),('eq',('x','a'),('x','c')),('comm','x','z'),('eq',('z','a'),('z','c')),('mt','z','b')],
 'V2: c~x~z, z identifies, z|><|b': base+[('comm','x','c'),('comm','x','z'),('eq',('z','a'),('z','c')),('mt','z','b')],
 'V3: c~x~z, x identifies, z|><|b': base+[('comm','x','c'),('eq',('x','a'),('x','c')),('comm','x','z'),('mt','z','b')],
 'V4: c~z, z identifies, z|><|b': base+[('comm','z','c'),('eq',('z','a'),('z','c')),('mt','z','b')],
 'V5: z identifies, z|><|b, z<=k, x<=k ... skip': None,
}
for name,P in cands.items():
    if P is None: continue
    for m in (4,5):
        t=time.time(); r=valid(P,('mt','a','b'),m); print(f"{name}: m={m}: {r} ({time.time()-t:.0f}s)",flush=True)
        if not r: break
