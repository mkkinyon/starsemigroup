import sys, time
exec(open('goal2.py').read().split("t = time.time()")[0])
G1 = ((-1, ('E', 'c')), (1, ('J', 'a', 'b')))
P = [('mt','a','c'), ('mt','c','b')]
conds = {
 "(R)": P + [('comm','x','a'), ('comm','x','c'), ('eq',('x','b'),('x','c'))],
 "(R)'=(W1)": P + [('comm','x','c'), ('comm','x','b'), idf('x')],
 "(R')": P + [('comm','x','c'), idf('x'), ('comm','y','a'), ('eq',('x','b'),('y','b'))],
 "(R'')": P + [('comm','x','c'), idf('x'), ('comm','y','b'), ('eq',('x','b'),('y','a'))],
 "(W2)": W2,
 "(R'_2)": P + [('comm','x','c'), idf('x'), ('comm','x','z'), idf('z'), ('comm','y','a'), ('eq',('z','b'),('y','b'))],
}
for name, H in conds.items():
    t = time.time(); print(f"m={m} {name}: G1 {holds(H, [], G1)}  G2 {holds(H, [], GOAL)} ({time.time()-t:.0f}s)", flush=True)
