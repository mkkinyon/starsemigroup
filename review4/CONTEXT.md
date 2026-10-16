# Cold read request: Theorem 5.50 (K0 holds in every partition monoid)

You are an independent referee. Read `thmK0.tex` (the theorem and its proof, with the post-proof
paragraph) and `lemPX.tex` (Lemma 1.1 = `lem:PX`, the only facts about partition monoids used).
Write your report to `REPORT.md` in this directory.

## Setting (all you need)
P_X = partition monoid on a finite set X. A projection p of P_X is a pair (ε_p, T(p)): an equivalence
relation ε_p on X (its blocks) and a set T(p) of "transversal" blocks (the rest are N(p)-blocks);
supp p = union of the T(p)-blocks; rk p = |T(p)|. θ_p(q) := pqp (notation in Prover9 files: X*Y = θ_Y(X)).
q ≤ p iff θ_p(q) = q. p ~ q means pq = qp. p ⋈ q ("matched") iff θ_p(q) = p and θ_q(p) = q.
(Q1) (valid in P_X): r ≤ p, r ≤ q ⇒ pq = qp; for commuting projections pq = θ_p(q) = θ_q(p).
Axiom valid in every projection algebra: θ_p(θ_q(p)) = θ_p(q); also θ_p(θ_p(q)) = θ_p(q).
Lemma `lem:friends`: θ_p(q) ⋈ θ_q(p) for all projections p, q (valid in every regular *-semigroup).
Theorem thm:R's notation: for a ⋈ c ⋈ b with T-blocks A_i, C_i, B_i (i = 1..m), the classes of
ε_a ∨ ε_c meeting supp a ∪ supp c are Γ_1..Γ_m with Γ_i ⊇ A_i, C_i (exactly one T(a)- and one
T(c)-block each, Lemma 1.1(c)); likewise Δ_i ⊇ C_i, B_i for ε_b ∨ ε_c. The indexing of the B's is
through the C's (B_i is the T(b)-block in the Δ-class of C_i).

The condition K0: a ⋈ c ⋈ b, yc = cy, θ_y(b) = θ_b(a), θ_b(z) = b, θ_z(a) = θ_z(b), θ_y(z) = θ_a(b)
⇒ a ⋈ b. It is verified in P(P_m) for m ≤ 6 (SAT) and on 1.7 million instances of P(P_5)
(`../embed/pa8/k0/k0inst5.log`). The claimed hand proof is for every P_X.

## What to do
1. Check every step of the proof for correctness and completeness, in particular:
   - Step 1: the derivation of θ_a(z) = a from θ_z(a) = θ_z(b) and θ_b(z) = b (rank count).
   - Step 2: the two "no type (iii)" claims (every T(a)-block and every T(b)-block meets supp y),
     and the listed consequences; the identification of the U_j with the M_j ∩ supp a.
   - Step 3: the classes K_j, K_F of ε_y ∨ ε_z.
   - Step 4(a)-(d): crossing blocks, non-crossing blocks in one cell, N(y)-blocks and z-blocks in one
     cell, the connectivity argument.
   - Step 5: ε_a ≤ ε_b ∨ ε_z, in particular the diagonal argument A_i ⊆ D_i ⊆ L'_i.
   - Step 6: the contradiction.
   Look for gaps of the kind found in the K4 proof on 16 Oct (a count that is a tautology; a claim
   that silently assumes what is to be proved; a case not covered, e.g. a T(y)-block meeting an
   N(a)-block AND a T(a)-block, blocks of y containing points outside supp a ∪ supp b ∪ supp c, a
   crossing block meeting an N(b)-block, empty diagonal cells, m = 1, etc.).
2. Verify the intermediate claims numerically and independently of the author's script
   (`../embed/pa8/k0/k0claims.py` is the author's; `../review3/review-scripts/pm.py` is an
   independent partition-monoid multiplication by union-find, `../review2/review-scripts/fast.py` the
   bit calculus: projection = (tuple of block bitmasks, T bitmask); `fast.theta(p,q)` = θ_p(q),
   `fast.join(p,q)` = classes of ε_p ∨ ε_q as bitmasks, `fast.commute`, `fast.matched`,
   `fast.projections(n)`). Instances of K0 in P_4 are in `../embed/pa8/k0/k0inst4.pkl` (list of dicts
   with keys a,b,c,y,z), in P_5 in `k0inst5.pkl` (1.7 M; sample it). Put scripts in
   `review-scripts/` here. Run with `python3 -I` is NOT needed (these are the project's own files).
   Test at least: the no-type-(iii) claims; "every N(y)-block is an N(a)- and N(b)-block";
   crossing blocks ⊆ ∪(A_i ∩ B_i ∩ C_i); non-crossing T(y)-blocks and N(y)-blocks in one cell;
   ε_a ≤ ε_b ∨ ε_z; and, for the dropped-hypothesis test, that each of these fails when the
   hypothesis the proof uses for it is dropped (so the proof cannot be using less than it says).
3. Report: verdict (proof correct / gap at step ... / unclear at ...), each issue with the exact
   sentence quoted, and the numerical results with instance counts. Be concrete and brief; do not
   rewrite the proof. If you find a gap, say whether you see a repair.
Budget: keep computations under ~15 minutes of CPU total; the machine has 2 cores and another job
is running.
