import sys, time, pickle
from congr import all_congruences, quotient
from analyse import props
from embed import PnData, find_embedding
from hexquot import hex_hyps_hold
Tq2, sq2, A2 = pickle.load(open("hex_smallest.pkl", "rb"))
print("size", len(Tq2), props(Tq2, sq2))
t = time.time(); congs = all_congruences(Tq2, sq2); print(len(congs), "congruences", f"({time.time()-t:.0f}s)")
for c in sorted(congs, key=lambda c: len(set(c))):
    T3, s3 = quotient(Tq2, sq2, c)
    classes = sorted(set(c)); qidx = {cl: i for i, cl in enumerate(classes)}
    A3 = [qidx[c[x]] for x in A2]
    ok, distinct = hex_hyps_hold(T3, s3, A3)
    print(f"  quotient size {len(T3)}: hyps {ok}, w!=z {distinct}, Q1={props(T3,s3)['Q1']}")
for n in range(1, 6):
    t = time.time(); D = PnData(n); s = find_embedding(Tq2, sq2, D)
    print(f"61-element Q0' -> P_{n}: {'yes' if s else 'no'} ({time.time()-t:.0f}s)", flush=True)
    if s: break
