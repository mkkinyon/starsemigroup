import sys
sys.argv = ['x', sys.argv[1], '3']
exec(open('inv2.py').read().split("def clauses():")[0])
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
base1 = [('mt','a','c'), ('comm','x','c'), idf('x')]
base2 = base1 + [('comm','x','y'), idf('y')]
base3 = base2 + [('comm','y','z'), idf('z')]
ii = ((1, ('E','c')), (-1, ('J','a','c')), (-1, ('J','c','x')))
A = ((-1, ('E','c')), (1, ('J','a','x')))
for name, cl in (('(ii) (avc)^(cvx) = c', ii), ('Lemma A', A)):
    print(f"m={m} {name}: pos1 {run(base1, [], (cl, None))} pos2 {run(base2, [], (cl, {'x':'y'}))} pos3 {run(base3, [], (cl, {'x':'z'}))}", flush=True)
