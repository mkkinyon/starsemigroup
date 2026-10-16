import sys, time
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n=4; P=projections(n)
# (i) a<=y, th_y(z)=a => th_z(y)=th_z(a)
f1=0; tot1=0; ex=None
for y in P:
    for a in P:
        if theta(y,a)!=a: continue
        for z in P:
            if theta(y,z)!=a: continue
            tot1+=1
            if theta(z,y)!=theta(z,a):
                f1+=1
                if ex is None: ex=(a,y,z)
print('(i) a<=y, th_y(z)=a => th_z(y)=th_z(a):', f1, '/', tot1, ex)
# (ii) with extra: exists c with a><c, y~c
f2=0; tot2=0; ex2=None
for y in P:
    for a in P:
        if theta(y,a)!=a: continue
        if not any(matched(a,c) and commute(y,c) for c in P): continue
        for z in P:
            if theta(y,z)!=a: continue
            tot2+=1
            if theta(z,y)!=theta(z,a):
                f2+=1
                if ex2 is None: ex2=(a,y,z)
print('(ii) + exists c: a><c, y~c:', f2, '/', tot2, ex2)
# (iii) with extra: y~a only
f3=0;tot3=0
for y in P:
    for a in P:
        if theta(y,a)!=a: continue
        for z in P:
            if theta(y,z)!=a: continue
            tot3+=1
print(tot3)
