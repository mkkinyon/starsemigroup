"""Mace4 input for a (W_n)-but-not-(W_{n-1})... i.e. a projection algebra violating (W_n) along a chain
c ~ x1 ~ ... ~ xn ~ b with bottoms d = bottom(a), e0 = c^x1, e1 = x1^x2, ..., en = xn^b, satisfying (Q1), (Tri) and
the known conditions and (W_{n-1}).  Most of the table is fixed; Mace4 fills the rest at domain size 2n+5."""
import sys
n = int(sys.argv[1]); known = len(sys.argv) > 2 and sys.argv[2] == 'known'
xs = [f'x{i}' for i in range(1, n+1)]; es = [f'e{i}' for i in range(0, n+1)]
top = ['a', 'b', 'c'] + xs; bot = ['d'] + es; all_ = top + bot
L = []
L.append('set(prolog_style_variables). assign(max_seconds, 3600). assign(max_megs, 3000). op(400, infix, "*").')
L.append('formulas(assumptions).')
L += ['X*X = X.', '(Y*X)*X = Y*X.', '(X*Y)*X = Y*X.', '((Z*X)*Y)*X = Z*(Y*X).', '(((Z*X)*Y)*X)*Y = (Z*X)*Y.',
      '(Z*X = Z & Z*Y = Z) -> X*Y = Y*X.']
# W_{n-1} as an axiom (n-1 >= 1); and (W_1) etc. are implied
m = n - 1
V = [f'V{i}' for i in range(1, m+1)]
hyp = ['C*A = A', 'A*C = C', 'C*B = B', 'B*C = C', f'{V[0]}*C = C*{V[0]}', f'{V[-1]}*B = B*{V[-1]}'] + \
      [f'{V[i]}*{V[i+1]} = {V[i+1]}*{V[i]}' for i in range(m-1)] + [f'A*{v} = C*{v}' for v in V]
L.append(f"% (W_{m})\n(" + ' & '.join(hyp) + ') -> (B*A = A & A*B = B).')
if known:
    L.append('% (Tri)')
    L.append('(B1*B2 = Z & B2*B1 = Z & B2*B3 = Z & B3*B2 = Z & B3*B1 = Z & B1*B3 = Z & A1*B1 = B1*A1 & A2*B2 = B2*A2 & A3*B3 = B3*A3 & B2*A1 = A1 & A1*B2 = B2 & B3*A2 = A2 & A2*B3 = B3 & B1*A3 = A3 & A3*B1 = B1 & A1*A2 = W & A2*A1 = W & A2*A3 = W & A3*A2 = W & A3*A1 = W & A1*A3 = W) -> W = Z.')
    L.append('(C*A = A & A*C = C & C*B = B & B*C = C & D*B = B & B*D = D & C*D = D*C & (C*D)*A = (C*D)*B) -> (D*A = A & A*D = D).')
    L.append('(C*B = B & (T*A)*B = T*A & (T*C)*A = T*C) -> (T*A)*(T*B) = T*A.')
L.append('% fixed part of the table (X*Y = theta_Y(X))')
# bottoms: theta_e constant
for e in bot:
    for y in all_: L.append(f'{y}*{e} = {e}.')
# theta_a, theta_c, theta_b
for y in all_:
    L.append(f"{y}*a = {'a' if y in ('a','c') else 'd'}.")
    L.append(f"{y}*c = {'c' if y in ('a','b','c') else 'e0'}.")
    L.append(f"{y}*b = {'b' if y in ('b','c') else f'e{n}'}.")
# theta_{x_i}: value in {e_{i-1}, e_i} or x_i (free), with the forced ones
for i, x in enumerate(xs, start=1):
    lo, hi = f'e{i-1}', f'e{i}'
    for y in all_:
        if y == x: L.append(f'{x}*{x} = {x}.')
        elif y == lo or y == hi: L.append(f'{y}*{x} = {y}.')
        elif y == 'c' and i == 1: L.append(f'c*{x} = {lo}.')
        elif y == 'b' and i == n: L.append(f'b*{x} = {hi}.')
        elif y == (f'x{i-1}' if i > 1 else None): L.append(f'{y}*{x} = {lo}.')
        elif y == (f'x{i+1}' if i < n else None): L.append(f'{y}*{x} = {hi}.')
        else: L.append(f'{y}*{x} = {lo} | {y}*{x} = {hi} | {y}*{x} = {x}.')
    L.append(f'a*{x} = c*{x}.')
# distinct constants
for i in range(len(all_)):
    for j in range(i+1, len(all_)): L.append(f'{all_[i]} != {all_[j]}.')
L.append('end_of_list.')
open(f'wn_{n}{"_known" if known else ""}.in', 'w').write('\n'.join(L) + '\n')
print('elements', len(all_))
