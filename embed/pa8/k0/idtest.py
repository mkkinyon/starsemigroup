import sys
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n=4; P=projections(n)
f=tot=0; ex=None
f2=tot2=0
for a in P:
    for b in P:
        u=theta(a,b)
        for z in P:
            if theta(z,a)!=theta(z,b): continue
            tot+=1
            if theta(z,u)!=theta(z,a):
                f+=1
                if ex is None: ex=(a,b,z)
            if theta(b,z)==b:
                tot2+=1
                if theta(z,u)!=theta(z,a): f2+=1
print('th_z(a)=th_z(b) => th_z(aba)=th_z(a):', f, '/', tot, ex)
print('+ th_b(z)=b:', f2, '/', tot2)
