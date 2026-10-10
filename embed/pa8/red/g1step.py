import sys, time
exec(open('goal2.py').read().split("t = time.time()")[0])
A_y = ((-1, ('E','c')), (1, ('J','a','y')))
M_y = ((1, ('E','c')), (-1, ('J','a','c')), (-1, ('J','c','y')))
G1 = ((-1, ('E', 'c')), (1, ('J', 'a', 'b')))
t = time.time()
print(f"m={m}: weak + A(y) + M(y) => G1: {holds(weak, [A_y, M_y], G1)} ({time.time()-t:.0f}s)")
print(f"m={m}: weak + A(y) => G1: {holds(weak, [A_y], G1)};  weak + M(y) => G1: {holds(weak, [M_y], G1)}")
print(f"m={m}: weak + A(y) + M(y) => GOAL: {holds(weak, [A_y, M_y], GOAL)}")
# which parts of 'weak' are needed?  drop y~b / b|><|c / y id
for drop in range(len(weak)):
    H = [h for i, h in enumerate(weak) if i != drop]
    print(f"   without {weak[drop]}: A+M => G1: {holds(H, [A_y, M_y], G1)}")
