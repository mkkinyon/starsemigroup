"""Multiplication table of the projection algebra of P_n (indices), matched relation."""
import sys, pickle, os
import numpy as np
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pmon import projections, mul
def build(n):
    f = f'tab{n}.pkl'
    if os.path.exists(f): return pickle.load(open(f, 'rb'))
    P = projections(n); idx = {p: i for i, p in enumerate(P)}; N = len(P)
    T = np.zeros((N, N), dtype=np.int16)   # T[p,q] = index of theta_q(p) = q p q
    for i, p in enumerate(P):
        for j, q in enumerate(P):
            T[i, j] = idx[mul(mul(q, p, n), q, n)]
    pickle.dump((P, T), open(f, 'wb'))
    return P, T
if __name__ == '__main__':
    P, T = build(int(sys.argv[1])); print(len(P))
