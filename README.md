# starsemigroup

Working repository for the project on regular *-semigroups and partition monoids
(M. Kinyon, with Claude). Two threads:

* **Embedding problem** — which regular *-semigroups / projection algebras *-embed
  in a partition monoid P_X. The working notes are `notes/notes-embedding.tex`
  (PDF alongside); they are a running record, not a paper. `notes/status-table.tex`
  summarises every necessary condition found so far with its evidence level
  (proved / verified in P(P_m) for small m by SAT / no embedding found for small m),
  and `notes/conditions.in` collects the projection-algebra axioms and all conditions
  as Prover9/Mace4 clauses in the binary notation `X*Y = theta_Y(X)`.
* **Rigidity of the involution** — the markdown files in `rigidity/` (earlier thread).

## Layout

* `notes/` — the notes, status table, `conditions.in`, the K-catalogue, the cold-read
  reports (10, 11, 16 Oct 2026) and the handoff files. State on 16 Oct 2026 (evening): all seven
  order-8 candidates are proved minimal non-embeddable (the last two by K4, Thm 5.49, and K0, Thm 5.50);
  the variant K0'' of K0 (same proof) settles the order-9 candidate 5, and K0, K4 settle candidates 0 and 4;
  open are the order-9 candidates 1, 2, 3, K5 as a condition, and the chain family (R'_n).
* `embed/` — all code and logs of the embedding thread (Python 3; SAT via `pysat`;
  Prover9/Mace4 inputs `*.in`, outputs `*.out`). The directory structure is described
  in the "Files" paragraph of the notes (Section "Computations"). Recent subdirectories:
  * `embed/pa8/n4/` — the 2-path search language with auxiliaries (Section 5.13).
  * `embed/pa8/rpp/` — reconnaissance of (R'') and the chain family (W_n) (Section 5.14);
    see its `README.md`.
  * `embed/pa8/w3/` — the order-11 witnesses of (W_3) and of the triangle condition.
  * `embed/pa8/wn/` — the explicit chain witnesses P^ch_n (`family.py`, `check.py`).
  * `embed/pa8/impl/` — the implication/independence matrix of all conditions.
  * `embed/pa8/red/` — K4 reconnaissance (`k4rec*.py`, `k4drop.py`, `k4sat.py`): Theorem 5.49, 16 Oct.
  * `embed/pa8/k0/` — K0 reconnaissance and the dropped-hypothesis maps of Theorem 5.50 (16 Oct, evening);
    see its `README.md`.
  * `review3/`, `review4/` — the cold reads of 16 Oct (K4: gap found and repaired; K0: one justification added).
* `embed/pa_sat.py` — SAT embedding of a partial projection-algebra table into P(P_m).

Large data files (instance pickles, `.pos`/`.neg` signature files, anything over 5 MB)
are not in the repository; the scripts that produce them are.

## Conventions

* Projection algebra in binary notation: `x*y = theta_y(x) = y x y`; `q <= p` iff
  `q*p = q`; `p` and `q` commute iff `p*q = q*p`; `p |><| q` (matched/friendly) iff
  `q*p = p` and `p*q = q`.
* Mace4/Prover9 files use `set(prolog_style_variables)`: capitalised symbols are
  variables, lowercase symbols are constants (never `u`–`z` as constants without that
  flag).
* Tables in JSON files are `T[i][j] = i*j = theta_j(i)`.
