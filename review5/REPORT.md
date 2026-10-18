# Cold read of `paper/embedding.tex` (draft of 18 Oct 2026)

Scope: the whole file was read in order; every algebraic identity in Sections 2, 3, 5.2, 5.3 (incl. Cor. 5.5), 5.4, 5.5, 5.6 (incl. Cor. 5.13), Step 1 of 5.7, 5.9, 6.1–6.4 and 7 was checked by hand; the ported proofs of (A2), (P1), (Q) were read for the e/f/u/v renaming and for the type numbering of Lemma 2.6(b); the eight displayed conditions of 5.1 were compared with `fig-wiring.tex`; all `\ref`s were resolved through `embedding.aux`. Small computations (Python, block calculus of `fast.py`) were used only to test the tables of Section 5.9, the chain witnesses for n ≤ 4, Remark 3.2, the example in Step 2 of (Q), and Lemma 6.1 for k = 1, 2. Line numbers refer to `embedding.tex`.

Numbering of results follows `embedding.aux` (Lemma 2.6 = `lem:PX`, Lemma 2.7 = `lem:order`, Theorem 5.3 = `thm:Rp`, Proposition 5.21 = `prop:witnesses`, Lemma 6.1 = `lem:radius`, etc.).

---

## A. Errors or gaps in proofs

1. **(PC) is never proved for P_X, although the paper says it is.** Section 2.2, line 186: "In P_X, as we recall in Section 2.3, two projections with a common lower bound commute." Section 2.3 contains no such statement or proof, and nothing else in the paper proves (PC) in P_X (line 1049 cites Proposition 2.4(4), which is an equivalence *assuming* (PC)). Yet (PC) in P_X is used in almost every proof (Step 1 of Theorem 5.3, Theorem 5.6, Theorem 5.8, Step 1 of (Q), Step 1 of Theorem 5.15, Section 6.1, ...), and the `\todo` at line 88 says the result is unpublished. Gap in the exposition, not in the mathematics; repaired by four lines from Lemmas 2.6/2.7: if r ≤ p, q then every block of p and of q lies in a block R of r and every N(p)-block (resp. N(q)-block) is an N(r)-block; a class K of ε_p ∨ ε_q lies in one block R of r; if R is a T(r)-block it is a union of T(p)-blocks and of T(q)-blocks, so K is of type (i); if R is an N(r)-block it is an N(p)-block or a union of T(p)-blocks, and likewise for q, giving types (ii), (iii), (iv) with K = R; by the converse of Lemma 2.6(b) (item A5) pq = qp. *Fix:* add this as Lemma 2.6(d) or a corollary after Lemma 2.7, and change line 186.

2. **Lemma 2.7(a) (lines 243–253) is false as stated.** "q ≤ p iff every block of p lies in a block of q and every N(p)-block is a block of q." Counterexample: X = {1}, p = ({1}, N), q = ({1}, T): both conditions hold but θ_p(q) = p ≠ q. The proof of ⇐ (line 252) ignores N(p)-blocks that are T(q)-blocks. Typo-level: replace "is a block of q" by "is an N(q)-block" (the proof then works). Only the ⇒ direction is used elsewhere (lines 262, 277, 647, 714, 784), so nothing propagates.

3. **Lemma 6.1 (radius, lines 1055–1063): statement does not match the proof, and is false.** It says z is at distance exactly k+1 from c "in the comparability graph of Id(a,c)". The upper bound in the proof is a chain c ∼ y_1 ∼ … ∼ y_k ∼ z of *commuting* identifiers (consecutive y_i, y_{i+1} are not comparable), and the lower bound is proved for chains of commuting identifiers. Computation for k = 2 (5 points): distance 3 = k+1 in the graph "adjacent iff commute", distance 4 in the comparability graph. *Fix:* state the lemma for the graph on Id(a,c) in which two identifiers are adjacent when they commute (equivalently: z is a chain end of (W_{k+1}) but of no (W_n), n ≤ k); the sentence before it (unbounded radius) is true for either graph. Also, line 1062 "{p_i,q_i} is a nontransversal block of y_{j+1}": maximality of j only gives that it is a *block* of y_{j+1}; it may be transversal (the argument survives: in types (i) and (ii) it is a union of T(y_j)-blocks).

