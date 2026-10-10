from qi import test_qi
import time, sys
M = [('aca','a'),('cac','c'),('bcb','b'),('cbc','c'),('bdb','b'),('dbd','d')]
tests = {
 'S: matchings + cdc=dcd + aza=bzb (z=cdc) => a|><|d': ('abcd', M + [('cdc','dcd'),('acdca','bcdcb')], ('ada','a')),
 'S2: matchings + cdc=dcd => a|><|d': ('abcd', M + [('cdc','dcd')], ('ada','a')),
 'S3: matchings + aza=bzb (z=cdc) => a|><|d': ('abcd', M + [('acdca','bcdcb')], ('ada','a')),
 'S4: matchings + cdc=dcd + aza=bzb (z=cdc) => dad=d': ('abcd', M + [('cdc','dcd'),('acdca','bcdcb')], ('dad','d')),
}
n = int(sys.argv[1])
for name,(L,h,c) in tests.items():
    t=time.time(); r = test_qi(n, L, h, c)
    print(name, f'P_{n}:', 'FORCED' if r==[] else 'not forced: '+str(r[0]), f'({time.time()-t:.0f}s)', flush=True)
