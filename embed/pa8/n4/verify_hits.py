"""Verify hitting-set candidates: SAT validity in P(P_m) for m = 4, 5 (full validity, variables not distinct),
then test against the order-9 census candidates (cand9.json) for violation.
Usage: python3 verify_hits.py n hitsfile [mmax]"""
import sys, os, json, time, itertools
os.environ['EMBED_DIR'] = '/home/claude/pa8w/embed'
sys.path.insert(0, '/home/claude/pa8w/embed/pa8'); sys.path.insert(0, '/home/claude/pa8w/embed')
from pc3_verify import valid
from pathclose4b import atoms_for, fmt
def canon(h, A):
    """swap x<->y and take the lexicographically smaller index tuple"""
    sw = {'x': 'y', 'y': 'x'}
    idx = {a: i for i, a in enumerate(A)}
    def swap(at):
        if at[0] in ('x', 'y'): return (sw[at[0]],) + at[1:]
        if at[0] == 'xy':
            if at[1] == 'xley': return ('xy', 'ylex')
            if at[1] == 'ylex': return ('xy', 'xley')
        return at
    h2 = tuple(sorted(idx[swap(A[k])] for k in h))
    return min(tuple(sorted(h)), h2)
C9 = json.load(open('/home/claude/pa8w/embed/pa8/cand9.json'))
def violates(T, H, n):
    """does the algebra T (T[x][y] = theta_y(x)) violate H => p0 ~ pn (distinct path vertices)?"""
    N = len(T)
    def th(p, q): return T[q][p]      # theta_p(q)
    mt = lambda p, q: th(p, q) == p and th(q, p) == q
    adj = {p: [q for q in range(N) if q != p and mt(p, q)] for p in range(N)}
    def ok(P, x, y):
        Z = {'x': x, 'y': y}
        for at in H:
            if at[0] == 'ch':
                if not mt(P[at[1]], P[at[2]]): return False
            elif at[0] in ('x', 'y'):
                z, k = Z[at[0]], at[1]
                if k == 'comm' and th(z, P[at[2]]) != th(P[at[2]], z): return False
                if k == 'zle' and th(P[at[2]], z) != z: return False
                if k == 'sees' and th(z, P[at[2]]) != th(z, P[at[3]]): return False
                if k == 'seen' and th(P[at[2]], z) != th(P[at[3]], z): return False
            else:
                k = at[1]
                if k == 'comm' and th(x, y) != th(y, x): return False
                if k == 'xley' and th(y, x) != x: return False
                if k == 'ylex' and th(x, y) != y: return False
                if k == 'sees' and th(x, P[at[2]]) != th(y, P[at[2]]): return False
                if k == 'seen' and th(P[at[2]], x) != th(P[at[2]], y): return False
                if k == 'xsees' and th(x, P[at[2]]) != th(y, P[at[3]]): return False
                if k == 'xseen' and th(P[at[2]], x) != th(P[at[3]], y): return False
        return True
    def paths(pre):
        if len(pre) == n + 1: yield pre; return
        for q in adj[pre[-1]]:
            if q not in pre: yield from paths(pre + [q])
    for p0 in range(N):
        for P in paths([p0]):
            if mt(P[0], P[-1]): continue
            for x in range(N):
                for y in range(N):
                    if ok(P, x, y): return (P, x, y)
    return None
def main():
  n = int(sys.argv[1]); hits = sys.argv[2]; mmax = int(sys.argv[3]) if len(sys.argv) > 3 else 5
  A = atoms_for(n)
  hs = sorted({canon(list(map(int, l.split()))[1:], A) for l in open(hits)}, key=lambda h: (len(h), h))
  print(len(hs), 'candidates after x/y symmetry', flush=True)
  out = []
  for h in hs:
      H = [A[k] for k in h]; s = ', '.join(fmt(a) for a in H); res = []
      t = time.time()
      for m in range(4, mmax + 1):
          v = valid(H, n, m)
          res.append((m, v))
          if not v: break
      if res[-1][1]:
          viol = [k for k, T in enumerate(C9) if violates(T, H, n)]
          print(f"VALID m<={mmax}: {s}   violated by order-9 candidates {viol}  ({time.time()-t:.0f}s)", flush=True)
          out.append((h, viol))
      else:
          print(f"fails at m={res[-1][0]}: {s}", flush=True)
  json.dump([[list(h), v] for h, v in out], open(hits + '.valid.json', 'w'))
if __name__ == '__main__': main()
