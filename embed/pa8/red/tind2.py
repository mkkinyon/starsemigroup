import sys, time
exec(open('tind.py').read().split("tests = {")[0])
# extra elements: w = theta_y(b), v = y z (= theta_y(z)), r = theta_y(theta_z(b))?
step2 = step + [('eq', ('y','b'), 'w'), ('eq', ('y','z'), 'v')]
Tyw = meetst('aw', 'cyw', 'cw'); Tyv = meetst('av', 'cyv', 'cv')
A_w = ((-1, ('E','c')), (1, ('J','a','w')))
tests = {
 "T(y;z), T(y;w), T(y;v) => T(z;b)": [Tyz, Tyw, Tyv],
 "T(y;z), T(y;w), T(y;v) + A(y),A(z),M(y),M(z) => T(z;b)": [Tyz, Tyw, Tyv, A_y, A_z, M_y, M_z],
 "T(y;w) alone => T(z;b)": [Tyw],
}
for name, hy in tests.items():
    t = time.time(); print(f"m={m}: {name}: {holds4(step2, hy, Tzb)} ({time.time()-t:.0f}s)", flush=True)
