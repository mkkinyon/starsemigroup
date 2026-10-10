import sys; sys.argv = ['x', '4']
exec(open('rp_min.py').read().split("for eq in EQS:")[0])
import time
for eq, S in [(('cy','cx'), {2,3,4,5,6}), (('ax','yac'), {2,3,4,5,6}), (('xab','xcb'), {2,3,4,5,6}), (('cy','cx'), {2,3,4,6}), (('cy','cx'), {2,3,5,6}), (('cy','cx'), {3,4,5,6}), (('cy','cx'), {2,4,5,6}), (('cy','cx'), {2,3,4,5})]:
    t0 = time.time(); print(eq, sorted(S), holds(eq, S), f"{time.time()-t0:.0f}s", flush=True)
