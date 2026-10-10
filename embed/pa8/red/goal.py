import sys
sys.argv = ['x', sys.argv[1], '4']
exec(open('inv4.py').read().split("if __name__ == '__main__':")[0])
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
base1 = [('mt','a','c'), ('comm','x','c'), idf('x')]
base2 = base1 + [('comm','x','y'), idf('y')]
base3 = base2 + [('comm','y','z'), idf('z')]
G_c = ((-1, ('J3',)), (-1, ('T','c','u')), (-1, ('T','c','v')), (1, ('E','c')))
G_a = ((-1, ('J3',)), (-1, ('T','a','u')), (-1, ('T','a','v')), (1, ('E','a')))
G_x = ((-1, ('J3',)), (-1, ('T','x','u')), (-1, ('T','x','v')), (1, ('E','x')))
for name, cl in (('G_c: no class of avcvx has two T(c)', G_c), ('G_a: ... two T(a)', G_a), ('G_x: ... two T(x)', G_x)):
    print(name, '| pos1:', run(base1, [], (cl, None)), '| pos2:', run(base2, [], (cl, {'x': 'y'})), '| pos3:', run(base3, [], (cl, {'x': 'z'})), flush=True)
