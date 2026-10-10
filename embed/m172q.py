from qi import test_qi
import time, sys
base = [('bcb','b'),('cbc','c'),('bdb','b'),('dbd','d'),('cdc','z'),('dcd','z'),('aca','a'),('cac','c')]
tests = {
 'Q1: base + aza=w, w|><|z => ada=a': ('abcdzw', base + [('aza','w'),('wzw','w'),('zwz','z')], ('ada','a')),
 'Q2: base + aza=w, w|><|z => ada=w': ('abcdzw', base + [('aza','w'),('wzw','w'),('zwz','z')], ('ada','w')),
 'Q3: base + aza=w, w|><|z, ada=w => a=b': ('abcdzw', base + [('aza','w'),('wzw','w'),('zwz','z'),('ada','w')], ('a','b')),
 'Q4: base + aza=w, bzb=w, w|><|z, ada=w => a=b': ('abcdzw', base + [('aza','w'),('bzb','w'),('wzw','w'),('zwz','z'),('ada','w')], ('a','b')),
 'Q5: base + aza=w, bzb=w, w|><|z, ada=w, dad=z => a=b': ('abcdzw', base + [('aza','w'),('bzb','w'),('wzw','w'),('zwz','z'),('ada','w'),('dad','z')], ('a','b')),
 'Q6: base + aza=w, bzb=w, w|><|z, ada=w, dad=z, aba=w => a=b': ('abcdzw', base + [('aza','w'),('bzb','w'),('wzw','w'),('zwz','z'),('ada','w'),('dad','z'),('aba','w'),('bab','w')], ('a','b')),
}
n = int(sys.argv[1])
for name,(L,h,c) in tests.items():
    t=time.time(); r = test_qi(n, L, h, c)
    print(name, f'P_{n}:', 'FORCED' if r==[] else 'not forced: '+str(r[0]), f'({time.time()-t:.0f}s)', flush=True)
