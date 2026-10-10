import json, sys, os
sys.path.insert(0,'/home/claude/pa8w/embed/pa8/wn'); sys.path.insert(0,'/home/claude/pa8w/n4')
from iso import iso
E='/home/claude/pa8w/embed/pa8/'
P8=[json.loads(l)['A'] for l in open(E+'post8.log') if json.loads(l).get('embeds') is None]
R1=json.load(open('R1_T.json'))
for k,A in enumerate(P8,1):
    if iso(A,R1): print('R1 iso P8:',k)
algs=json.load(open('/home/claude/pa8w/embed/pa8/impl/algs.json'))
items = algs.items() if isinstance(algs,dict) else enumerate(algs)
for name,A in items:
    A = A['T'] if isinstance(A,dict) and 'T' in A else A
    if len(A)==8 and iso(A,R1): print('R1 iso known',name)
print('done')
