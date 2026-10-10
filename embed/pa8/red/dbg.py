import sys, pickle, random
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import mul
n = 4; inst = pickle.load(open('rp2inst4.pkl', 'rb'))
def m(p, q): return mul(p, q, n)
def ev(w, V):
    r = V[w[0]]
    for ch in w[1:]: r = m(r, V[ch])
    return r
L = 'acbxzy'; le = lambda p, q, V: ev(q+p+q, V) == ev(p, V)
random.seed(2); S = random.sample(inst, 30000)
for I in S:
    V = dict(zip(L, I))
    if not le('zcz', 'cy', V):
        print('instance', I)
        for t in ['zcz <= c', 'zcz <= y', 'zcz <= zy', 'c ~ y', 'z ~ y', 'zy = yz']:
            pass
        print('zcz<=c', le('zcz','c',V), 'zcz<=y', le('zcz','y',V), 'zcz<=zy', le('zcz','zy',V), 'zy=yz', ev('zy',V)==ev('yz',V), 'cy=yc', ev('cy',V)==ev('yc',V))
        print('zcz', ev('zcz',V)); print('zaz', ev('zaz',V)); print('m a b a m', ev('zyabazy',V)); print('cy', ev('cy',V)); print('cy zcz cy', ev('cyzczcy',V))
        print('r=zbz', ev('zbz',V), 'yby', ev('yby',V))
        break
