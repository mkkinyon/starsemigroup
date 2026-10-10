"""Mace4 input: triangle hypotheses + cw != cz + the walk from a1 does not close within n turns."""
import sys
n=int(sys.argv[1])
def Phi(x):
    for p in ["b3","a2","b1","a3","b2","a1"]: x=f"({x} * {p})"
    return x
t=["a1"]
for i in range(n+1): t.append(Phi(t[-1]))
hyp=open("triangle.in").read()
body=hyp[hyp.index("formulas(assumptions)."):hyp.index("end_of_list.")]
body+="cw != cz.\n"
for i in range(n): body+=f"{t[i]} != {t[i+1]}.\n"
body+="end_of_list.\n"
print('op(400, infix, "*").\n'+body)