4. **Proposition 5.21 (lines 1004–1014) is false for 𝔓_7, with consequences for Theorem 1.4.** 𝔓_7 also violates (X): with (a,b,c,t) := (x,c,a,b) one has bcb = cac = c, ata = θ_x(b) = v ≤ c, ctc = θ_a(b) = u ≤ x, but ata = v ≠ c = θ_c(b) = btb. (This follows from the verbal description at line 1002 alone, so it is not a table typo; the table was also checked by computer: a projection algebra with (PC) violating exactly (A1), (A2), (X) and W_1 among (Sq), (A1), (A2), (X), (P1), (P2), (Q), (Ab), (Hm), (Tri), W_∞.) Hence:
   - line 1008 must read "𝔓_7: (A1), (A2), (X), and every (W_n)", and the last sentence of the proposition ("𝔓_7 satisfies everything except (A1), (A2) and the chain conditions") must be corrected;
   - line 555 "Table 1 lists, for each condition, the projection algebra that violates it and satisfies all the others" is false for 𝔓_7 (and already for 𝔓, which the proposition says violates (P2), (Q), (Ab)); say "the smallest algebra violating it";
   - **Theorem 1.4 and line 1192** claim that 𝔓^ch_n satisfies the eight wiring conditions "for every n". Since 𝔓^ch_1 ≅ 𝔓_7 (line 1153), this is false for n = 1 (it violates (A1) = (W_1), (A2), (X)); also (W_0) is undefined. By computation 𝔓^ch_2, 𝔓^ch_3, 𝔓^ch_4 satisfy all nine conditions and (Tri). *Fix:* "for every n ≥ 2" in Theorem 1.4, in the intro paragraph (line 92) and at line 1192 ("by direct computation also for 2 ≤ n ≤ 4"). The other eight witnesses check out: 𝔓 violates exactly (Sq), (P2), (Q), (Ab); 𝔓_8^1 (Hm) [and (Hm')]; 𝔓_8^2 (P1); 𝔓_8^3 (A2); 𝔓_8^4 (P2), (Q); 𝔓_8^5 (Q); 𝔓_8^6 (Ab); 𝔓_8^7 (X); all satisfy (PC), (Tri), W_∞; the listed violating instances are correct.

5. **Lemma 2.6(b), line 228: type (iv) is ambiguous, and the converse of (b) is used but not stated.** "(iv) K is a single block of both p and q" overlaps with (i) (common T-block) and with (ii)/(iii) (a T(p)-block that is an N(q)-block); the proof (line 236) produces (iv) only when U_K = L_K = ∅, and later text reads (iv) as "common N-block" (lines 605, 899). The parenthetical "nor of type (iv) (B meets supp p)" at line 236 is only valid with that reading. The *converse* of (b) — if every class is of one of the four types then pq = qp — is needed in Step 3 of Theorem 5.3 (line 649, proved there in a parenthesis), in Lemma 6.1 (line 1060) and in item A1. *Fix:* write (iv) as "a single N-block of both p and q" and state (b) as an "iff", moving the parenthetical of line 649 into Lemma 2.6.

6. **Lemma 7.4(c), line 1302: degenerate instances not covered.** "By (PC) the tree of a,b differs from that of c,d" presupposes a ≠ c and b ≠ c (matched pairs may be equal). If a = c the hypotheses force b = c and the instance is trivial, likewise b = d; the lemma is correct, but the proof should say so (as the proof of Theorem 7.3 does for c = d).

7. **Theorem 5.3, Step 2, line 647:** "every block of a, of c and of x lies inside supp y or is an N(y)-block" is not what Lemma 2.6(b) gives for a and c (a T(a)-block may lie strictly inside an N(y)-block, type (iii)). The statement is true because y commutes with a and c and a ⋈ c, by Lemma 5.2 (it is re-proved in Step 3). *Fix:* cite Lemma 5.2, or write "or inside an N(y)-block". The same sentence at line 748 (Theorem 5.8) is correctly justified by Lemma 5.2.

8. **Theorem 5.8, Step 4, line 756:** the parenthetical for the case "no block of 𝓕 meets supp b" is confused (a T(a)-block A_i = B_i ⊆ Y met by 𝓕 would make 𝓕 meet supp b). Since supp a = supp e ∪ ⋃_{i∉I} A_i ⊆ supp b (Step 2), in this case 𝓕 meets no T(a)-block and the claim is vacuous; replace the parenthesis by this reason.

9. **Theorem 1.1, second sentence, rests on Remark 3.2 (lines 343–351)**, where pqr ≠ pr is asserted without computation and "𝓜[ℤ_2;3,3;P] with p_12 ≠ 1" is not explained. Verified by computation: p ⋈ q ⋈ r ⋈ p, pqr ≠ pr, the generated *-subsemigroup has 18 elements of rank 2, 9 idempotents, 3 projections, and is not orthodox. Since the sentence is part of a main theorem, give the middle-layer computation of pqr and pr, or downgrade the sentence to a remark.

10. **Theorem 5.3, Step 5, line 661:** "a T(c)-block lies in some V_k" uses that no T(c)-block lies in an N(x)-block, which follows from Step 3 together with Step 4(d) (every Ñ-block is an N(c)-block); say so, since Step 5 precedes the collecting Step 6.

Everything else checked in the listed sections is correct (checklist at the end).

---

## B. Inconsistencies (notation, references, statements vs proofs)

1. **Theorem 1.2 vs Theorem 4.7(b).** Theorem 1.2: "For every set X … (D_E) holds in P_X iff E is not a star"; Theorem 4.7(b) proves it for |X| ≥ 2. For X = ∅ every (D_E) holds trivially; for |X| = 1 the counterexample of Theorem 4.5(b) still works (F = {1,1'}, e = {1},{1'}). *Fix:* "for every nonempty set X" in 1.2, and |X| ≥ 1 in 4.5(b)/4.7(b).

2. **Line 90:** "the others have up to seven variables" — the eight conditions have at most six ((Q): 4+2, Table 1); seven occurs only in (E_1).

3. **Line 92:** "a chain c ∼ x_1 ∼ … ∼ x_n ∼ b of *pairwise* commuting projections" — only consecutive members commute (Section 6.1).

4. **Theorem 1.4, line 118:** "(W_{n-1})" undefined for n = 1, and the claim fails for n = 1 (A4). Theorem 1.5 says "X finite" while Theorem 6.11 says "PA(P_X)" without restriction; the proof gives both (the maximal subalgebras embed in finite PA(P_m)); make the statements agree.

5. **Proposition 5.21, line 1007:** for 𝔓 no (Ab)-instance is given ("(a,c,b,d) as named" only covers (Sq)/(P2)/(Q)). A valid instance is (a,c,b,y,z) := (b,c,a,d,a) (or (c,b,d,a,d)); for (P2)/(Q) name the auxiliary x = w (and y = w or y = b).

6. **Line 969 (Remark 5.19):** "\Kzero$''$" — leftover research label K0''; should be \Hmp.

7. **Line 542:** "consequences of (Q) and (A2) respectively (Corollaries 5.5 and 5.13)" — with "respectively" the corollaries are in the wrong order (5.13 gives (Sq), 5.5 gives (A1)).

8. **Lines 1047 and 1153:** the order-9 candidates, and the fact that 𝔓^ch_2 is one of them, are in Section 8 (line 1372), not Section 9 ("Section~\ref{sec:open}"); Section 9 has only the three open ones.

9. **Letters reused with a different meaning.**
   - Proposition 5.11 (line 850): "e" is an index while e = xa is the auxiliary of Step 1 of the same subsection (acknowledged, but a proof that cites "Step 1" should not do this); rename the index.
   - Theorem 5.3, line 626: m := xy, while m = rk a is global notation (line 286).
   - Ñ is an N(x)-block inside supp y in Theorem 5.3 and an N(c)-block inside supp x in Theorem 5.8; both are declared local, but consecutive proofs should not swap the meaning of the same symbol.
   - Section 4 (line 477) uses u_i := a_i z a_i and Section 7 uses u for a vertex, while u = θ_a(b) is reserved (line 288); Lemma 6.1 uses B for a block while the B_i are the T(b)-blocks.
   - Line 621 declares e,f local to Theorem 5.3 (e = ya, f = xc); in 5.5 e = xa, f = xc; in 5.6 e = xa. Each proof declares its letters, but a one-line table of local letters at the start of Section 5 would help.

10. **Line 310:** "In P_X the down-set ↓p depends only on rk p" — its *size* does.

11. **Line 1372, order-9 counts:** 81 259 − 1 227 = 80 032 extensions with (PC), (Sq), (A1) of embeddable order-8 algebras, versus 80 039 such algebras in total (line 984). The difference (7 algebras all of whose maximal-element deletions are non-embeddable) is consistent but should be explained; the argument "every order-9 algebra violating (Sq) or (A1) contains one of the nine" also needs the remark that an algebra all of whose maximal deletions are non-embeddable contains a minimal non-embeddable subalgebra of order 8 (Theorem 5.22).

12. **Proposition 6.9, line 1166:** "the identifiers of (a,c) are c, the x_i and the bottoms" — a is also an identifier (θ_a(a) = θ_a(c) = a); it commutes only with itself and d, so the argument is unaffected, but the list should be complete.

13. **Remark 7.5(2), line 1264:** "for 𝔔 with ⊥ injective it uses |X| = 15" — 𝔔 (Definition 7.2) has the non-injective colouring and is non-embeddable; say "for Q(a−c−b−d, ⊥) with ⊥ injective".

14. **Type references in the ported proofs:** every "type (i)–(iv)" in 5.3 (lines 647, 649, 661), 5.5 (748), 5.6 (797), 5.7 (899, 901), 5.8 (939–947), 6.1, 6.3 was checked against Lemma 2.6(b) with the stated (p,q): all correct. The letters e, f in 5.3, 5.5, 5.6 are used consistently with their declarations; u, v do not occur in those three proofs.

15. **Figure 2 vs Section 5.1:** all eight diagrams agree with the displayed formulas (hypotheses, half-matched ends, labels u, v). Table 1 agrees with Proposition 5.21 and Section 5.9 except for the "satisfies all the others" sentence (A4). All `\ref`s point to results of the right kind (checked against the `.aux`). The main theorems 1.1–1.7 are implied by the later results except for the points in A4, A9, B1, B4.

---

## C. Presentation

1. Line 88: the `\todo` on the attribution of (PC) must be resolved; together with A1, state and prove (PC) for P_X and attribute it.
2. Line 1035: "Prover9 (M. Kinyon) derives …" — self-attribution by the author; drop the parenthesis.
3. Research-notes residue: line 618 ("Most of the algebraic part was found with Prover9, and the combinatorial statements were found by testing candidates…"), line 776 ("were found and checked on all instances … before being proved"), Remark 5.14(2) ("an earlier proof of (Sq) handled them by a finite computer check"), Remark 5.16 ("The test exposed a gap in a first version of Step 5"), line 1181 ("the tables were verified by computer for n ≤ 7" — a proof is given), line 1192 ("explains why the family was found late"). Section 8 is the natural home for the methodological remarks; the "gap in a first version" sentence should go.
4. Remark 5.14(1): make clear that the unverified identity θ_y(d) = θ_y(b) is not used (it says so, but after "verified … countermodels of order 6" the reader may doubt).
5. Section 5.1, line 553: (E_1), (E_6) are mentioned before they are defined (Remark 5.23); add a forward pointer.
6. LaTeX: amsart warns that the abstract should precede `\maketitle` (line 67); `\scriptsize` inside `gather*` (line 986) gives "Command \SMALL invalid in math mode"; overfull boxes at lines 106–107, 337–339, 852–853, 1046, 1056–1057; `\date{Draft of \today}` and the `\todo` macro are draft-only.
7. Line 1002: "(so far the projection algebra of …)" — "so far" is informal; say "the algebra without x is …".
8. Definition 6.8: the left/right description of θ_{x_i} is correct but hard to parse; a small picture of the chain with the e_i between consecutive members would help.
9. Line 1192: "(which have at most seven variables) for n ≥ 5" — six variables, so n ≥ 4; adjust with A4.
10. Lemma 2.6(b) proof, line 236: the final sentence becomes clean after the fix in A5.

---

## Checklist of what was verified (correct unless listed above)

- Section 2.1: axioms (1)–(2) and their θ-form; Lemma 2.1; idempotence of pq; Lemma 2.3 (both identities); Proposition 2.4 (all implications, incl. fg = f = g); line 216.
- Section 2.3: Lemma 2.6 (a), (b) incl. the final sentence, (c) and its converse; Lemma 2.7(b) and 2.7(a) ⇒; Lemma 2.8 (transport); Lemma 2.9 (counting invariant, δ and δ′, and the xy corollary); the notation paragraph at line 286.
- Section 2.4: Lemma 2.10 (a)–(d).
- Section 3: Theorem 3.1 in full (π_i is a partition, φ(i,g,j)*, injectivity, both product cases incl. M_s and T_{l;j,t}); Remark 3.2 by computation.
- Section 4 (read, not refereed in detail): Lemma 4.1, Lemma 4.3, Lemma 4.4, Steps 1–3 of Theorem 4.5(a), the monotonicity argument of line 432, Theorem 4.5(b).
- Section 5.2: Lemma 5.1 (closing lemma); Lemma 5.2 (commuting auxiliary), including "every block of a lies in supp x or *is* an N(x)-block".
- Section 5.3: Theorem 5.3 Step 1 (i)–(vii), every identity; Steps 2–8 and the conclusion; Remark 5.4 (ab = acb); Corollary 5.5.
- Section 5.4: Theorem 5.6 Steps 1–5 (type T and type N) and conclusion; Remark 5.7(3).
- Section 5.5: Theorem 5.8 Steps 1–5.
- Section 5.6: Step 1 (the identity θ_{θ_r(p)}(θ_p(q)) = θ_r(θ_p(q)) and the reduction to x = e ≤ a), Step 2 (Π_1 = ε_e∨ε_d = ε_a∨ε_z, the (nh)/(h) dichotomy, π, |G| ≤ 2 and cross-wiring, the P_4 example by computation), Step 3 (∗) and (a)–(e); Steps 4–7 read, not independently re-derived; Theorem 5.12; Corollary 5.13 (both implications).
- Section 5.7: Step 1 of Theorem 5.15 in full (az = za = u, θ_b(y) = v, θ_u(y) = θ_u(c) = u, b ⋈ w, θ_w(f) = θ_z(f) = θ_b(f), b = w, θ_y(u) = θ_y(z)); the type references in Steps 2–4.
- Section 5.8: Step 1 of Theorem 5.17; Corollary 5.18; Remark 5.19 (modulo B6).
- Section 5.9: Lemma 5.20; the seven tables and 𝔓_7 are projection algebras with (PC) (computed); Proposition 5.21 except 𝔓_7 (A4); Theorem 5.22 and its counts (296/1671/10932, 9 = 1671 − 1662, 104 = 10932 − 10828); the descriptions of 𝔓_8^3 and 𝔓_8^7 at line 1002 against the tables.
- Section 6: the (W_∞) reformulation (line 1049); Lemma 6.1 up to A3; Corollary 6.2; Lemma 6.3; Lemma 6.4 (A), (M), (G2′); Theorem 6.5 (i), (ii), (8), (9), (G1), (G2); Theorem 6.6; Definition 6.8 (order 2n+5, the identities after it, 𝔓^ch_1 ≅ 𝔓_7 element by element); Proposition 6.9 (all five axioms, (PC), (W_{n−1}), ¬(W_n); confirmed by computation for n ≤ 4); Proposition 6.10 (all four embeddings block by block, incl. the switch of the R-pattern at index i that separates e_{i−1} from e_i when X_i is absent); Theorem 6.11.
- Section 7: Lemma 7.1 (associativity, involution, projections, (PC) ⇔ proper colouring); Definition 7.2 and the (Sq)-violation; Theorem 7.3 (iii)⇒(iv) incl. the induced-P_4 argument, and (iv)⇒(i) incl. the Claim and the products; Lemma 7.4 (associativity via f(q_k,r) = max(k,f(q,r)), θ formula, (a)–(d), modulo A6); Theorem 7.6 (p ↦ p̂, the semigroup embedding, |X|); Remark 7.7 (𝔓_9: 9 elements, 29-element semigroup, (PC), violates (Sq), θ_a(d) = m).
- Section 8: Proposition 8.1; the bound |S| ≥ |P(S)| + 2·#matched pairs; internal consistency of the order-9 counts (modulo B11).
