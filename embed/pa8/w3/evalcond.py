"""Evaluate the labelled clauses of conditions.in (binary notation, capitalised variables) in a finite table T[i][j] = i*j."""
import re, itertools, sys, json, time
T = json.load(open(sys.argv[1])); n = len(T)
txt = open('/mnt/user-data/outputs/conditions.in').read()
# clauses: text between a line start and '# label("...")', possibly multi-line; strip comments
body = '\n'.join(l.split('%')[0] for l in txt.split('\n'))
clauses = re.findall(r'([^\n#]*(?:\n[^\n#]*)*?)\s*#\s*label\("([^"]*)"\)', body)
def tokenize(s): return re.findall(r'[A-Za-z][A-Za-z0-9]*|->|!=|=|&|\*|\(|\)|\|', s)
def parse_term(tokens, i, env):
    # term := factor ('*' factor)*  with left assoc; factor := var | '(' term ')'
    def factor(i):
        if tokens[i] == '(':
            v, i = term(i+1); assert tokens[i] == ')'; return v, i+1
        return ('v', tokens[i]), i+1
    def term(i):
        v, i = factor(i)
        while i < len(tokens) and tokens[i] == '*':
            w, i = factor(i+1); v = ('*', v, w)
        return v, i
    return term(i)
def parse_formula(s):
    tokens = tokenize(s.replace('.', ' '))
    # split on '->'
    k = tokens.index('->')
    def atoms(toks):
        out = []; i = 0
        while i < len(toks):
            if toks[i] in ('(', ')') and (i == 0 or i == len(toks)-1): i += 1; continue
            if toks[i] in ('&', '|'): i += 1; continue
            lhs, i = parse_term(toks, i, None); op = toks[i]; rhs, i = parse_term(toks, i+1, None)
            out.append((lhs, op, rhs))
        return out
    hyp = atoms(tokens[:k]); con = atoms(tokens[k+1:])
    # strip enclosing parens of each side properly: re-parse
    return hyp, con
def ev(t, env):
    if t[0] == 'v': return env[t[1]]
    return T[ev(t[1], env)][ev(t[2], env)]
def vars_of(t, acc):
    if t[0] == 'v': acc.add(t[1])
    else: vars_of(t[1], acc); vars_of(t[2], acc)
for text, label in clauses:
    try: hyp, con = parse_formula(text)
    except Exception as e: print(label, 'parse error', e); continue
    V = set()
    for a in hyp + con: vars_of(a[0], V); vars_of(a[2], V)
    V = sorted(V); t0 = time.time(); viol = None; cnt = 0
    for vals in itertools.product(range(n), repeat=len(V)):
        env = dict(zip(V, vals))
        if all((ev(l, env) == ev(r, env)) == (op == '=') for l, op, r in hyp):
            if not all((ev(l, env) == ev(r, env)) == (op == '=') for l, op, r in con):
                viol = env; break
    print(f"{label:8} vars {len(V)}: {'VIOLATED '+str(viol) if viol else 'satisfied'} ({time.time()-t0:.0f}s)", flush=True)
