import sys, time
exec(open('tind.py').read().split("Tyz = ")[0])
one = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','b')]
two = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y'), ('comm','y','b')]
three = two[:-1] + [('comm','y','z'), idf('z'), ('comm','z','b')]
for n, H, e in ((1, one, 'x'), (2, two, 'y'), (3, three, 'z')):
    L1 = meetst('abc', 'b' + e, 'b'); L2 = meetst('bc' + e, 'ac', 'c'); Tn = meetst('ab', 'bc' + e, 'bc')
    base = [('mt','a','c'), ('comm', e, 'b'), idf(e)]
    print(f"m={m} n={n}: L1 {holds4(H, [], L1)}  L2 {holds4(H, [], L2)};  base + L1 + L2 => T{n}: {holds4(base, [L1, L2], Tn)}", flush=True)
    if n == 2:
        for i, h in enumerate(H):
            HH = [x for j, x in enumerate(H) if j != i]
            print(f"   without {h}: L1 {holds4(HH, [], L1)}  L2 {holds4(HH, [], L2)}")
