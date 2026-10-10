"""For each labelled condition in conditions.in, ask Mace4 (domain fixed to the given table) for a violating assignment."""
import re, json, subprocess, sys
T = json.load(open(sys.argv[1])); n = len(T)
txt = open('/mnt/user-data/outputs/conditions.in').read()
body = '\n'.join(l.split('%')[0] for l in txt.split('\n'))
clauses = re.findall(r'([^\n#]*(?:\n[^\n#]*)*?)\s*#\s*label\("([^"]*)"\)', body)
table = '\n'.join(f"{i}*{j} = {T[i][j]}." for i in range(n) for j in range(n))
for text, label in clauses:
    if '->' not in text: continue
    text = text.strip().rstrip('.')
    hyp, con = text.split('->')
    V = sorted(set(re.findall(r'\b[A-Z][A-Za-z0-9]*\b', text)))
    sub = {v: 'k' + v.lower() for v in V}
    def inst(s):
        return re.sub(r'\b[A-Z][A-Za-z0-9]*\b', lambda m: sub[m.group(0)], s)
    h = inst(hyp).strip().strip('()') if False else inst(hyp).strip()
    c = inst(con).strip()
    # negate conclusion: con is a conjunction of equations possibly in parens
    c_in = c.strip(); 
    if c_in.startswith('(') and c_in.endswith(')'): c_in = c_in[1:-1]
    neg = ' | '.join(e.strip().replace('=', '!=') for e in c_in.split('&'))
    inp = f"""set(prolog_style_variables). assign(max_seconds, 300). set(arithmetic).
op(400, infix, "*").
formulas(assumptions).
{table}
{h}.
{neg}.
end_of_list.
"""
    inp = inp.replace('set(arithmetic).', '')
    open(f'chk_{re.sub(r"[^A-Za-z0-9]","",label)}.in', 'w').write(inp)
    r = subprocess.run(['/home/claude/bin/mace4', '-n', str(n), '-N', str(n), '-m', '1'], input=inp, capture_output=True, text=True, timeout=600)
    out = r.stdout
    status = 'VIOLATED' if 'interpretation(' in out else ('satisfied' if 'exhausted' in out else 'unknown: ' + out[-300:])
    assign = ''
    if 'VIOLATED' in status:
        assign = ', '.join(f"{m.group(1)}={m.group(2)}" for m in re.finditer(r'function\((k\w+), \[ *(\d+)\]', out))
    print(f"{label:8} {status} {assign}", flush=True)
