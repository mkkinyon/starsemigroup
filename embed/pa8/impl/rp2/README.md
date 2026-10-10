# pa8/impl/rp2 — the hybrid chain family (R'_n) and its witnesses P^{R'}_n  (notes, Section 5.17)

Binary notation `X*Y = theta_Y(X)`; tables `T[i][j] = i*j`.

- `mk10.py`, `mk10.json`, `mk10_T.json` — M. Kinyon's Mace4 model (11 Oct 2026): smallest projection algebra with (Q1), (S), (R), (R'), (V), (R''), (W2) but not (R'_2); order 10, constants a=0, b=1, c=2, k=3, p=4, q=5.
- `st10.py` — its structure (theta maps, order, commuting and matched pairs); `an10.py` — violating instances, irreducible elements, maximal subalgebras, isomorphism test against the known algebras; `emb10.py full|max` — SAT embedding of the algebra (none for m <= 7) and of its maximal subalgebras (all embed, m <= 5); `w4chk.py` — (W_n), n <= 4, and (R'_n), n <= 3, by brute force.
- `simp.py` — simpler 5-variable candidates (last link matched instead of commuting) all fail at m = 4.
- `minsets.py`, `minsets.log` — the minimal valid (m = 4, confirmed m = 5) subsets of the 11 hypotheses the model offers: exactly (R'_2) and its variant theta_k(b) = q.
- `rp2_m6.py`, `rp2_m6.log` — SAT validity of (R'_2) in P(P_m), m = 5 (valid, 16 s), m = 6 (running).
- `rpfam.py` — the family P^{R'}_n (Definition 5.35), `R{n}.json`, `R{n}_T.json` for n <= 5; checks the axioms and (Q1); n = 2 is isomorphic to the Mace4 model, n = 1 to P_8^3.
- `rpchk.py n [mmax]`, `rpchk.log` — for P^{R'}_n: (R'_j) violations, (W_j) violations, all labelled conditions (evalcond2), maximal subalgebras, SAT embedding.
- `iso8.py` — P^{R'}_1 = P_8^3.
- `rp3ind.in`, `w4ind.in` — Mace4 inputs for the next separations ((R'_2) but not (R'_3); (W3) but not (W4)); expected smallest models P^{R'}_3 (order 12) and P^{ch}_4 (order 13). Domain 5 exhausted in seconds; domains 10–12 are long runs.
