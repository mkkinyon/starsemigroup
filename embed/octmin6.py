import sys, time
sys.argv = ["x", "6"]
src = open("octmin.py").read()
src = src[:src.index("cons = full_constraints()")]
exec(src)
cons = full_constraints()
t = time.time()
r = realizable(cons, limit=3000)
print("P_6 full relaxed octagon realizable:", r, f"({time.time()-t:.0f}s)", flush=True)
sub = [c for c in cons if not (c[0] == "C" and c[1][0] == "a" and c[2][0] == "a" and (c[1], c[2]) != ("a2", "a4"))]
t = time.time()
r = realizable(sub, limit=3000)
print("P_6 18-constraint sub-configuration realizable:", r, f"({time.time()-t:.0f}s)", flush=True)
