import sys; sys.path.insert(0,'/home/claude/repo/starsemigroup/embed')
import hotel_sat as H
th, pr, matched, comm = H.th, H.pr, H.matched, H.comm
H.CONDS['Sq'] = dict(vars='abcdg', hyp=matched('a','c')+matched('c','b')+matched('b','d')
    +[(pr('g'), th('c','d')), (pr('g'), th('d','c')), (th('a','g'), th('b','g'))], concl=('mt','a','d'))
H.CONDS['P2'] = dict(vars='abcdx', hyp=matched('a','c')+matched('c','b')+matched('b','d')+comm('x','a')+comm('x','b')
    +[(th('x','c'), th('x','b')), (th('c','x'), th('d','x'))], concl=('mt','a','d'))
H.CONDS['Q'] = dict(vars='abcdxy', hyp=matched('a','c')+matched('c','b')+matched('b','d')+comm('x','a')+comm('y','a')+comm('y','b')
    +[(th('c','x'), th('d','x')), (th('y','c'), th('y','b'))], concl=('mt','a','d'))
name, f, d, B = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
H.run(name, f, d, B)
