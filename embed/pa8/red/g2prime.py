import sys
sys.argv = ['x', sys.argv[1], '4']
exec(open('inv4.py').read().split("if __name__ == '__main__':")[0])
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
base1 = [('mt','a','c'), ('comm','x','c'), idf('x')]
base2 = base1 + [('comm','x','y'), idf('y')]
base3 = base2 + [('comm','y','z'), idf('z')]
G2p = ((-1, ('J3',)), (-1, ('T','c','u')), (-1, ('T','c','v')), (1, ('J','c','x')))
G2pa = ((-1, ('J3',)), (-1, ('T','a','u')), (-1, ('T','a','v')), (1, ('J','a','x')))
for name, cl in (("G2'(x): two T(c) points in one class of avcvx are joined in cvx", G2p), ("G2'a: two T(a) points ... joined in avx", G2pa)):
    print(f"m={m} {name}: pos1 {run(base1, [], (cl, None))} pos2 {run(base2, [], (cl, {'x':'y'}))} pos3 {run(base3, [], (cl, {'x':'z'}))}", flush=True)
