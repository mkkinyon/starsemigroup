import json, sys
from pc_prover import AX, S_CL, atom_str
R_CL = """z1 * x1 != x1 | x1 * z1 != z1 | z1 * y1 != y1 | y1 * z1 != z1 | x1 * x != x * x1 | z1 * x != x * z1 | y1 * x != z1 * x | y1 * x1 = x1.
z1 * x1 != x1 | x1 * z1 != z1 | z1 * y1 != y1 | y1 * z1 != z1 | x1 * x != x * x1 | z1 * x != x * z1 | y1 * x != z1 * x | x1 * y1 = y1.
"""
n = int(sys.argv[1]); combos = json.load(open(sys.argv[2])); i = int(sys.argv[3]); mode = sys.argv[4] if len(sys.argv) > 4 else "SR"
combo = [tuple(a) for a in combos[i]]
hyps = "".join(f"a{k+1} * a{k} = a{k}. a{k} * a{k+1} = a{k+1}.\n" for k in range(n)) + "".join(atom_str(at) + "\n" for at in combo)
print(AX + (S_CL if "S" in mode else "") + (R_CL if "R" in mode else "") + hyps + f"a{n} * a0 != a0 | a0 * a{n} != a{n}.\nend_of_list.\n")
