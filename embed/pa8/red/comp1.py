"""Print the component of c in I(a,c) for one pair, plus the invariants. Usage: python3 comp1.py n 'a' 'c' ['y']"""
import sys, re
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
from collections import deque
def parse(s):
    blocks=[];T=0
    for m in re.finditer(r'([\[\(])([\d ]+)[\]\)]',s):
        b=sum(1<<int(t) for t in m.group(2).split());blocks.append(b)
        if m.group(1)=='[':T|=b
    return (tuple(sorted(blocks)),T)
n=int(sys.argv[1]); a=parse(sys.argv[2]); c=parse(sys.argv[3]); P=projections(n)
idf=[y for y in P if theta(y,a)==theta(y,c)]
dist={c:0};dq=deque([c])
while dq:
    u=dq.popleft()
    for v in idf:
        if v not in dist and commute(u,v): dist[v]=dist[u]+1;dq.append(v)
def delta(x): return len(join(x,a))-len(join(x,c))
print("matched:",matched(a,c),"|Id|=%d |Comp(c)|=%d delta(c)=%d"%(len(idf),len(dist),delta(c)))
for x in sorted(dist,key=lambda x:dist[x]): print(" d=%d %s"%(dist[x],show(x,n)))
if len(sys.argv)>4:
    y=parse(sys.argv[4]); print("y=%s in Id: %s, in Comp: %s, delta=%d"%(show(y,n),y in idf,y in dist,delta(y)))
