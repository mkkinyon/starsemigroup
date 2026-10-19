# Cold read of `paper/embedding.tex` (revision c186715, "finite versus infinite X")

Referee pass by a fresh reader (19 Oct 2026). Scripts in `review6/review-scripts/`
(`q_hotel.py`, `hinf_check.py`, `run_sq.py`, `hotel_Q_411.log`). Line numbers refer to
`paper/embedding.tex` at revision c186715.

## Headline findings

- **A1 (major):** the proof of (Q) (Theorem `thm:Q`) still uses pigeonhole counts in Step 4
  (line 857) and Step 7 (line 912), and in Prop. `prop:Qnh` (line 884). (Q) is in fact
  **false in PA(P_N)**: an explicit 1-periodic counterexample on points p_i, q_i, r_i, s_i, found
  with the repository's own `hotel_sat.py` and verified independently by hand and by code. The
  count-free part of the proof still gives theta_d(a) = d for every X, so (Q), (P2), (Sq) are
  *finitely valid* via `lem:descent`(b), which is all the census needs; validity of (Sq), (P2)
  for infinite X is now open. Abstract, Thm 1.3, lines 80/82/90/593/928 need rewording.
- **A2:** Remark `rem:hinf`'s "levels <= 4" check is unjustified as argued (the correct
  compression bound is 18 for the axioms, 25 for the hexagon); the claims are nevertheless
  true: axioms/(PC) verified to level 18, hexagon condition proved by hand.
- **A3-A6:** wrong "iff"/"that is" at lines 1258 and 1464 ((Ab) is already finitely valid);
  line 90 wrongly says (Hm') and (Hm) are equivalent in finite algebras; lines 80/82
  overclaim the non-finite-basis result for all P_X; Lemma `lem:psi` is announced as "will
  be used" but never used.
- All requested items were checked and found correct unless listed: `lem:psi`, `prop:phi0`
  (example re-derived; script agrees), `lem:count` structural form, `thm:K4` Step 4 and the
  final paragraph (no other finiteness in Steps 5-7), `thm:K0` Steps 1-7 and part (c)
  (identities confirmed with Prover9), Section 6 under the finite scope, `prop:chainwit`,
  the (H1) parenthesis, the `prop:Q1` display, the composition convention, the
  commuting-graph definition.

## A. Errors or gaps in proofs

### A1. (Q) uses counts and is false in PA(P_N)

Where finiteness is used:
- Step 4, line 857: "Consequently every hub G has E_G != empty, and pi is a permutation of
  the hubs." Steps 2 and 4 give an injection from the hubs with nonempty trace onto all
  hubs; that every hub has a nonempty trace is pigeonhole.
- Step 7, line 912: "sum_G |pi(G)| = sum_G |G|, so |pi(G)| = |G|".
- Prop. `prop:Qnh`, line 884: "tau is surjective, hence bijective" (G may be infinite).

Counterexample in PA(P_N) (points p_i, q_i, r_i, s_i, i >= 0):

    a:  T {p0,s0}, {q0}, {r0}, {p_i}, {r_i} (i>=1);      N {q1}, {s_i,q_{i+1}} (i>=1)
    b:  T {q_i} (i>=0), {s_i} (i>=1);                    N {p0,s0}, {r_i,p_{i+1}} (i>=0)
    c:  T {q0}, {r0}, {s0,q1}, {r_i} (i>=1), {q_i} (i>=2);  N {p0}, {p_i,s_i} (i>=1)
    d:  T {p_i} (i>=0), {s_i} (i>=1);                    N {q0,r0}, {s0,q1}, {r_i,q_{i+1}} (i>=1)
    x:  rank 0:  N {p0,s0}, {q0,r0}, {q1}, {p_i,r_i} (i>=1), {s_i,q_{i+1}} (i>=1)
    y:  T {q_i} (i>=1), {s_i} (i>=1);                    N {q0}, {p0,s0}, {r_i,p_{i+1}} (i>=0)

a |><| c |><| b |><| d, x <= a, theta_c(x) = theta_d(x), y <= b, y ~ a, theta_y(c) = y = theta_y(b);
but the class {q0, r0} of e_a v e_d contains two T(a)-blocks and no T(d)-block, so
theta_a(d) != a (theta_d(a) = d holds). In the proof's terms the hubs are G_0 = {A_q0, A_r0},
G_i = {A_pi, A_ri}, with pi(G_i) = G_{i-1} and E_{G_0} empty: Hilbert's hotel on the hubs.

Fix (makes (Q) finitely valid): the count-free parts give theta_d(a) = d for every X
(plain classes contain no T(d)-block; in non-hub classes (a), (b), (c) give that every T(d)-block
is attached to some A_i and no rho-class contains two T(d)-blocks; in hub classes Claims 1 and
2 give the same). Then a |><| d follows for finite X by rank, and for a finite subalgebra by
Lemma lem:descent(b) applied to theta_a(d) <= a, theta_a(d) |><| theta_d(a) = d |><| b |><| c |><| a.
The rigidity arguments inside (a), (b) of prop:Qnh and Claims 1-3 of prop:Qh were checked for
their logical structure only.

Consequences: thm:Q, thm:main-wiring, abstract, lines 90, 593, cor:QS (validity part) must be
reworded; (P2), (Sq) lose their proof for infinite X (open; no hotel for (Sq) with three fibres,
`Sq 3 1 1` UNSAT); thm:census, prop:witnesses, thm:graphsg (an instance of (Sq) in V u B lies
in a subalgebra of at most eight elements), thm:layered survive with finite validity.

### A2. Remark rem:hinf: level bound

A simultaneous shift of levels normalises the minimum level to 0 but does not bound the
maximum; gap compression does: with k chain-valued variables and term depth d, levels can be
compressed to <= (k-1)(2d+1) without changing any comparison: 18 for the axioms, 25 for the
hexagon condition. Axioms and (PC) verified to level 18 (`hinf_check.py`); the hexagon
condition can be proved by hand: in a hexagon configuration either all six elements are low
(then w = z) or all are chain elements, the a_i are e's with pairwise distinct indices, the
b_i are f's, and the six matchings give N_1 = M_2 = N_3 = M_1 = N_2 = M_3 and N_1 = M_3 + 1,
a contradiction. Triangle instance and the sentence about the walk are correct.

### A3. Lines 1258, 1464: "iff" should be "if" (P^ch_n embeds => W_n not finitely valid; converse
not argued); "they" at 1464 wrongly includes (Ab), which is finitely valid.

