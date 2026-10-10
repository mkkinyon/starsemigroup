import sys
sys.argv = ['x', sys.argv[1], '4']
exec(open('inv4.py').read().split("if __name__ == '__main__':")[0])
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
base1 = [('mt','a','c'), ('comm','x','c'), idf('x')]
base2 = base1 + [('comm','x','y'), idf('y')]
base3 = base2 + [('comm','y','z'), idf('z')]
C = {
 "N(x)-block, two supp-a points => joined in avc": ((-1,('E','x')), (1,('T','x','u')), (1,('J','a','c')), (-1,('T','a','u')), (-1,('T','a','v'))),
 "N(x)-block, supp-a point u, any v => joined in avc": ((-1,('E','x')), (1,('T','x','u')), (1,('J','a','c')), (-1,('T','a','u'))),
 "N(x)-block, two supp-a points => joined in cvx": ((-1,('E','x')), (1,('T','x','u')), (1,('J','c','x')), (-1,('T','a','u')), (-1,('T','a','v'))),
 "N(x)-block, two supp-a points, not in supp c => joined in avc": ((-1,('E','x')), (1,('T','x','u')), (1,('J','a','c')), (-1,('T','a','u')), (-1,('T','a','v')), (1,('T','c','u'))),
 "N(x)-block, supp-a point u not in supp c, v not in supp c => E(c)": ((-1,('E','x')), (1,('T','x','u')), (1,('E','c')), (-1,('T','a','u')), (1,('T','c','u')), (1,('T','c','v'))),
 "N(x)-block, u in supp a \\ supp c => v in same a-block or joined avc": ((-1,('E','x')), (1,('T','x','u')), (1,('J','a','c')), (-1,('T','a','u')), (1,('T','c','u'))),
}
for name, cl in C.items():
    print(f"m={m} [{name}]: pos1 {run(base1, [], (cl, None))} pos2 {run(base2, [], (cl, {'x':'y'}))} pos3 {run(base3, [], (cl, {'x':'z'}))}", flush=True)
