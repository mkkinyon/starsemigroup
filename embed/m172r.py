from qi import test_qi
import time, sys
tests = {
 'R: a|><|c, b|><|c, z<=c, aza=w=bzb, w|><|z => a=b': ('abczw', [('aca','a'),('cac','c'),('bcb','b'),('cbc','c'),('czc','z'),('aza','w'),('bzb','w'),('wzw','w'),('zwz','z')], ('a','b')),
 'R2: a|><|c, b|><|c, z<=c, aza=w=bzb => a=b': ('abczw', [('aca','a'),('cac','c'),('bcb','b'),('cbc','c'),('czc','z'),('aza','w'),('bzb','w')], ('a','b')),
 'R3: a|><|c, b|><|c, aza=bzb => a=b': ('abcz', [('aca','a'),('cac','c'),('bcb','b'),('cbc','c'),('aza','bzb')], ('a','b')),
}
n = int(sys.argv[1])
for name,(L,h,c) in tests.items():
    t=time.time(); r = test_qi(n, L, h, c)
    print(name, f'P_{n}:', 'FORCED' if r==[] else 'not forced: '+str(r[0]), f'({time.time()-t:.0f}s)', flush=True)
