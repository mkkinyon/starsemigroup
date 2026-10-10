import re, json, subprocess, sys, os
txt = open('/mnt/user-data/outputs/conditions.in').read()
body = '\n'.join(l.split('%')[0] for l in txt.split('\n'))
clauses = dict((l, t.strip().strip('.').strip()) for t, l in re.findall(r'([^\n#]*(?:\n[^\n#]*)*?)\s*#\s*label\("([^"]*)"\)', body))
clauses['(W4)'] = "(C*A = A & A*C = C & C*B = B & B*C = C & X*C = C*X & X*Y = Y*X & Y*Z = Z*Y & Z*T = T*Z & T*B = B*T & A*X = C*X & A*Y = C*Y & A*Z = C*Z & A*T = C*T) -> (B*A = A & A*B = B)"
AX = """X*X = X.
(Y*X)*X = Y*X.
(X*Y)*X = Y*X.
((Z*X)*Y)*X = Z*(Y*X).
(((Z*X)*Y)*X)*Y = (Z*X)*Y.
(Z*X = Z & Z*Y = Z) -> X*Y = Y*X."""
def ground(cl):
    hyp, con = cl.split('->'); V = sorted(set(re.findall(r'\b[A-Z][A-Za-z0-9]*\b', cl)))
    sub = {v: 'k' + v.lower() for v in V}
    f = lambda s: re.sub(r'\b[A-Z][A-Za-z0-9]*\b', lambda m: sub[m.group(0)], s)
    h = f(hyp).strip(); c = f(con).strip()
    if h.startswith('(') and h.endswith(')'): h = h[1:-1]
    if c.startswith('(') and c.endswith(')'): c = c[1:-1]
    return h, c
san = lambda z: re.sub(r'[^A-Za-z0-9]', '', z.replace("''", 'pp').replace("'", 'p'))
pairs = json.load(open('unsettled.json'))
known = [("(R')", "(R)"), ("(P2)", "(S)"), ("(Q)", "(S)"), ("(Q)", "(P2)"), ("(W3)", "(W2)"), ("(W4)", "(W3)"), ("(W4)", "(W2)")]
todo = [(X, Y) for X, Y in pairs if (X, Y) not in known]
for X, Y in todo:
    h, c = ground(clauses[Y]); neg = ' | '.join(e.strip().replace('=', '!=') for e in c.split('&'))
    base = f'set(prolog_style_variables).\nop(400, infix, "*").\nformulas(assumptions).\n{AX}\n{clauses[X]}.\n{h}.\n'
    tag = san(X) + '_' + san(Y)
    open(f'm_{tag}.in', 'w').write('assign(max_seconds, 300). assign(max_megs, 2500).\n' + base + neg + '.\nend_of_list.\n')
    open(f'p_{tag}.in', 'w').write('assign(max_seconds, 120).\n' + base + 'end_of_list.\nformulas(goals).\n' + c + '.\nend_of_list.\n')
print(len(todo), [f"{X}=>{Y}" for X, Y in todo])
