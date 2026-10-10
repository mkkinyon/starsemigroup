"""Backtracking evaluation of the labelled implications of conditions.in on a finite table T[i][j] = i*j."""
import re, sys, json, time
T = json.load(open(sys.argv[1])); n = len(T)
txt = open('/mnt/user-data/outputs/conditions.in').read()
body = '\n'.join(l.split('%')[0] for l in txt.split('\n'))
clauses = re.findall(r'([^\n#]*(?:\n[^\n#]*)*?)\s*#\s*label\("([^"]*)"\)', body)
def tokenize(s): return re.findall(r'[A-Za-z][A-Za-z0-9]*|->|!=|=|&|\*|\(|\)|\|', s)
def parse_term(tokens, i):
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
def atoms(toks):
    out = []; i = 0
    while i < len(toks):
        if toks[i] in ('&', '|'): i += 1; continue
        if toks[i] == '(':
            # could be a parenthesised term or grouping; try term parse
            try:
                lhs, j = parse_term(toks, i)
                if j < len(toks) and toks[j] in ('=', '!='):
                    rhs, j2 = parse_term(toks, j+1); out.append((lhs, toks[j], rhs)); i = j2; continue
            except Exception: pass
            i += 1; continue
        if toks[i] == ')': i += 1; continue
        lhs, j = parse_term(toks, i); op = toks[j]; rhs, j2 = parse_term(toks, j+1); out.append((lhs, op, rhs)); i = j2
    return out
def vars_of(t, acc):
    if t[0] == 'v': acc.add(t[1])
    else: vars_of(t[1], acc); vars_of(t[2], acc)
def ev(t, env):
    if t[0] == 'v': return env[t[1]]
    return T[ev(t[1], env)][ev(t[2], env)]
for text, label in clauses:
    if '->' not in text: continue
    toks = tokenize(text.replace('.', ' ')); k = toks.index('->')
    hyp = atoms(toks[:k]); con = atoms(toks[k+1:])
    V = []
    for a in hyp + con:
        s = set(); vars_of(a[0], s); vars_of(a[2], s)
        for v in sorted(s):
            if v not in V: V.append(v)
    # order variables greedily: each next variable completes as many hypothesis atoms as possible
    def avars(a):
        s = set(); vars_of(a[0], s); vars_of(a[2], s); return s
    order = []; remaining = list(V)
    while remaining:
        best = max(remaining, key=lambda v: sum(1 for a in hyp if avars(a) <= set(order + [v])))
        order.append(best); remaining.remove(best)
    checks = [[a for a in hyp if avars(a) <= set(order[:i+1]) and not avars(a) <= set(order[:i])] for i in range(len(order))]
    t0 = time.time(); viol = [None]; nodes = [0]
    def rec(i, env):
        if viol[0]: return
        if i == len(order):
            if not all((ev(l, env) == ev(r, env)) == (op == '=') for l, op, r in con): viol[0] = dict(env)
            return
        for val in range(n):
            env[order[i]] = val; nodes[0] += 1
            if all((ev(l, env) == ev(r, env)) == (op == '=') for l, op, r in checks[i]): rec(i+1, env)
        del env[order[i]]
    rec(0, {})
    print(f"{label:8} vars {len(V)}: {'VIOLATED '+str(viol[0]) if viol[0] else 'satisfied'} ({nodes[0]} nodes, {time.time()-t0:.0f}s)", flush=True)