### A4. Line 90: (Hm') is not equivalent to (Hm) in finite algebras (an order-9 algebra
satisfies (Hm) and not (Hm')); write "which implies it".

### A5. Lines 80, 82: overclaim the non-finite-basis result for all P_X; the proved version is
for the finite partition monoids.

### A6. Line 327: Lemma lem:psi "will be used" but is never used; "two of our conditions" (only
(Hm) shown to fail; now (Q) as well).

## B. Inconsistencies

1. Line 357: "the matching A_i <-> B_{i+1} through c" is wrong with the paper's indexing (through
   c it is A_i <-> B_i; the pairing through e_a v e_b is A_i <-> B_{i+1}, an injection missing B_0).
2. Validity levels used consistently except at lines 80/82, 1258, 1464 and for (Q), (P2), (Sq).
3. Line 1440: cite Theorem thm:K0(a) for the validity of (Hm'), not cor:K0pp.
4. Line 1089: "finitely valid (Section subsec:rank)" should cite the theorems.
5. Line 604: (E6) needs only (PC)+(Ab); (E1) is derived at the level of finite partition monoids.
6. Line 1033: Mace4 searches bounded sizes; "at any size" is what cor:K0pp proves.
7. thm:K4 Step 5(C), line 964: "of the second kind" undefined there.
8. thm:Rp "followed by a count" / "Step 8: counting": not a count; rename. "n + t distinct
   classes" in thm:K4 Step 4 reads like a count.
9. thm:main-wiring and Table 1 vs prop:witnesses: consistent; first sentence needs rewording
   after A1.
10. thm:graphsg line 1312: (ii)=>(iii) uses (Sq) on an eight-element subalgebra; say so.
11. q:infinite: open list should be (Ab), (Sq), (P2), chain conditions.

## C. Presentation

1. A status table of the ten conditions in Section 2.5.
2. Remark after thm:nfbW and q:infinite overlap.
3. rem:hinf: replace the shift sentence by the compression bound or the hand proof.
4. `python3 -I hinf2.py` fails (imports termeval from its directory); use `python3 hinf2.py`.
5. The \todo at line 88 and \date{Draft of \today} are still open.

## D. Checklist (verified and found correct)

Axioms and theta-form, composition convention; lem:comm, lem:friends; prop:Q1 incl. the display;
lem:count structural form and consequences; lem:psi; prop:phi0 (hand and script); lem:descent;
(H1) parenthesis and semilattice example; rem:hinf definition, chains, matchings, triangle
instance, walk; Section 5.1 displays vs figure and table; thm:K4 Steps 1-7 (new Step 4 and final
paragraph; no further finiteness); thm:K0 Steps 1-7 and (c) (Prover9 identities); thm:census
proof; Section 6 preface, commuting graph, lem:radius, thm:Wn, thm:endstep, prop:chainwit,
thm:nfbW, line 1260; introduction theorems except (Q); other proofs scanned for hidden
finiteness: thm:DE, thm:Rp, thm:V, thm:P1, cor:R, thm:K0(a): none.

Computations: hotel_phi0.py; hinf2.py 4 and hinf_check.py 18 12; Prover9 identities; hotel_sat.py
extended with (Sq), (P2), (Q): Q 4 1 1 SAT (3 min), Q 2 1 1 UNSAT, Sq 3 1 1 UNSAT; Sq 4 1 1,
P2 4 1 1, P2 3 1 1, Q 3 1 1 unresolved in 25 min.
