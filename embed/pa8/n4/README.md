# n4/ — does the path-closing family continue at length 4?  (9 October 2026)

Question: is there a path-closing condition on p0~p1~p2~p3~p4 (conclusion p0~p4) with auxiliaries x, y that is
valid in every P_X and not a consequence of the known conditions?  Language: the reduced two-auxiliary atom language
of pathclose3.py without the z = theta_p(q) and p <= z atoms (78 atoms for n = 4; 53 for n = 3):
comm(z,p_i), z <= p_i, theta_z(p_i) = theta_z(p_j), theta_{p_i}(z) = theta_{p_j}(z) for z in {x, y};
xy = yx, x <= y, y <= x, theta_x(p_i) = theta_y(p_i), theta_{p_i}(x) = theta_{p_i}(y); chords p_i ~ p_j.

* `pathclose4b.py m n npaths seed`: sampled paths in P(P_m) (vertices distinct), x, y ranging over the projections
  that commute with or lie below some path element, *including* coincidences x = y and x, y among the path elements;
  signatures (which atoms hold) written as packed records to pc4_m_n_seed.neg (p0 not~ pn) / .pos.
* `census_neg.py n`: the same records from all embeddable census algebras of order <= 9 (orders 1-7 complete,
  orders 8, 9 with `embeds` not null in post8.log / post9_*.log).
* `hit4.c`: C program; marks all subsets of size <= K of each negative record and prints the minimal unmarked sets
  that are contained in some positive record (minimal hypothesis sets valid on the sample).  `hit4 nat K neg pos`.
* `verify_hits.py n hits [mmax]`: SAT validity in P(P_m) (variables not assumed distinct, pc3_verify.valid), and
  the violation test against the seven order-9 candidates (cand9.json); library functions canon, violates.
* `mace_gen.py`: Mace4 input (conditions.in minus given labels, negated candidate instance) and Prover9 input
  (candidate as goal) for a candidate.  NB: Mace4 with the triangle condition (8 variables) exhausts memory at
  domain size 8; drop "(Tri)" and check the triangle condition on any model afterwards.  Prover9 does not find the
  instance (P2) from (Q) in 60 s, so derivability has to be tested semantically (Mace4 / census), not by Prover9.
* `explain9.py`: for the order-9 candidates 1 and 3 (the only ones with length-4 paths), the (x,y)-rows of their
  unclosed length-4 paths not contained in any negative P_5 record.  `minimise9.py` / cand1_min.json: greedy
  minimisation of those rows under SAT validity at m = 4.
* `decode.py`, `decode2.py`: the matched/order/commuting structure of the seven order-9 candidates and a readable
  form of the quasi-identities extracted for them in qi_all9.jsonl.

Results (16 000 sampled paths of length 4 in P_5, 1.0e8 negative records; hits_5_4.txt):
* 84 minimal hypothesis sets of size <= 4 valid on the sample (after x/y symmetry).  All but five contain a chord
  (p_i ~ p_j), i.e. they are conditions on a shorter path; the five chord-free ones (x commutes with p4 and one
  other vertex, p0 and p2 see x alike, p1 and p3 see x alike) all FAIL the SAT test already in P(P_4) when
  variables may coincide.
* Of the seven order-9 candidates only candidate 1 has a chordless unclosed path of length 4 ((1,8,0,4,5)); its six
  (x,y)-rows not covered by the P_5 sample are each covered after removing any single atom, and fail in P(P_5):
  candidate 1 is not explained by any two-auxiliary length-4 condition valid in P(P_5).  Candidate 3's length-4
  paths have chords (p1~p3, p1~p4).
* The quasi-identities extracted for the order-9 candidates (qi_all9.jsonl, decode2.py) are all of the shape
  "unclosed path of length 2 (or an order conclusion as in (V)) plus 6-7 auxiliary elements given by restrictions
  and half-matchings pqp = p"; six of the seven candidates have unclosed 2-paths a~c~b, a not~ b (decode output):
  cand 0: (7,8); 1: (0,1),(0,5),(4,8); 3: (1,3),(1,4),(1,7),(3,4); 4: (0,3),(1,4); 5: (3,6),(4,5); 6: (0,1); cand 2 none.
Conclusion: at order <= 9 the obstructions do not grow along the path length but along the number and kind of
auxiliaries attached to a path of length 2 (the (R) -> (R') direction) and the half-matching/order shapes ((V), (E)).
Size-5+ hypothesis sets and three auxiliaries at n = 4 were not searched (C(78,5) subsets per record is too slow
with 1e8 records; a targeted enumeration of structured candidates would be the way).

## 10 October: the candidate-6 identity rewritten  (qi.py, varB.py, checkB3b.py)

Candidate 6 of order 9 = graph semigroup a-d-b over the 2x2 band {c,e,f,g} (a over f, b over e, d over g) plus two
elements h, i with h commuting with d, i commuting with b, theta_h(a) = theta_h(d) = g, theta_h(b) = c = theta_i(a) = theta_i(d),
theta_i(b) = e.  Its extracted identity (qi_all9.jsonl) reduces to the (R')-shaped condition

  (R'')   a |><| c |><| b,  xc = cx,  theta_x(a) = theta_x(c),  yb = by,  theta_x(b) = theta_y(a)   =>   a |><| b

(B3 in varB.log; path a-d-b, x = h, y = i).  Compare (R'): ... ya = ay, theta_x(b) = theta_y(b).  Status of (R''):
valid in P(P_m) for m <= 6 (SAT, variables not assumed distinct; m = 7 running, b3m7.py), satisfied by all 92 647
embeddable census algebras of order <= 9, violated by candidate 6 and by no other candidate of order 8 or 9;
P_8^3 violates (R') but not (R''), so the two are independent.  The variants with theta_x(b) = theta_y(a), y ~ a
(equivalently theta_x(b) <= a) and theta_x(b) = theta_y(b), y ~ b (equivalently theta_x(b) <= b) are valid for
m <= 5 but have no witness of order <= 9.
Why the earlier searches missed it: the atom language of pathclose3.py has only theta_x(p_i) = theta_y(p_i), not the
cross atoms theta_x(p_i) = theta_y(p_j), i != j.  With the cross atoms added (pathclose4b.py, pc3_verify.py,
verify_hits.py, mace_gen.py) the sampled 2-path search in P_5 finds (R'') (and its mirror image) as the only
candidates explaining an order-9 algebra; verify6_2.py checks the other ~40 cross-atom candidates at m = 6.
