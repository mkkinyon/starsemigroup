"""Mace4 input for a chain model with n turns and the expected level structure:
walk x_{-1}=b2, x0=a1, x1=b3, x2=a2, x3=b1, x4=a3, x5, x6, ..., x_{6n}; closes at the bottom: x_{6n} -> x_{6n-5}.
Within each level consecutive pairs matched; descent steps x_{6m} -> x_{6m+1} only one-sided."""
import sys
n=int(sys.argv[1])
V=["a1","b3","a2","b1","a3","b2"]   # class of x_j is V[j mod 6]
def X(j):
    if j==-1: return "b2"
    if 0<=j<=4: return V[j]
    return f"e{j}"
hyp=open("triangle.in").read()
body=hyp[hyp.index("formulas(assumptions)."):hyp.index("end_of_list.")]
body+="cw != cz.\n% walk elements\n"
for j in range(5,6*n+1): body+=f"{X(j)} = {X(j-1)} * {V[j%6]}.\n"
body+="% descent steps and matched steps\n"
for j in range(-1,6*n):
    body+=f"{X(j)} * {X(j+1)} = {X(j+1)}.\n"
    if j%6!=0: body+=f"{X(j+1)} * {X(j)} = {X(j)}.\n"
body+=f"% bottom closes\n{X(6*n)} * {X(6*n-5)} = {X(6*n-5)}.\n"
body+="% chain strictly descending\n"
for m in range(n): body+=f"{X(6*m)} != {X(6*m+6)}.\n"
body+="end_of_list.\n"
print('op(400, infix, "*").\n'+body)
