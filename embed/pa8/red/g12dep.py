import sys
exec(open('meets.py').read().split("L = 'abcy'")[0])
G1 = ((-1, ('E', 'c')), (1, ('J', 'a', 'b')))
G2 = ((-1, ('J3', 'a', 'b', 'c')), (-1, ('T','c','u')), (-1, ('T','c','v')), (1, ('E','c')))
for name, g in (('G1', G1), ('G2', G2)):
    print(f"m={m}: {name} under (W_2): {holds2(W2, [], g)}")
    for i, h in enumerate(W2):
        H = [x for j, x in enumerate(W2) if j != i]
        print(f"   {name} without {h}: {holds2(H, [], g)}")
