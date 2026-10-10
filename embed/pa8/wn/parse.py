import re, sys, json
txt = open(sys.argv[1]).read()
m = re.search(r'interpretation\(\s*(\d+).*?function\(\*\(_,_\), \[(.*?)\]\)', txt, re.S)
n = int(m.group(1)); vals = [int(t) for t in m.group(2).replace('\n', ' ').split(',')]
T = [vals[n*i:n*i+n] for i in range(n)]
consts = dict(re.findall(r'function\((\w+), \[\s*(\d+)\]\)', txt))
json.dump({'T': T, 'consts': {k: int(v) for k, v in consts.items()}}, open(sys.argv[2], 'w'))
print(n, consts)
