import pickle, numpy as np
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]
comm = (T == T.T)
R = pickle.load(open('/home/claude/pa8w/q/instQ4.pkl', 'rb')); a, c, b, d, x, y = R.T
def rank0(i):  # index of p with all blocks N
    return None
u = th(x, a)   # theta_x(a)  = x a x
ua = th(a, x)  # theta_a(x) = a x a  (= xa since commute)
tests = {
 'x->th_a(x): comm a': comm[ua, a], 'x->th_a(x): th_c=th_d': th(c, ua) == th(d, ua),
 'x->th_x(a): comm a': comm[u, a], 'x->th_x(a): th_c=th_d': th(c, u) == th(d, u),
 'y->th_a(y): comm a,b': comm[th(a, y), a] & comm[th(a, y), b], 'y->th_a(y): th_y(c)=th_y(b)': th(th(a, y), c) == th(th(a, y), b),
 'y->th_b(y): comm a,b': comm[th(b, y), a] & comm[th(b, y), b], 'y->th_b(y): th_y(c)=th_y(b)': th(th(b, y), c) == th(th(b, y), b),
 'y->th_y(a): comm a,b': comm[th(y, a), a] & comm[th(y, a), b], 'y->th_y(a): th(c)=th(b)': th(th(y, a), c) == th(th(y, a), b),
 'y->th_y(b): comm a,b': comm[th(y, b), a] & comm[th(y, b), b], 'y->th_y(b): th(c)=th(b)': th(th(y, b), c) == th(th(y, b), b),
 'th_c(x)<=a?': T[th(c, x), a] == th(c, x), 'th_a(x)<=c?': T[ua, c] == ua,
 'th_y(a)=th_y(b)?': th(y, a) == th(y, b), 'th_y(x)=th_x(y)': th(y, x) == th(x, y), 'x~b': comm[x, b], 'x~y': comm[x, y],
 'th_y(c)<=x?': T[th(y, c), x] == th(y, c), 'th_a(y)~c': comm[th(a, y), c], 'y~c': comm[y, c],
}
for k, v in tests.items(): print(f"{k:32s} fails {np.count_nonzero(~v)}")
