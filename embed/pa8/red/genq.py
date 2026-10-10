import sys, time
sys.argv = ['x', sys.argv[1], '3']
exec(open('inv2.py').read().split("def clauses():")[0])
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
A_q = ((-1, ('E','c')), (1, ('J','a','x')))      # with x renamed to q
base = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','q')]
cases = {
 'q~x only': [],
 'q~x, q id': [idf('q')],
 'q~x, q|><|c': [('mt','q','c')],
 'q~x, c<=q': [('le','c','q')],
 'q~x, q<=c': [('le','q','c')],
 'q~x, q~c': [('comm','q','c')],
 'q~x, th_q(c)=th_q(a) weakened: th_c(q)=th_a(q)?': [('eq',('c','q'),('a','q'))],
 'q~x, q~a': [('comm','q','a')],
 'q~x, q|><|a': [('mt','q','a')],
}
for name, extra_h in cases.items():
    t = time.time(); r = run(base + extra_h, [], (A_q, {'x': 'q'})); print(f"m={m} eps_c <= eps_a v eps_q under [{name}]: {r} ({time.time()-t:.0f}s)", flush=True)
