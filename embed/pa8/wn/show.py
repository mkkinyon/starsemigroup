import json, sys, re
n=int(sys.argv[1]); d=json.load(open(f'wn{n}.json')); T=d['T']
# recover names from the .in order: mace4 assigns constants... consts dict empty (no function lines?) -> recover from structure
# names: constants are the first 2n+5 elements in the order they appear? Mace4 lists functions for constants; our parse missed them. Re-parse:
txt=open(f'wn_{n}_sv.out').read()
consts=dict((k,int(v)) for k,v in re.findall(r'function\((\w+), \[\s*(\d+)\s*\]\)', txt))
if not consts: consts=dict((k,int(v)) for k,v in re.findall(r'(\w+) = (\d+)', txt.split('interpretation')[1]) )
inv={v:k for k,v in consts.items()}
names=[inv.get(i,str(i)) for i in range(len(T))]
xs=[f'x{i}' for i in range(1,n+1)]
for x in xs:
    col=consts[x]
    print(f"theta_{x}: " + ', '.join(f"{names[y]}->{names[T[y][col]]}" for y in range(len(T)) if names[y] not in (x,)))
