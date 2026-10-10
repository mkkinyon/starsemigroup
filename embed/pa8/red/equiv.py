import sys, time
exec(open('goal2.py').read().split("t = time.time()")[0])
G1 = ((-1, ('E', 'c')), (1, ('J', 'a', 'b')))
tri = [('mt','a','c'), ('mt','c','b'), ('mt','a','b')]
print(f"m={m}: a|><|c|><|b, a|><|b => G1: {holds(tri, [], G1)};  => G2: {holds(tri, [], GOAL)}")
# and the closing lemma itself (sanity): weak path + G1 + G2 => a|><|b, with NO y at all
path = [('mt','a','c'), ('mt','c','b')]
print(f"m={m}: a|><|c|><|b + G1 + G2 => a|><|b: {valid_mt(path, [G1, GOAL])}")
