# pa8/rpp — reconnaissance of (R'') and the chain family (W_n)  (notes, Section 5.14)

Binary notation throughout the Prover9/Mace4 files: `X*Y = theta_Y(X)`.  Instance tuples are stored as `(a, c, b, x, y)`.

## Instances and identities
- `rpp_inst.py n` — all instances of the (R'') hypotheses in P(P_n) (`inst4.pkl`: 89 696); `rpp_inst5.py seed N` — sampled instances in P_5 (`inst5_s0.pkl`: 9 482).
- `words.py`, `words2.py` — word identities (length <= 3) holding on all instances (`w4_sample.txt`: the 193 identities; they include consequences of the conclusion).
- `rel.py`, `rel2.py` — relations between r = theta_x(b), v = xc, w = yb, u = theta_a(x), m = xy.
- `alg_sat.py`, `alg_sat2.py` — SAT checks of the derived identities (theta_y(c) = theta_y(a) etc.) in P(P_m); `alg_sat2.log`.
- `h*.in` — Prover9 attempts at the derived identities (base2.txt: *-semigroup language with xy = yx assumed; pb.txt, pb2.txt: binary language with (Q1)); `sc1.in` (special case x = c, proved), `sc2.in` (special case y = b, not proved); `v3p.in`, `v4p.in` (the order variants r <= a, r <= b: proved to force a = c, resp. to be (R)); `red.in` (R'' from the derived identities + known conditions: no proof in 280 s).

## Block structure
- `harness.py` ... `harness16.py` — block-level statements tested on instances (see Section 5.14, "Towards a proof of (W_2)"; harness8–16 run on the W_2 instances `w2inst4.pkl`, `w2inst5_s0.pkl`); `kinds.py`, `kinds2.py`, `kinds3.py`, `walk*.py` — kinds of c-blocks and the abstract walk search; `deep.py` — deepest alternating chains; `joins.py` — join inequalities; `lemA_sat.py m` — SAT test of Lemma A (every c-block in one class of eps_y v eps_a) and of its hypotheses (uses the `extra` hook added to `pa_sat.solve`); `c4ex.py`, `lemA_ex.py`, `ex1.py` — example printers.

## The identification language and chains
- `ci2.py` — all minimal valid (m = 4) hypothesis sets with <= 2 auxiliaries in the commutation/identification language (`ci2.log`, `ci2_minimal.pkl`).
- `chain3.py n` — the 2^n identification words along a chain of length n (`chain3.log` for n = 3 with m = 5, `chain4.log` for n = 4 at m = 4).
- `wn_sat.py k:m ...` — SAT validity of (W_k) in P(P_m) (`wn_sat.log`).
- `w2_inst.py n` — instances of (W_2) in P(P_n) (`w2inst4.pkl`: 244 469).
- `chk_chain.py` — which non-embeddable algebras of order 8, 9 violate the chain conditions (`chk_chain.log`).

## Mace4 inputs for a bigger machine (domain 9 and up; (Tri) is omitted on purpose, it exhausts memory)
- `w3ind.in` — (Q1) + (S), (R), (R'), (V), (R''), (W2), negated (W3).  A model = a projection algebra satisfying (W2) but not (W3): would show the chain family is genuinely infinite at the first step.  Domains 6, 7, 8: exhausted, no model (domain 8 takes a few minutes alone on one core); domain 9 (`w3ind9.in`, 10-hour limit) was started on the cloud machine.
     mace4 -n 9 -N 9 -m 1 -f w3ind.in > w3ind.d9.out
- `w2_rpp.in` — (Q1) + known conditions + (W2), negated (R''): does (W2) imply (R'')?  Domains 6–8: no model.
- `rpp_w2.in` — (Q1) + known conditions incl. (R''), negated (W2): does (R'') imply (W2)?  Domains 6–8: no model.
