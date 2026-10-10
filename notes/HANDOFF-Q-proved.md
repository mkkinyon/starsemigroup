# Addendum to `HANDOFF-summary-for-James.md` (18 September 2026): (Q) is now proved

Read this after the original handoff. It changes the status of two conditions and two witnesses;
everything else in the original handoff stands. The attached `notes-embedding.pdf` / `.tex`
(60 pages, 18 Sept 2026) and `status-table.tex` are the current versions; use their numbering.

## What changed

1. **(Q) is proved for every P_X** (Theorem 5.29, Section 5.11). Hence, in every projection
   algebra, (P2) and (S) follow (Proposition 5.32(a)), so:
   - (P2) is proved (Corollary 5.30);
   - the hub case of (S) (Theorem 5.6), which rested on a finite computer check (`hubtypes.py`),
     now has a computer-free proof as a special case of (Q) (Corollary 5.30, Remark 5.31(2));
   - 𝔓_8^4 (violates (P2)) and 𝔓_8^5 (violates (Q)) are *proved* minimal non-embeddable projection
     algebras. The count of proved candidates of order 8 is now 5 of 7.
2. Still only *verified* in P(P_m) for m ≤ 7: (E6) and (E1); their witnesses 𝔓_8^6 and 𝔓_8^1
   remain candidates (no embedding into P(P_m), m ≤ 8; not proved). The Caveat of Section 5.8
   and the preamble of Proposition 5.19 have been reworded accordingly.
3. The abstract, the Caveat, the paragraph after Proposition 5.32 and Question 7.3 have been
   updated; the list of proved conditions is now (Q1), Tri, (R'), (V), (P1), (Q), with the
   redundant (S), (P2), (R).

## Shape of the proof of (Q) (for the summary's proof-sketch section; half a page at most)

Write the path as a ⋈ c ⋈ b ⋈ d with matched blocks A_i ↔ C_i ↔ B_i ↔ D_i, hypotheses
xa = ax, θ_c(x) = θ_d(x), ya = ay, yb = by, θ_y(c) = θ_y(b); conclusion a ⋈ d.
- Step 1 normalises x to u = xa ≤ a. The blocks of u group the indices i into *groups* G.
- Step 2 (from θ_c(u) = θ_d(u) and the transport lemma) shows that Π_1 = ε_u ∨ ε_c = ε_u ∨ ε_d,
  whose classes Γ_G contain the A_i, C_i (i ∈ G), and that each group is a *non-hub*
  (c and d have the same N-blocks in Γ_G, and the same union of T-blocks) or a *hub* (C_G is a
  single N(d)-block and Γ_G ∩ supp d is a single N(c)-block E_G = D_{π(G)}, π a permutation of the
  hubs). Hubs have |G| ≤ 2 and are "cross-wired" on the b-side. The key new observation is that
  every class of ρ = ε_a ∨ ε_d inside Γ_G contains some A_i (because Π_1 = ρ ∨ ε_u).
- Step 3 (from y): blocks of a are of "b-type" (they meet supp c ∪ supp d only inside supp b) or
  "N-type" (contained in an N(b)-block which is an N(y)-block); a lemma (∗) about the classes of
  ε_y ∨ ε_c not meeting supp c.
- Step 5 attaches to N(b)-blocks and to common N-blocks an *index pair* (λ, δ) (the indices of
  their classes in ε_b ∨ ε_d and ε_c ∨ ε_b); the pair is preserved along chains of N-type blocks
  and is reset to a diagonal or undefined pair at b-type blocks ("rigidity").
- Steps 6–7 (Propositions 5.27, 5.28): inside each Γ_G, chase pairs along chains of N-blocks to
  show that each T(d)-block is attached to a unique T(a)-block and vice versa; for hubs this gives
  |π(G)| ≤ |G|, hence equality by counting over the permutation π, and then the matching.
Do not paraphrase the case analysis of Proposition 5.28; describe the invariant (the index pair
and its rigidity) and point to the proposition.

## Verification levels (updated)

- Proved for all X: (Q1), triangle/hexagon, (S), (R), (R'), (V), (P1), (P2), (Q).
- Verified in P(P_m) for m ≤ 7 by SAT: (E6), (E1) (and, as a sanity check, all of the above).
- Candidates (no embedding into P(P_m), m ≤ 8; not proved): 𝔓_8^1, 𝔓_8^6, and the seven new
  candidates of order 9.
