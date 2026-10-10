"""Check p9/conditions.in against the witness algebras with LADR clausefilter."""
import sys, os, json, pickle, subprocess, re
sys.path.insert(0, '/home/claude/pa8w'); sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from indep import violated_set
from pa_sat import M172
from fourth import table as P7table
W = [('P (order 6)', M172), ('P7', P7table())]
P9names = 'a b c d m n k w z'.split()
rows = '''a m a m m m m w w
m b b b m m m w w
c c c z n n z z z
k d z d k z k z z
m m m m m m m w w
n n n z n n z z z
k k z k k z k z z
w w w w w w w w w
z z z z z z z z z'''.split('\n')
thP9 = {p: dict(zip(P9names, r.split())) for p, r in zip(P9names, rows)}
W.append(('P9', [[P9names.index(thP9[q][p]) for q in P9names] for p in P9names]))
os.chdir('/mnt/user-data/outputs/starsemigroup/embed')
Tq, sq, A2 = pickle.load(open('hex_smallest.pkl', 'rb'))
from layered import proj_algebra
P, A = proj_algebra(list(range(len(Tq))), Tq, sq); W.append(('P(Q0)', A))
recs = [json.loads(l) for l in open('/home/claude/pa8w/post8.log')]
for k, A in enumerate([r["A"] for r in recs if r["embeds"] is None]): W.append((f'P8^{k+1}', A))
for k, A in enumerate(json.load(open('/home/claude/pa8w/cand9.json'))): W.append((f'cand9-{k}', A))
os.chdir('/home/claude/pa8w/p9')
env = dict(os.environ, PATH="/home/claude/bin:" + os.environ.get("PATH", ""))
src = open('conditions.in').read()
# clausefilter wants clauses/formulas only: strip set/op lines and list wrappers
body = "\n".join(l for l in src.splitlines() if not l.startswith(('set(', 'op(', 'formulas(', 'end_of_list', '%')))
body = 'op(400, infix, "*").\nset(prolog_style_variables).\nformulas(assumptions).\n' + body + "\nend_of_list.\n"
open('cond_body.in', 'w').write(body)
def interp(name, A):
    n = len(A)
    flat = [A[i][j] for i in range(n) for j in range(n)]
    return f"interpretation({n}, [number=1, seconds=0], [ function(*(_,_), [{','.join(map(str, flat))}]) ]).\n"
ok = True
for name, A in W:
    open('w.interp', 'w').write(interp(name, A))
    p = subprocess.run(['clausefilter', 'w.interp', 'false_in_all'], input=open('cond_lc2.in').read(), capture_output=True, text=True, env=env)
    labs = re.findall(r'label\("?([^")]*)"?\)', p.stdout)
    py = violated_set(A)
    print(f"{name:12s} order {len(A):2d}: clausefilter {labs}   python {py}", flush=True)
    if p.returncode not in (0, 1): print(p.stderr[-500:])
