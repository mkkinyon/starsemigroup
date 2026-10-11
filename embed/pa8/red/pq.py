import sys, time
exec(open('tind.py').read().split("Tyz = ")[0])
Q2 = meetst('cy', 'ab', 'bc'); P2 = meetst('acy', 'bcy', 'cy'); T2 = meetst('ab', 'bcy', 'bc')
Q1 = meetst('cx', 'ab', 'bc'); P1 = meetst('acx', 'bcx', 'cx'); T1 = meetst('ab', 'bcx', 'bc')
one = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','b')]
two = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y'), ('comm','y','b')]
print(f"m={m}: one link: P1 {holds4(one, [], P1)}  Q1 {holds4(one, [], Q1)};  base(a|><|c, x~b)+P1+Q1 => T1: {holds4([('mt','a','c'), ('comm','x','b')], [P1, Q1], T1)}")
print(f"m={m}: two links: P2 {holds4(two, [], P2)}  Q2 {holds4(two, [], Q2)};  base(a|><|c, y~b)+P2+Q2 => T2: {holds4([('mt','a','c'), ('comm','y','b')], [P2, Q2], T2)}")
# which hypotheses does Q1 / Q2 need?
for name, H, g in (("Q1", one, Q1), ("Q2", two, Q2), ("P2", two, P2)):
    for i, h in enumerate(H):
        HH = [x for j, x in enumerate(H) if j != i]
        print(f"   {name} without {h}: {holds4(HH, [], g)}")
