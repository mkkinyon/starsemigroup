# pa8/red — reductions, invariant search, the two join statements (notes, Section 5.19)

- `inst.py n` — instances of the (R'_2) hypotheses in P_n (`rp2inst4.pkl`: 1 213 522).
- `redsearch.py INST VARS [level]` — substitution reductions of a condition to a proved one (terms of depth 1 or 2); `red_*.log`.
- `ids.py`, `ids_w2.py`, `ids_w2_long.py` — word-identity surveys ((R'_2); (W_2) length <= 3; (W_2) length <= 5 over a,c,x,y).
- `rel.py`, `dbg.py` — specific relations for (R'_2); `alg_cy.in`, `alg_by.in` — Prover9: c~y (fails), b x2 = b y (proved).
- `lemA2_sat.py`, `lemA3_sat.py`, `lemA4_sat.py`, `cex.py` — Lemma A along chains and failed propagation forms.
- `closing.py` — commutation replaced by block properties: fails.
- `contract.py`, `contract2.py`, `contract3.py` — no contracting z: (W_2) does not reduce to (W_1) (330 instances).
- `inv.py`, `inv2.py`, `inv3.py`, `inv4.py` — two-point clause language over (x; a, c), chain-valid clauses, propagation fixed points (`inv2_m4_K*.pkl`, `invQ_m5.pkl`, `inv4*.pkl`, logs).
- `inv5.py`, `inv5close.py` — clauses over (y; a, c, b) valid under (W_2), the 40 that need the x-link; `inv6.py` — clauses with one 3-join atom.
- `goal*.py`, `g12.py`, `g12cex.py`, `g12all.py`, `equiv.py` — the statements G1 (eps_c <= eps_a v eps_b) and G2 (no class of a v b v c with two T(c)); closing lemma; G1, G2 under all 2-path conditions.
- `genq.py`, `five.py`, `g2prime.py`, `chk_ii.py` — further candidate invariants along chains.
- `obstr.py`, `whichfail.py`, `findx.py`, `blocktypes.py`, `classtypes.py` — the obstruction configuration and its analysis.
