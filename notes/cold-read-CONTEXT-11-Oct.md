# Context for the cold read (11 Oct 2026)

Project: which finite regular *-semigroups (equivalently, which finite projection algebras) *-embed in a partition
monoid P_X.  Collaboration between M. Kinyon (mathematician) and Claude (AI).  `notes-embedding.tex/.pdf` (73 pages,
11 Oct 2026) is a WORKING DOCUMENT keeping track of progress; it is NOT intended for publication in this form, so do
not review it as a paper (style, length, repetition, chronology are not the point).  What matters: mathematical
correctness, whether the three evidence levels are kept apart (proved / verified in P(P_m) for small m by SAT /
no embedding found for small m), whether the overall direction is sensible, and what to do next.

A first cold read was done on 10 Oct 2026 (`previous-cold-read-10-Oct.md`, with an addendum); its findings were
incorporated (Step 4 of the (Q) proof was repaired, the textual fixes made).  You may use it to see what has already
been checked; do not re-review those parts in depth, but do say if anything there is inconsistent with the new material.

NEW SINCE THEN (Sections 5.14-5.19 of the notes, status-table rows (W_2), (W_n), (R'_n)), which is what this read is for:
 * the chain families (W_n) (a |><| c |><| b, chain c ~ x_1 ~ ... ~ x_n ~ b of commuting projections each
   identifying a with c, theta_{x_i}(a) = theta_{x_i}(c)  =>  a |><| b) and the hybrid (R'_n);
 * explicit witnesses P^ch_n (order 2n+5, Definition 5.33) and P^{R'}_n (order 2n+6, Definition 5.35), Mace4 models
   of M. Kinyon of orders 11 and 10 as the n = 3 resp. n = 2 members;
 * conditional non-finite-basis theorems 5.34 and 5.36;
 * Proposition 5.37: explicit embeddings of ALL maximal proper subalgebras of both families, for all n, into
   P(P_m), m <= 2n+3 (verified by computer for n <= 7: `code/chemb.py`, `code/rpemb.py`, `code/verify7.log`);
 * the closing lemma 5.38 (G1 and G2 imply a |><| b) and the analysis of Section 5.19 of why no uniform proof
   of (W_n) has been found: the two-point-language invariant searches, their failure in P(P_5) resp. P(P_6),
   the statement (T_n), the unbounded radius of the component of c in the identification graph.
 The status is: (W_n), (R'_n) are verified in P(P_m) for small m only; nothing in 5.14-5.19 is a proof of
 validity in P_X; the embeddings of 5.37 and Lemma 5.38 are proved.

Questions on which an evaluation is wanted:
 1. Are Definitions 5.33/5.35 and Theorems 5.34/5.36 correct as stated (in particular the irreducibility argument
    and the variable counts)?  Are the proofs complete?
 2. Is Proposition 5.37 correct?  Spot-check at least two of the listed embeddings by hand with Lemma 1.1(a),
    and/or rerun `python3 code/chemb.py 4`, `python3 code/rpemb.py 4` (they need `code/pmon.py` and
    `family.py`/`rpfam.py` on the path; see the headers).  Is the "proof" (block types independent of n) acceptable
    as a proof, or does it need the routine list written out?
 3. Is Lemma 5.38 correct?  Is the reduction of all 2-path conditions to (G1), (G2) a real simplification?
 4. Section 5.19: is the conclusion "no bounded local invariant exists, the proof must be carried by the chain"
    justified by the evidence given, and is the obstruction (h)/(T_n) real?  Do you know an existing argument or
    theory (chained projection groupoids of East-Azeef Muhammed, biordered sets, representation games, anything)
    that handles chains of commuting projections of unbounded length?
 5. What should be done next: continue towards a hand proof of (W_2) by the Steps 2-8 method of Theorem 5.23?
    switch to the groupoid formulation?  something else?  Please prioritise.
 6. Any errors, inconsistencies or conflations of evidence levels anywhere in the new material; also check that the
    status table and Section 5.16(b) (implications/independence) agree with Sections 5.17-5.18.

Conventions: binary notation x*y = theta_y(x) = y x y; q <= p iff q*p = q; p ~ q means commuting; p |><| q
("matched"/"friendly") iff q*p = p and p*q = q; tables T[i][j] = i*j.  Prover9/Mace4 files use
set(prolog_style_variables).  `code/pmon.py` multiplies partitions of P_n (`mul(p, q, n)`; a projection is a
partition of {0..2n-1} with the lower copy at +n; `projections(n)`).  `code/evalcond2.py` evaluates all labelled
conditions of conditions.in on a table given as JSON (`mk10.json` = M.K.'s order-10 model, `model11.json` = the
order-11 model).

Please write your report as REPORT.md in this folder, in the same form as the previous one (state of the problem as
you understood it; mathematical scrutiny section by section; conceptual assessment; prioritised next steps; the three
most valuable things for the next session).
