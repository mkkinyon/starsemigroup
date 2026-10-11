"""The target statements under the real (W_2) hypotheses at m = 6: G1, G2, T2, L1', L2 (U2).  Usage: python3 m6targets.py m NAME"""
import sys, time
m_arg, which = sys.argv[1], sys.argv[2]; sys.argv = ['x', m_arg]
exec(open('tind.py').read().split("Tyz = ")[0])
G1 = ((-1, ('E', 'c')), (1, ('J', 'a', 'b')))
G2 = ((-1, ('J3', 'a', 'b', 'c')), (-1, ('T','c','u')), (-1, ('T','c','v')), (1, ('E','c')))
L1p = ((-1, ('E','y')), (-1, ('J3','a','b','c')), (1, ('E','b')))
T2 = meetst('ab', 'bcy', 'bc'); U2 = meetst('ac', 'bcy', 'c')
W2full = [('mt','a','c'), ('mt','c','b'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y'), ('comm','y','b')]
goal = {'G1': G1, 'G2': G2, 'L1p': L1p, 'T2': T2, 'U2': U2}[which]
t = time.time(); r = holds4(W2full, [], goal); print(f"m={m}: {which} under (W_2): {r} ({time.time()-t:.0f}s)", flush=True)
