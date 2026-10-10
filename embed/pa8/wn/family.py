"""The chain family P_n (order 2n+5): top a, c, b, x1..xn; bottoms d, e0..en (rectangular band).
theta_e constant; theta_a: a,c -> a, else d; theta_c: a,b,c -> c, else e0; theta_b: b,c -> b, else en;
theta_{xi}: xi -> xi; 'left' elements (a, c, d, e0..e_{i-1}, x1..x_{i-1}) -> e_{i-1}; 'right' (e_i..e_n, x_{i+1}..x_n, b) -> e_i.
Table T[y][x] = theta_x(y) = y*x."""
import sys, json
def build(n):
    names = ['a','c','b'] + [f'x{i}' for i in range(1,n+1)] + ['d'] + [f'e{i}' for i in range(n+1)]
    idx = {s:i for i,s in enumerate(names)}; N = len(names)
    def th(x, y):   # theta_x(y)
        if x == y: return x
        if x == 'd' or x.startswith('e'): return x
        if x == 'a': return 'a' if y == 'c' else 'd'
        if x == 'c': return 'c' if y in ('a','b') else 'e0'
        if x == 'b': return 'b' if y == 'c' else f'e{n}'
        i = int(x[1:])
        left = {'a','c','d'} | {f'e{j}' for j in range(i)} | {f'x{j}' for j in range(1,i)}
        return f'e{i-1}' if y in left else f'e{i}'
    T = [[idx[th(x, y)] for x in names] for y in names]
    return T, names
if __name__ == '__main__':
    n = int(sys.argv[1]); T, names = build(n)
    json.dump(T, open(f'P{n}_T.json','w')); json.dump({'T':T,'consts':{s:i for i,s in enumerate(names)}}, open(f'P{n}.json','w'))
    print(n, len(T), names)
