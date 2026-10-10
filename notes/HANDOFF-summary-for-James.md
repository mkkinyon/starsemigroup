# Handoff: write a "state of play" document on the partition-monoid embedding problem

## What you are given

- `notes-embedding.pdf` / `notes-embedding.tex` (52 pages, 15 Sept 2026): the working notes of M. Kinyon and Claude on which regular *-semigroups (equivalently, which projection algebras) embed in a partition monoid P_X. This is the **master document**. Do not edit it; it is still being extended by another session.
- `status-table.tex`: a one-page table of the eleven known necessary conditions, with their status and where each is proved or verified in the notes. Its numbering matches the notes. Build the summary around this table; check the summary against it, not the other way round.
- `conditions.in`: every condition stated once, unambiguously, in Prover9 syntax for projection algebras (binary `X*Y = theta_Y(X) = Y X Y`). Use it to resolve any doubt about the exact hypotheses of a condition.
- `pa8/README.md` (optional): what the code files do. The summary does not need to discuss code beyond naming the file that produced a result.

## Deliverable

A **separate** LaTeX document, `embedding-summary.tex`, of about 8–12 pages, for James East (a coauthor who knows partition monoids and regular *-semigroups well but has not followed these notes). Its purpose is to let him catch up in an hour, then use the full notes as a reference. Suggested contents, in this order:

1. The problem and the setting (one page): projection algebras, P(P_X), the block calculus for products of projections in P_X (Section 1 of the notes), the projection condition (Q1) and its reformulation (Section 2).
2. The known necessary conditions, as a table (use `status-table.tex`) followed by a short paragraph on each: what it says in words, what violates it, and its status.
3. The three main structural results stated precisely: the matching-pattern/triangle conditions and the master-condition theorem (Section 4); the wiring obstruction and the characterisation of embeddable graph semigroups and layered graph semigroups (Section 5.1–5.5); the census method (one-point extensions) and what it found at orders 7, 8, 9 (Sections 5.6–5.8, Remark 5.22(3)).
4. Proof *sketches* (half a page each at most) of (S), (V), (R'), (P1): the shape of the argument and which lemma carries the weight, with a pointer to the theorem in the notes.
5. What is proved by computation and how (Section 6; the verification levels below).
6. Open questions (Section 7), ending with what is being worked on next: a hand proof of (Q), which would also cover (P2) and give a computer-free proof of the hub case of (S).

Plain expository prose; theorem-proof style only for the precise statements. Use the notes' notation (theta_q(p) = qpq, ≤, ⋈, the classes Γ_i, Δ_i, Λ_i when sketching proofs) so that James can move between the two documents without translation.

## Constraints (important)

1. **Do not blur the three levels of evidence.** The notes carefully distinguish (a) *proved* for every X, (b) *verified* in P(P_m) for m ≤ 7 by SAT, and (c) *no embedding found* into P(P_m) for m ≤ 8. Level (c) is not proof of non-embeddability: the notes give a 9-element semilattice that embeds in P(P_8) but in no P(P_7). Every statement in the summary about a condition or a candidate algebra must say which level it is at. The "Caveat" paragraph in Section 5.8 and the preamble of Proposition 5.19 are the authoritative wording; keep their content.
2. **Do not paraphrase the proofs of (R') and (P1)** (Theorems 5.23 and 5.25). They are intricate, and a rewording could silently change a case split. Either summarise the strategy in your own words at the level of "which invariant is maintained and why it closes the argument", or quote. The same applies to the hub case of (S), which is a computer check, and must be described as such.
3. **Do not change any mathematical statement** relative to the notes: hypotheses of conditions, which algebra violates which condition, orders and counts (1 663 algebras of order 7, 10 828 of order 8, 80 039 of order 9; candidates 1, 7, 8; proved 1, 3, 1), timings. If the notes and `status-table.tex` seem to disagree, report the discrepancy in a "queries" list at the end of the summary instead of resolving it yourself.
4. **Do not add results.** No new lemmas, conjectures, or "it is easy to see" strengthenings, even if they look obvious; several natural-looking strengthenings were checked and found false in P_4 (e.g. Remark 5.22(4)–(5)). If something seems worth saying, put it in the queries list.
5. The chronology of the notes (what was found when, what searches were run and stopped) is *not* wanted in the summary, except where it explains why a result has the shape it has (e.g. why (R') was found after (R)).
6. Output only `embedding-summary.tex` (self-contained, compiling with pdflatex, amsmath/amsthm/booktabs) plus a short `queries.md` with any discrepancies or doubts you encountered. Do not produce a modified copy of the notes.

## Verification levels, for reference

- Proved for all X: (Q1), triangle/hexagon, (S), (R), (R'), (V), (P1).
- Verified in P(P_m) for m ≤ 7 by SAT (`pa8/verify6.py`, `pa8/verify7b.py`): (Q), (P2), (E6), (E1). Also all of the above for m ≤ 6 as a sanity check.
- Candidate algebras: no embedding into P(P_m) for m ≤ 8 (SAT). Non-embeddability is *proved* only when the algebra violates a proved condition.
