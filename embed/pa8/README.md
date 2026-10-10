# Census of projection algebras with (Q1), (S), (R) by one-point extensions

Every finite projection algebra has a maximal element e, and P \ {e} is then a subalgebra (theta_q(p) = e forces
e <= q, so q = e).  Since (Q1), (S), (R) are quasi-identities, the algebras of order n+1 satisfying them are exactly
the extensions of the order-n ones by a new maximal element.

* `extend.py n [n2] [part nparts]` -- reads `ord<n>.json` (list of tables, T[x][y] = x*y = theta_y(x)) and writes
  `ord<n+1>.json`; Mace4 gets the base table as ground equations and finds all extensions; reduction up to isomorphism
  by `layered_search.canon`.  Parallel runs: `extend.py 8 9 0 2` and `extend.py 8 9 1 2`, then `extend.py 8 9 -1 2`
  to merge.  Checkpoints `ext<n>_<part>.ckpt` (resumable).  Needs mace4/interpformat/isofilter in /home/claude/bin
  (edit `extensions()` for another location) and the modules of the parent directory (set EMBED_DIR if the script is
  run from elsewhere).
  Counts: 1, 2, 5, 16, 62, 295, 1662, 10828, 80039, 658727 (orders 1..10; the last from `extend.py 9 10 0 1`, 8.2 h on one core, log `ext9_0.log`; `post8.py 10 ...` not run).
* `post8.py n [MS]` -- for every algebra in `ord<n>.json`: triangle condition, embeddability into P(P_m)
  (backtracking m <= 4, SAT m = 5..MS); one JSON line per algebra in `post<n>.log`; algebras containing a known
  non-embeddable algebra of smaller order (from `post<k>.log`) as a subalgebra are marked `minimal: false` and not
  tested.  Any algebra with `embeds: null` and `minimal: true` is a minimal non-embeddable algebra.
  Order 8: all 10828 satisfy the triangle condition; 10821 embed with m <= 7; the seven with `embeds: null` in
  `post8.log` are P_8^1..P_8^7 of the notes (in this order).
* `cand8.py`, `cand8b.py` -- structure of the seven (bottom band, order, matched/commuting pairs; one-point deletions
  and the graph-semigroup structure of the deleted algebra).  Output `cand8.out`.
* `qi_extract.py`, `qi_all.py` -- greedy minimisation of the diagram of a candidate under a SAT validity test in
  P(P_m) (partial tables, conclusion negated by a fresh element and a distinctness constraint); results `qi_all.jsonl`.
* `../pathclose3.py` -- two-auxiliary path-closing signatures in P(P_m) with chord atoms; saves `pc3sig_m_n.pkl`.
* `pc3_hit.py` -- for a candidate algebra, the minimal hypothesis sets (hitting sets of the negative signatures)
  violated by it; `full_valid_ones` filters by SAT validity without distinctness (`pc3_verify.py`).
  Logs `fv_4_2.log` (n = 2), `fv_4_3*.log` (n = 3).
* `pc1_classify.py` -- all one-auxiliary hypothesis sets of size <= 4 for n = 3 (76, from `pc1_4_3_size4.pkl`), SAT
  validity at m = 4, 5, and countermodels among the census algebras of order <= 8; output `pc1_classified.json`.
  `pc1_4_3_size5.pkl`: the 8 minimal sets of size 5.
* `verify6.py m` -- SAT verification of the new conditions (R'), (V), (P1), (P2), (Q), ... at level m.
* `mace_r2_not_r/` -- Mace4: no projection algebra of order <= 8 with (Q1) and (R') violating (R).

## Order 9

`post8.py 9 7 PART NPARTS` (logs `post9_*.log`): 80039 algebras; 163 contain one of P_8^1..P_8^7 (all violate one of the
new conditions, `newconds.py`), 1 violates (R') without containing them, 79783 embed with m <= 7, 92 candidates.
`pass2_9.py PART NPARTS 8` (logs `pass2_9_*.log`): of the 92, 39 are semilattices (embed in P(P_8)), 46 embed in
P(P_8), 7 embed in no P(P_m), m <= 8: `cand9.json`, described in `cand9.out`.  `sat8.py 8`: the seven of order 8
do not embed in P(P_8) (`sat8.log`).  `verify7.py 7`: (V), (R'), (P1) hold in P(P_7) (`verify7.log`).

## rp/ — the proof of (R') (Theorem thm:Rp)
* `rp_inst.py n` enumerates all instances (a,c,b,x,y) of the hypotheses of (R') in P(P_n) (n=3: 2273, n=4: 91172); `rp_inst5.py seed N` samples N matched pairs (a,c) in P_5 and enumerates the rest (`inst5_s7.pkl`, 278655 instances, not copied: 7 MB).
* `rp_words.py`, `rp_min.py`, `rp_rel.py`: word equations of length <= 3 valid in all instances (`words4.txt`), minimal hypothesis subsets for them, order/commutation relations among the derived projections.
* `rss_base.txt`, `g_*.in`, `pa_base.txt`, `pa_*.in`, `m4_*.in`, `core.m4.in`, `batch_words.sh`: Prover9/Mace4 inputs for the algebraic Step 1 (regular *-semigroup form with e=x, f=y; projection-algebra form with prolog-style variables and (Q1)). `pa_yc`, `pa_cy`, `pa_xa`, `pa_mx`, `pa_ava`, `pa_uw`, `pa_wu`, `pa_w`, `g_xab`, `g_xa`, `g_xb` are proved; `pa_core*`, `m4_w2` show that neither `ubu=u` nor `theta_b(u)=theta_b(v)` suffices as an intermediate (countermodel P_7).
* `blocks.py`, `harness.py` (structure of an instance: blocks, Gamma/Delta/rho/sigma classes) and `harness2..13.py`: block-level statements tested on all P_4 instances (and `harness13.py 5 inst5_s*.pkl` on the P_5 samples). `harness13.py` checks exactly the lemmas used in the proof (reduction of Step 3, L1-L3), `harness5.py` the key statement (S24) = eq. (Rp-goal). The `*_ex.pkl` files hold a failing instance for each statement that fails.
