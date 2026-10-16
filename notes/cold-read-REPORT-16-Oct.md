# Cold read of 16 Oct 2026: Theorem 5.49 (K4 in every partition monoid), Section 5.20, and the corrections of 15 Oct

Reader: a semigroup theorist / universal algebraist with no prior exposure to the project. Files read: CONTEXT.md;
notes-embedding.tex (Section 1 with Lemma 1.1 and its proof; Lemma "lem:friends" (theta_p(q) |><| theta_q(p));
Theorem 5.16 and its proof, for the notation A_i, C_i, B_i, Gamma_i, Delta_i; Theorem 5.23 Step 1; Section 5.19(a)
with the closing lemma; all of Section 5.20 (subsec:count) and Section 5.21 (subsec:K4); Section 7, Questions 2 and
4); status-table.tex; conditions.in; the code directory (fast.py, k4chk.py, k4drop.py, k4rec2.py, k4sat.py, qi.py,
pa_sat.py, k4.pf2, rpp_vs_chain.pf, k6_vs_chain.pf, k0_implies_e1_README.txt); previous-cold-read-11-Oct.md for
style only.

Everything I checked by computer was checked with my own scripts (directory `review-scripts/`, list in Section 8),
on top of the previous reviewer's block calculus `code/fast.py`, which I first validated independently against
direct partition-monoid multiplication (union-find on three layers) for all 94 x 94 products of P(P_4) and all
22 x 22 of P(P_3): no discrepancy in `theta` or `commute` (`pm.py`).

---------------------------------------------------------------------------------------------------------------

## 0. Summary of verdicts

**Item 1, Theorem 5.49 (K4 in every P_X): not proved as written.** Step 1 and Steps 3-6 are correct, but Step 2
rests on the sentence "the left side is n", which is false in general: the counting identity it is drawn from
(Lemma 5.40 for the pair (b,c) and v <= b) is a tautology for every v <= b, and the statement it is used to
establish ("every B_i lies in some S_j", equivalently supp theta_b(a) = supp b, equivalently supp a <= supp z) is
of full strength: it fails when any one of the five y/z-hypotheses is dropped, while the argument given uses only
a |><| c |><| b and theta_z(c) = b (never theta_a(y) = a). A concrete instance of P_4 satisfying all of Step 2's
inputs and violating its conclusion is given in 1.3. What the proof as written establishes is "K4 given
supp a <= supp z". The gap is, I believe, **repairable**: Section 1.6 gives a short argument for the missing
statement (a "bright/dark class" invariant along a chain in Gamma_1) using only facts already established in
Steps 1, 3, 4 and Lemma 5.40; if the authors confirm it, the theorem stands. Until then K4, (E_6) and the
minimality of P_8^6 must be reported as *verified for m <= 7* (the authors' SAT); my own SAT run adds m = 8 for the
missing statement (hence, with Steps 3-6, K4 in P(P_8)).

**Item 2, "K4: reductions, and the case z = b"; k4.pf2:** the algebra is correct (rank lemma, the identities, the
equivalence of K4 with "hypotheses imply theta_a(theta_y(b)) = a"); k4.pf2 assumes exactly the seven stated
equations in the x*y = theta_y(x) convention and nothing else (not even (Q1)). But "what is proved about the
geometry" asserts supp a <= supp z without proof, and "the case z = b" inherits the same gap: its argument treats
only "some I_j has two indices" and silently assumes that no T(a)-block lies in an N(z)-block, which with z = b is
not automatic (same P_4 instance). The "equivalent geometric forms" are asserted, not proved, and cannot be tested
in P(P_m), m <= 7.

**Item 3, Section 5.20 (Lemma 5.40, Cor. 5.41, Lemmas 5.42, 5.43, Theorems 5.44-5.48): correct** as far as I can
check (hand verification of every step of 5.40-5.45; the two Prover9 files for 5.47 have exactly the right
hypotheses; 5.48 is cited only). One wording slip in Lemma 5.42's strictness clause; "outer block" used in the
proof of Theorem 5.44 before it is defined (in 5.21). Both harmless.

**Item 4, Theorem 5.23 Step 1(iv): correct.** Each identity re-derived by hand; the false principle hh* |><| h*h is
used nowhere else (the two other places that look similar, Lemma "friends" and Step 2(b) of Theorem 5.16, use
correct arguments).

**Item 5, status-table.tex and conditions.in:** consistent with the notes *as the notes stand*, but the notes
overstate: the rows/comments saying "K4 proved, (E_6) proved, P_8^6 minimal non-embeddable" must revert to
"verified m <= 7 (SAT)" unless the repair of 1.6 is accepted. Several stale sentences remain (Question 7.(2),
7.(4), the comment block and footnote of the status table), listed in Section 5.

---------------------------------------------------------------------------------------------------------------

## 1. Theorem 5.49: K4 holds in every partition monoid

### 1.1 Structure of the proof as I read it

Hypotheses: a |><| c |><| b, theta_a(y) = a, b <= z, yc = cy, theta_z(y) = theta_b(a) =: v, theta_z(a) = theta_a(b) =: u.
Notation: m = rk a = rk c = rk b, n = rk u = rk v; A_i, C_i, B_i matched T-blocks, Gamma_i, Delta_i the classes of
eps_a v eps_c, eps_b v eps_c containing C_i. The proof shows n = m through the following chain of statements:

1. (Step 1) algebraic consequences: az = za = u, theta_b(y) = v, u |><| v, theta_u(y) = theta_u(c) = u, theta_z(c) = b
   (Prover9, k4.pf1, not available to me), theta_y(u) = theta_y(z).
2. (Step 2) eps_u = eps_a v eps_z with T(u)-blocks the type-(i) classes K_1..K_n; the classes D_j of eps_a v eps_b
   containing K_j, S_j = D_j cap supp b the T(v)-blocks, I_j = {i : A_i <= K_j}; **(claim) every B_i lies in some
   S_j; (claim') supp a <= supp z (no class of type (ii))**; then: N(z)-blocks = common N-blocks of a, b, z ("outer"),
   D_j <= supp z, A_i <= K_j iff B_i <= S_j.
3. (Step 3) eps_z v eps_c = eps_b v eps_c, Delta_i cap supp z = B_i; eps_z v eps_y = eps_b v eps_y, the classes K'_j
   with K'_j cap supp z = S_j; the four types of y-blocks relative to c.
4. (Step 4) E_i (classes of eps_a v eps_y at A_i), M_j (classes of M = eps_a v eps_z v eps_y at K_j), M_j = union
   of E_i over I_j by a count, and every T(y)-block of M_j lies in K'_j (from theta_y(u) = theta_y(z)).
5. (Steps 5-6) if |I_j| >= 2 for some j, three labels (sigma, gamma, lambda) on the points of K'_j form a connected
   set in a graph L whose relevant components are the sets C_s; a chain in Gamma_i from A_i to the a-block of a
   point of B_i (i in I_j, i != s) cannot end in E_s: contradiction. So |I_j| = 1 for all j.

Since sum_j |I_j| = m is exactly what (claim') provides (every A_i lies in some K_j), the final step "hence n = m"
needs (claim'). Both (claim) and (claim') are established in Step 2 by a counting argument, and that argument is
wrong (1.3). Everything else holds (1.2, 1.4).

### 1.2 Step 1: verified

All identities re-derived by hand in the projection-algebra axioms PA2-PA5 of k4.pf2 (I checked the axioms
themselves against regular *-semigroups: PA5 is pq pq = pq, i.e. g = gg*g for g = pq).
- u <= a, u <= z, so az = za = u by (Q1) (reformulation (4) of Prop. 2.1); theta_a(z) = theta_z(a) = u holds even
  without (Q1), cf. step 71 of k4.pf2.
- theta_b(theta_z(x)) = theta_b(x) for b <= z: theta_b = theta_z theta_b theta_z (PA4) and PA2.
- u |><| v is Lemma "friends" (theta_p(q) |><| theta_q(p)), whose proof (pq idempotent, p(qp)^4 = pqp) is right.
- theta_u(y) = theta_u(theta_a(y)) = theta_u(a) = u, theta_u(c) likewise: correct.
- The identity theta_p(theta_{theta_q(p)}(x)) = theta_p(theta_q(x)) is PA5 with PA4 inside, as stated; the two
  instantiations give theta_y(theta_b(x)) = theta_y(theta_z(x)) for all x (also verified for all x in P(P_4) on all
  instances), and x = a, PA3 give theta_y(u) = theta_y(z). Correct.
- theta_z(c) = b: cited (k4.pf1 not available). Consistent with the computations: it holds on all 37,324 instances
  of P(P_4), and on every P_4 instance in which one of theta_a(y) = a, theta_z(a) = u is dropped (5,062 and 336,933
  instances), i.e. it depends exactly on the inputs the text lists (b |><| c, b <= z, yc = cy, theta_z(y) = v) and
  fails only when one of those is dropped. Nothing else in the proof depends on k4.pf1 except through this identity,
  which is used in Step 3 (eps_z v eps_c = eps_b v eps_c, Delta_i cap supp z = B_i) and in Step 2 (Omega = eps_u v eps_c,
  "a block of c in Delta_{i'} meets supp z only inside B_{i'}").

### 1.3 Step 2: the gap

**Location.** Step 2, the sentence beginning "Next, every B_i lies in some S_j: apply Lemma 5.40 to the pair (b,c)
and v <= b (both identify b with c); the delta' half gives |eps_v|_{supp b} = |eps_v v eps_c|_{supp c}, the left
side is n."

**What is wrong.** |eps_v|_{supp b} counts the blocks of v = theta_b(a) inside supp b. By Lemma 1.1(a) these are the
sets D cap supp b for *all* classes D of eps_a v eps_b meeting supp b: the T(v)-blocks S_j (n of them, D = D_j) *and*
the N(v)-blocks inside supp b (D meeting supp b but not supp a). So the left side is n + n', where n' is the number
of N(v)-blocks inside supp b, and n' = 0 is exactly the statement being proved (an N(v)-block inside supp b is a
nonempty union of T(b)-blocks). The right side |eps_v v eps_c|_{supp c} is also n + n': a class of eps_v v eps_c
meeting supp c is the union of the Delta_k over the T(b)-blocks B_k lying in one v-block inside supp b (a c-block of
Delta_k meets supp b only inside B_k, Lemma 1.1(c)), so these classes are in bijection with the v-blocks inside supp b.
The identity of Lemma 5.40 for the pair (b,c) and v <= b is therefore a tautology (and so is its delta half), and the
sentence "If some B_i lay in an N(v)-block, the class of eps_v v eps_c containing Delta_i would be a further one" is
not a contradiction: that further class on the right is matched by the further block on the left.

**A minimal illustration** (a |><| c |><| b only, which is all the sub-argument uses): in P_4, a = [0](1 2 3),
c = [0 1 2 3], b = (0)[1 2 3]; then v = theta_b(a) = (0)(1 2 3), n = 0, |eps_v|_{supp b} = 1 = |eps_v v eps_c|_{supp c},
and B_1 = {1,2,3} lies in an N(v)-block. Among the 31,142 triples a |><| c |><| b of P(P_4) the identity holds in all
of them and "every B_i lies in some S_j" fails in 6,100 (`claimtest.py`).

**An instance satisfying every input of Step 2 and violating its conclusion.** The inputs actually used in Step 2
are a |><| c, b |><| c, b <= z, theta_z(a) = u, theta_z(y) = v, yc = cy and theta_z(c) = b; the hypothesis
theta_a(y) = a is never used in Step 2. In P_4 take

    a = [0](1 2 3),   b = z = (0)[1 2 3],   c = [0 1 2 3],   y = (0 1 2 3).

All K4 hypotheses hold except theta_a(y) = a (theta_a(y) = (0)(1 2 3)); theta_z(c) = b, u |><| v, theta_u(c) = u hold.
Here n = 0 (there is no K_j and no S_j), |eps_v|_{supp b} = 1 (so "the left side is n" is false), B_1 lies in an
N(v)-block, supp a = {0} is not contained in supp z = {1,2,3} (the class {0} of eps_a v eps_z is of type (ii)), and
a |><| b fails. (`step2trace.py`: of the 5,062 P_4-instances lacking only theta_a(y) = a, 3,058 are of this kind,
and in all of them the first false sentence of Step 2 is "the left side is n".)

**How strong the missing statement is.** `dropmap.py` drops each K4 hypothesis in turn (as the authors' k4drop.py
does for a |><| b) and tests the intermediate statements of the proof. Entries: number of instances where the
statement FAILS / number of instances with the remaining hypotheses, in P(P_4):

| statement | -b<=z | -theta_a(y)=a | -theta_z(a)=u | -theta_z(y)=v | -yc=cy | full |
|---|---|---|---|---|---|---|
| a \|><\| b | 14802/14802 | 5062/5062 | 4104/336933 | 65442/567077 | 24228/338819 | 0/37324 |
| supp a <= supp z (claim') | 12102 | 3058 | 138996 | 59322 | 22440 | 0 |
| supp v = supp b (claim) | 11982 | 3058 | 3768 | 59442 | 22416 | 0 |
| supp u = supp a | 12102 | 3058 | 3840 | 59322 | 22440 | 0 |
| each Omega-class meeting supp c contains a K_j | 11958 | 3058 | 3696 | 58794 | 22368 | 0 |
| theta_z(c) = b | 14802 | 0 | 0 | 469032 | 164746 | 0 |
| theta_y(u) = theta_y(z) | 0 | 0 | 162142 | 454745 | 0 | 0 |
| eps_z v eps_c = eps_b v eps_c | 2988 | 0 | 0 | 315723 | 105453 | 0 |
| eps_z v eps_y = eps_b v eps_y | 2652 | 0 | 0 | 389680 | 0 | 0 |
| no T(z)-block meets two T(a)-blocks | 2700 | 2004 | 264 | 6120 | 1788 | 0 |

So (claim), (claim') and "supp u = supp a" need all five hypotheses (they fail when any one is dropped, in
particular when theta_a(y) = a is dropped), whereas theta_z(c) = b, theta_y(u) = theta_y(z) and the Step-3
identities depend exactly on the hypotheses the text says they do. No argument that ignores theta_a(y) = a can
prove (claim). This is the phenomenon the notes describe for K4 as a whole ("dropping any one hypothesis produces
counterexamples"), and it means that the real work of the theorem is in (claim)/(claim'), not only in Steps 5-6,
which deal with the case |I_j| >= 2 only.

**Downstream dependence.** (claim') is used to get: the right side n in the second count of Step 2 (so that the
number of type-(ii) classes is 0); supp u = supp a; "every class of eps_a v eps_b meeting supp a or supp b is some
D_j"; D_j <= supp z; A_i <= K_j iff B_i <= S_j; in Step 3 "K' cap supp z = S_j or an N(b)-block"; in Step 4 the
classes of M meeting supp a being the M_j and |eps_a| - |eps_u| = m - n; in Step 6 "P_k is an outer block" from
P_k cap supp z = empty; and the last line "hence |I_j| = 1 for every j, n = m". I checked that Steps 3-6 go through
with (claim) and (claim') assumed (1.4); I also checked that their main statements go through in a generalised form
without them (M_j = union of E_i over I_j, the T(y)-blocks of M_j lie in K'_j, |I_j| = 1 for every j), so that what
the proof as written establishes is: **under the K4 hypotheses, every K_j contains exactly one T(a)-block; hence K4
is equivalent to (claim')** (m = n + #{A_i in type-(ii) classes}).

### 1.4 Steps 3-6: verified, given (claim) and (claim')

I went through every sentence; the proof is correct and, as the notes say, uses each hypothesis where the computer
says it is needed. Points worth recording:

- Step 3. eps_b <= eps_z v eps_c from theta_z(c) = b, hence eps_z v eps_c = eps_b v eps_c (as eps_z <= eps_b): right.
  Delta_i cap supp z = B_i: right. eps_b <= eps_z v eps_y holds *without* (claim) (a b-block inside supp z lies in a
  v-block inside supp z, which is K cap supp z for one class K); "K' cap supp z is some S_j or an N(b)-block inside
  supp z" uses (claim). The types of y-blocks relative to c: right.
- Step 4. The count |eps_a v eps_y| - |M| = |eps_a| - |eps_u| from Lemma 5.40 applied twice (a identifies a with c
  and y with c; u <= a): right, and "no other class is merged" is right because the M-classes containing the E_i are
  at least n distinct ones. "The sets M_j cap supp y and K'_j cap supp y are the same family" from
  theta_y(u) = theta_y(z): right (both are the T-blocks of that projection; the families are disjoint and K'_j <= M_j).
- Step 5. The transitions of the labels on z-blocks and y-blocks are right. One inaccuracy: the components of L are
  the sets C_s (s in [m]), the clique {(i,i,empty) : i in [m]} (not single vertices: these are joined by edges of the
  first kind with k = empty), and single vertices; this does not affect the conclusion, since that clique has
  lambda = empty throughout and K'_j contains points with lambda = i and lambda = i'. The conclusion "its labels lie
  in one component C_s" is followed in Step 6 by "B_s <= K'_j", which needs s in I_j; this holds because a point of
  B_i (i != s) has sigma = s and sigma takes values in I_j, and should be said.
- Step 6. The induction is correct. In the third sub-case ("P_k is an outer block") the inference "P_k cap supp z =
  empty, so P_k is outer" needs (claim') (a T(a)-block in a type-(ii) class would also miss supp z); with (claim')
  it is fine, and only "N(z)-block, hence b-block" is used. The parenthetical "(and sigma-hat(P_{k-1}) not among the
  E_{i''}, i'' in I_j)" is neither needed nor part of the induction hypothesis. Notation clash: E_k denotes both the
  classes of eps_a v eps_y and the c-blocks of the chain; please rename the latter.
- Computer check of the label machinery (`k4verify.py`): on all 37,324 instances of P(P_4) and 242,694 instances of
  P(P_5) (|I_j| = 1 throughout), for every K'_j: sigma is well defined, labels are constant on outer blocks, of the
  form (i,i,k) on T(z)-blocks and (s,i,i) on y-blocks, no point has gamma = empty or lambda = empty, and (as the
  component structure predicts when I_j = {i}) every point of K'_j has gamma = lambda (35,149 + 264,633 classes;
  50,271 + 420,149 T(z)-blocks; 61,589 + 523,558 y-blocks; 9,348 + 92,306 outer blocks). All 65 statements of
  Steps 1-6 that I formulated hold on all these instances (logs in the script directory).

### 1.5 What is proved and what is not

- Proved (if the authors agree with 1.4): K4 holds in P_X whenever, under its hypotheses, every T(a)-block lies in
  supp z (equivalently every T(b)-block lies in supp theta_b(a)).
- Not proved as written: that this holds. Verified: for m <= 7 by the authors' SAT (through K4 itself), for m = 8 by
  my SAT run on the negation of (claim) (1.7).
- Hence, as the notes stand: K4 is "verified m <= 7, hand proof modulo one lemma"; (E_6) likewise; P_8^6 is a
  candidate. The abstract, Theorem 5.49's "Consequently", the (E_6) and K0-K6 rows of the status table, the comment
  at the top of the status table, the header of conditions.in and Question 7.(4) have to be read with this caveat,
  or corrected (Section 5).

### 1.6 A proposed repair (referee's; to be checked by the authors)

The missing statement can, I believe, be proved with the tools already in the proof. Call a class of
eps_z v eps_y **bright** if it contains a T(y)-block and **dark** otherwise. None of the facts (a)-(d) below uses
(claim) or (claim').

(a) [theta_z(y) = v, Lemma 1.1(a)] A class K of eps_z v eps_y meeting supp z meets it in exactly one block of v,
which is a T(v)-block if K is bright and an N(v)-block if K is dark. The T(v)-blocks are exactly the S_j = D_j cap supp b
(u |><| v, Lemma 1.1(c): a class D of eps_a v eps_b meeting supp a and supp b contains exactly one K_j). An
N(v)-block inside supp z is an N(b)-block or a set D cap supp b with D a class of eps_a v eps_b not meeting supp a;
either way it lies in one class of eps_a v eps_b, which I call D(K) for a dark class K meeting supp z. Also
eps_b <= eps_z v eps_y.

(b) [yc = cy, Lemma 1.1(b)] A block of c of type (iv) is a y-block, one of type (iii) lies in an N(y)-block; so these
lie in a single class of eps_z v eps_y. A block of type (ii) is a union of T(y)-blocks and one of type (i) lies in
supp y; so these lie in the union of the bright classes. Consequently *a c-block meeting a dark class lies inside it*.

(c) [a ~ z, Lemma 1.1(b)] Every a-block lies inside one z-block (the outer N(a)-blocks, and the T(a)-blocks inside a
type-(ii) class) or inside supp z (the T(a)-blocks of the K_j, the N(a)-blocks of type (iii)).

(d) [counts] Let Z^(1), ..., Z^(t) be the type-(ii) classes (N(z)-blocks which are unions of T(a)-blocks), and call
K_1, ..., K_n, Z^(1), ..., Z^(t) the *generalised K's*. Lemma 5.40 for (a,c), w = a, u <= a gives
|eps_u|_{supp a} = |Omega|_{supp c}, Omega = eps_a v eps_b v eps_c = eps_u v eps_c (Step 3). The left side is n + t.
By theta_u(c) = u every Omega-class meeting supp u contains exactly one K_j, and each such class meets supp c; so
exactly t Omega-classes meet supp c without meeting supp u; each of them contains a C_i, hence an A_i, hence a Z^(k);
by pigeonhole **every Omega-class meeting supp c contains exactly one generalised K, and a class containing a Z^(k)
contains no K_j**. Lemma 5.40 for (a,c) and (y,c) with w = a, u <= a (Step 4, verbatim) gives
|eps_a v eps_y| - |M| = |eps_a| - |eps_u| = m - n - t; the M-classes containing the E_i number at most n + t (M_j
contains E_i for i in I_j, the M-class of Z^(k) contains E_i for A_i <= Z^(k)), so they are exactly n + t distinct
classes, M_j = U_{i in I_j} E_i, M(Z^(k)) = U_{A_i <= Z^(k)} E_i, and M(Z^(k)) != M_j. In particular an a-block
inside supp z meeting some S_j lies in D_j <= M_j.

**Lemma.** Under the hypotheses of Theorem 5.49, t = 0 and every B_i lies in some S_j.

*Proof.* Suppose A_1 <= Z := Z^(1) (case I) or B_1 lies in an N(v)-block (case II). Let O be the Omega-class of C_1;
it contains Gamma_1 and Delta_1; in case I it contains Z and no K_j, in case II it contains K_j (A_1 <= K_j, which
we may assume after case I is excluded) and no other K.

Step A: D(B_1) does not meet supp a. In case II this is the definition (B_1 lies in an N(v)-block). In case I, if
D(B_1) met supp a it would contain some A_i; A_i <= K_{j'} would give D(B_1) = D_{j'} <= O, so K_{j'} <= O,
impossible; A_i <= Z^(k) would give D(B_1) = Z^(k), because a b-block which is a union of a-blocks is a class of
eps_a v eps_b by itself, and Z^(k) does not contain B_1. Hence, by (a), the class K' of eps_z v eps_y containing B_1
is dark, with D(K') = D(B_1); by (a) and (b), Delta_1 <= K' (b-blocks lie in single classes, c-blocks meeting K'
lie inside it), so C_1 <= K'.

Step B (case I only): the class of Z is bright. E_1 contains a T(y)-block H (theta_a(y) = a). Follow a chain
A_1 = P_0, Y_1, P_1, ..., Y_r = H in E_1 point by point and track the class of eps_z v eps_y of the current point:
a step inside a y-block, or inside an a-block lying in one z-block, keeps the class; a step inside an a-block
P <= supp z (an N(a)-block, since E_1 cap supp a = A_1 is not in supp z) joins two points of supp z, and neither lies
in a bright class: a bright class meets supp z in some S_j, and then P <= D_j <= M_j by (d), while P <= E_1 <= M(Z)
and M(Z) != M_j. So the class changes only between dark classes; since the chain ends in a bright class (at H), it
starts in one.

Step C: follow a chain A_1 = P_0, F_1, P_1, ..., F_t = C_1 in Gamma_1 (F's blocks of c, P's blocks of a, all inside
O) point by point and track the class K(x) of the current point. Invariant: *K(x) is bright, or dark and disjoint
from supp z, or dark, meeting supp z, with D(K(x)) = D_j* (in case I there is no j and the third alternative is
void). It holds at the start: in case I by Step B; in case II because x_0 in A_1 <= K_j <= supp z cap D_j. A c-step
preserves it by (b) (same class, or both points in bright classes). An a-step inside an a-block lying in one z-block
keeps the class. An a-step inside an a-block P <= supp z: the current point x is in supp z, so K(x) is not of the
second kind; if K(x) is bright, x lies in some S_{j'} by (a), so P <= D_{j'} <= O and K_{j'} <= O, which is
impossible in case I and forces j' = j in case II; if K(x) is dark then x in K(x) cap supp z <= D(K(x)) = D_j and
P <= D_j. In both cases the new point x' lies in P <= D_j cap supp z, so K(x') is bright or has D(K(x')) = D_j.
At the end the point lies in C_1 <= K', a dark class meeting supp z (in B_1) with D(K') = D(B_1) != D_j (Step A).
Contradiction. QED.

With the Lemma, Step 2 continues exactly as written from "Consequently supp u = supp a ...". The Lemma uses
theta_a(y) = a in Step B (case I) and all the other hypotheses through (a)-(d), in agreement with the dependency map
of 1.3. The facts (a)-(d) (and the closure facts used in Step A) were also checked numerically on the P_4 instances
with one hypothesis dropped (`repairfacts.py`): each holds on every instance that keeps the hypotheses it is derived
from (e.g. (b) on all instances lacking theta_z(y) = v, theta_z(a) = u, b <= z or theta_a(y) = a, and fails only
when yc = cy is dropped; the count statement of (d) fails only when theta_a(y) = a or theta_z(a) = u is dropped).

### 1.7 Computer checks

- `k4verify.py`: for each of the 37,324 instances of P(P_4) and for 242,694 instances of P(P_5) (every (b,z,y) for
  a random sample of matched pairs (a,c), 900 s), every intermediate statement of Steps 1-6 that I could formulate
  (65 statements, including the hypotheses and the conclusion) holds. This confirms Steps 1, 3, 4 and the label
  calculus of Step 5 on these instances; it cannot detect the circularity of Step 2 (all instances satisfy a |><| b).
- `claimtest.py`, `dropmap.py`, `step2trace.py`: as reported in 1.3.
- `k4gap_sat.py`: SAT search (pysat/Cadical, through the authors' pa_sat.solve and the partial table of qi.table,
  which I checked encodes exactly the K4 hypotheses; rows printed in the log) for the K4 hypotheses together with
  the negation of (claim), "some point of supp b is outside supp theta_b(a)", with a sound symmetry-breaking
  (points ordered by the labels of element 0). UNSAT for m = 3, 4, 5, 6 (<= 2 s each), m = 7 (52 s), **m = 8
  (1,574 s)**; m = 9 was still running when this report was written (log gap_m9.log). So the missing statement
  holds in P(P_8), one step beyond the authors' evidence for K4; with Steps 3-6 this gives K4 in P(P_8).

---------------------------------------------------------------------------------------------------------------

## 2. The paragraph "K4: reductions, and the case z = b" and k4.pf2

*Algebra.* All identities verified by hand: a |><| r, v |><| r', u |><| v (Lemma "friends"); theta_r(b) = theta_r(r')
(r <= y); theta_r(r') = theta_r(z) (theta_y(z) = theta_y(v) = theta_y(b) = r' by PA3 twice); theta_r(r') =
theta_y(theta_a(r')) (PA4 and theta_y(r') = r'). "a |><| b iff n = m in P_X": right (a projection below a projection
of the same rank equals it, by Lemma 1.1(a)). The rank lemma: right. "K4 follows from theta_a(theta_y(b)) = a": right.

*k4.pf2.* The file assumes PA2-PA5 and exactly the seven equations a*c = c, y*a = a, b*z = b, y*z = a*b,
a*z = b*a, c*z = b, (b*y)*a = a, i.e. theta_c(a) = c, theta_a(y) = a, b <= z, theta_z(y) = theta_b(a),
theta_z(a) = theta_a(b), theta_z(c) = b, theta_a(theta_y(b)) = a, and refutes b*a != a | a*b != b, i.e. derives
theta_a(b) = a and theta_b(a) = b. It uses neither (Q1), nor theta_a(c) = a, nor b |><| c, nor yc = cy. The sentence
"so that in every projection algebra with (Q1) the condition K4 is equivalent to: its hypotheses imply
theta_a(theta_y(b)) = a" is right (converse: a |><| b gives u = a, v = b, and then
a y b y a = a (y z y) a = a z y z y z a = a theta_z(y) a = a b a = a, using a = az = za). I spot-checked steps 61,
67, 71, 131 of the proof by hand.

*The geometry.* The paragraph "What is proved about the geometry" lists supp a <= supp z, the outer blocks,
D_j <= supp z, Delta_i cap supp z = B_i, eps_z v eps_y = eps_b v eps_y, the E_i, M_j = union of E_i, without proofs
(they are in Theorem 5.49); the first is the unproved (claim'). The five "equivalent geometric forms of the missing
statement" are asserted without argument; since every K4-instance in P(P_m), m <= 7, satisfies a |><| b, a P_4
verification cannot distinguish them from each other or from a |><| b, and "equivalent" should either be proved or
replaced by "candidate intermediate statements, each verified in P(P_4)".

*The case z = b.* The argument is: a ~ b, and if n < m "some I_j contains two indices, say 1, 2" (from the
preceding sentence), then Y meets A_1 and A_2, contradicting theta_a(y) = a. But n < m can also happen because some
T(a)-block lies in an N(b)-block (a type-(ii) class), and this is not excluded by the argument: in the instance of
1.3 one has z = b, a = [0](1 2 3), b = (0)[1 2 3], c = [0 1 2 3], y = (0 1 2 3), all hypotheses except
theta_a(y) = a hold, and A_1 = {0} is an N(b)-block. So the "case z = b" is not "immediate"; it needs the same
missing lemma (whose case I is exactly this situation, and uses theta_a(y) = a in Step B). With the Lemma of 1.6 it
is fine.

---------------------------------------------------------------------------------------------------------------

## 3. Section 5.20 (subsec:count)

*Lemma 5.40 (invariance).* Correct. I re-derived the proof: with S = supp w, sigma the common partition of S induced
by rho_p = eps_w v eps_p and rho_q, and eps_z = eps_w v mu with mu supported in S, the classes of eps_z v eps_p are
the rho_p-classes missing S together with one class per class of sigma v mu|_S; the count and the support count
follow as stated (for the support count: the classes of the first kind meeting supp p number |rho_p|_{supp p} minus
the number of "marked" parts G, and the second-kind classes meeting supp p number the classes of sigma v mu|_S
containing a marked part; both corrections are the same for p and q). The last assertion (transport along x ~ y via
xy <= y) is right.

*Corollary 5.41.* Correct (the equality case uses Lemma 1.1(c) to pass from eps_a = eps_c to a = c).

*Lemma 5.42 (contraction).* Correct. Wording: "it drops if the first identification joins two vertices of one
component" should read "we may perform that identification first; then |V| - c drops by one at that step and never
increases afterwards".

*Lemma 5.43 (value).* Correct: g_a - g_c = kappa - |eps_c| and g_c <= |eps_c| - kappa force g_a = 0 (= (A)) and the
equality case of 5.42 (= (M)); (G2') from the support count as written.

*Theorem 5.44 (end step).* Correct. I checked: (i) and (ii) (the spanning forest Lambda; |tau| - |tau v mu| <= s' - g
with the equality clause, and |eps v eps_c| = kappa_bc - (s' - g)); the identity (N); r_1 + r_2 = (|eps_c| - kappa_bc)
+ (s' - g) with r_1 <= |eps_c| - kappa_bc (Lemma 5.42 with pi_0 = eps_c <= eps_a v eps_c, rho = eps_b) and
r_2 <= s' - g, hence equalities and (star); (G1) from N >= |eps_a v eps_b| - (s' - g); (G2) from (star) and (G2').
The hypotheses of Lemma 5.43 are the first count, and (G2') needs the second: both are in the statement. The
closing Lemma 5.3x (lem:closing) is right.

*Theorem 5.45 ((W_n), (W_infinity)).* Correct: y in Comp(c) has the two values of c (Cor. 5.41), m = yb <= y
transports them (Lemma 5.40), eps_m = eps_b v mu with mu the grouping by the classes of eps_y v eps_b (Lemma 1.1(b);
I checked that eps_{yb} = eps_y v eps_b for commuting y, b), and Theorem 5.44 closes. The previous reader's wish
("a hand proof of a not in Comp(c)") is met by Cor. 5.41.

*Theorem 5.46.* Reduces to Theorem 5.34 (checked by the previous reader) with its hypotheses discharged by 5.45 and
Prop. 5.37; nothing to add.

*Theorem 5.47 ((R'') and K6 from (Q1) + (W_2)).* The files `rpp_vs_chain.pf` and `k6_vs_chain.pf` assume PA1-PA5,
(Q1) as A*B = A & A*C = A -> B*C = C*B, (W2) with both conclusions, and exactly the hypotheses of (R''), resp. K6, of
conditions.in (c*a = a, a*c = c, c*b = b, b*c = c; x*c = c*x, a*x = c*x, y*b = b*y, b*x = a*y; resp. z*y = a*z,
z*c = a*y, b*z = a*b), and refute a |><| b. The variable pattern of the (W2) clause (A = c, B = a, C = b, D = x,
E = y) matches (W2) of conditions.in. The narrative of the K6 derivation in the text (theta_y(a) <= c, so y ~ c by
(Q1), then theta_z(a) = theta_z(c), theta_y(a) = theta_y(c), y ~ z, z ~ b) agrees with steps 276, 1395, 277, 1640,
328/330, 332 of the file. Correct.

*Theorem 5.48 ((E_1) from (Q1) + (W_2) + K0).* Only the README is available; the text agrees with it (227 steps,
701 s, lemmas L1-L5 with the stated provenance, (R) from (W_2)). Cited, not checked.

*Computer checks paragraph.* I did not rerun delta.py, deltaW.py, thm6.py; their descriptions are consistent with the
theorems (deltaW.py's finding "a |><| b fails in 1,992 instances, in none of which delta' = 0" is exactly what
Theorem 5.45 predicts).

---------------------------------------------------------------------------------------------------------------

## 4. The correction in Theorem 5.23, Step 1(iv)

The new text is correct: axa = ava = a(cy)a = ac(ya) = ac(ay) = (aca)y = ay = u uses only ax = av (ii), v = cy (iii),
ya = ay and aca = a; the matching u |><| v is verified directly (uvu = ya yc ya = y a c y a = y aca y = yay = u,
and vuv likewise), and the intermediate "u = (yg)(yg)*, v = (yg)*(yg)" with yg = gy is correct but no longer load
bearing. The counterexample to "hh* |><| h*h for every h" (h = {0 -> 1} in P_2) is right, and so is the remark that
hh* and h*h are only D-related.

Search for other uses of the false principle (grep for hh^*, gg^*, xx^*, ... near "bowtie"/"matched"): none.
The two places that look similar are sound: Lemma "friends" (theta_p(q) |><| theta_q(p); proof via pq idempotent)
and Step 2(b) of Theorem 5.16 (u = (uv)(uv)* = uvu, which uses the commutation xg = gx explicitly).

---------------------------------------------------------------------------------------------------------------

## 5. status-table.tex and conditions.in

As they stand, the table and the header of conditions.in faithfully transcribe the notes' claims, including the
claim that K4 is proved; given Section 1, the following entries overstate the evidence and should revert to
"verified m <= 7 (SAT), hand proof modulo one lemma" (or, if the authors accept 1.6, stay as they are once the
lemma is inserted into the notes):
- status-table.tex, header comment ("K4 and hence (E_6) proved"); (E_6) row ("proved ... K4 is proved in every P_X
  (Thm 5.49, 16 Oct); P_8^6 is minimal non-embeddable"); K0-K6 row ("K4 proved in every P_X ...");
- conditions.in, header ("K4 is proved in every P_X, Thm 5.49 of 16 Oct, hence (E6) is proved"), the (E6) comment
  ("PROVED (consequence of (Q1)+K4, and K4 is proved, Thm 5.49)") and the K4a comment ("PROVED in every P_X");
- notes: abstract ("and the path-closing condition K4 ... we prove in every P_X ... and a tenth, of order 9,
  follows"), Theorem 5.49 "Consequently ...", Question 7.(4) "((W_2), (R''), K6 and K4 are: Theorems ...)".

Internal inconsistencies that exist independently of my finding:
- The footnote of the status table still lists (E_6) among "the rows marked verified only", while the (E_6) row is
  marked proved; the comment block at the end of status-table.tex still says "P_8^6 (E_6), P_8^1 (E_1) wait on
  proofs of those conditions" and "Open: are (E_6), (E_1) valid in every P_X?". (After the correction above these
  become right again.)
- Question 7.(2) still asks "are (E_6), (E_1) of Proposition 5.19 valid in every P_X?" and Question 7.(4) still says
  "(W_n) and (R'_n) ... provided (W_n) and (R'_n) are valid in every P_X (verified for small m only ...)", although
  (W_n) is proved for all n in Section 5.20. Section 5.20's own sentence "So P_8^1 and P_8^6 remain the order-8
  candidates whose non-embeddability needs a proof of (E_1) or K0, resp. (E_6) or K4" (written 11-13 Oct) is, as it
  happens, the correct current status.
- Theorem 5.49's parenthetical "every projection algebra of order <= 7 other than P_7 embeds" should read "every
  projection algebra of order <= 7 satisfying (Q1) and (S) other than P_7 embeds" (algebras violating (Q1) do not
  embed); the minimality argument is fine since proper subalgebras of P_8^6 inherit (Q1), (S), (R).
- The K4 formula of conditions.in and the K4 atoms of k4sat.py agree with the hypotheses of Theorem 5.49 (checked
  atom by atom: Y*A = A is theta_A(Y) = A, B*Z = B is B <= Z, Y*Z = A*B is theta_Z(Y) = theta_B(A), A*Z = B*A is
  theta_Z(A) = theta_A(B)).
- The evidence levels of the other rows ((R'_n) verified m <= 5 for n <= 3; (E_1) verified m <= 7 and reduced to
  K0; K0, K5 verified m <= 6; K6 and (R'') proved via (W_2); (W_n) proved) agree with the notes.

---------------------------------------------------------------------------------------------------------------

## 6. List of errors, from serious to cosmetic

1. **(Serious) Theorem 5.49, Step 2, "the left side is n".** False in general; the counting identity it comes from
   is a tautology for every v <= b, and the conclusion drawn ("every B_i lies in some S_j", then "no class of type
   (ii)", then supp u = supp a) is of the full strength of the theorem (fails when any single hypothesis is dropped,
   while the argument uses neither theta_a(y) = a nor the full force of the others). The theorem is therefore not
   proved as written; what is proved is "K4 given supp a <= supp z". A repair is proposed in 1.6.
2. **(Serious, same root) Section 5.20, "K4: reductions ... the case z = b".** "supp a <= supp z" is listed as
   proved, and the case z = b is declared immediate; both rest on the unproved statement (the instance with z = b in
   1.3 satisfies every hypothesis but theta_a(y) = a and has a T(a)-block in an N(b)-block).
3. **(Consequential) All downstream claims of "proved" for K4, (E_6), the minimality of P_8^6 and the "tenth" order-9
   algebra** (abstract; Theorem 5.49; status table rows (E_6), K0-K6 and header; conditions.in header, (E6) and K4a
   comments; Question 7.(4)) are at present at evidence level "verified m <= 7" (m = 8 for the missing statement,
   by my SAT run).
4. (Minor) Theorem 5.49, Step 5: the components of L are the C_s, the clique {(i,i,empty)} and single vertices; and
   the fact s in I_j (needed for B_s <= K'_j in Step 6) should be stated.
5. (Minor) Section 5.20, "equivalent geometric forms of the missing statement": equivalence asserted, not proved,
   and not testable in P(P_m), m <= 7.
6. (Minor) Theorem 5.49, Step 2: "each of these classes meets supp c (it contains D_j, hence ...)": a class of
   eps_v v eps_c need not contain D_j (eps_v v eps_c is not above eps_a); it contains S_j, which contains some B_i,
   which suffices.
7. (Cosmetic) Theorem 5.49: the notation E_k for the c-blocks of the chain in Step 6 clashes with the classes E_i;
   the parenthetical "(and sigma-hat(P_{k-1}) not among the E_{i''})" in Step 6 is unnecessary; "outer block" is
   used in the proof of Theorem 5.44 before it is defined (in 5.21).
8. (Cosmetic) Lemma 5.42: the strictness clause should say that the identification in question can be performed
   first.
9. (Cosmetic) Theorem 5.49: "every projection algebra of order <= 7 other than P_7 embeds" needs "satisfying (Q1)
   and (S)".
10. (Cosmetic) Stale sentences: Question 7.(2) and 7.(4) on (W_n) and (E_6); footnote and comment block of the
    status table (see Section 5).

---------------------------------------------------------------------------------------------------------------

## 7. Suggestions

1. Replace, in Step 2 of Theorem 5.49, the passage from "Next, every B_i lies in some S_j" to "which is therefore
   0" by a lemma proving both (claim) and (claim') - the one in 1.6 if it survives the authors' scrutiny - and make
   the dependence explicit: the lemma uses theta_a(y) = a (through the T(y)-block of E_1) and theta_z(y) = v
   (through the bright/dark dichotomy), which is exactly what the dropped-hypothesis table demands. Then update the
   paragraph "K4: reductions" accordingly (the case z = b becomes a corollary, not a separate "immediate" case).
2. Until that is done, downgrade K4/(E_6)/P_8^6 in the abstract, the theorem, the status table, conditions.in and
   Section 7 to "verified m <= 7 (K4) and m <= 8 (the missing statement); hand proof modulo Lemma X".
3. Adopt, as a routine check for every hand proof of a quasi-identity, the "dropped hypothesis" test of
   `dropmap.py`: for each intermediate statement S of the proof and each hypothesis h, test S on instances satisfying
   all hypotheses but h. A statement that fails when h is dropped cannot be proved without h; if the written argument
   for S does not use h, the argument is wrong. This is what exposed the gap here, which the authors' own k4chk.py
   (which tests the statements on full instances only, where everything is true) could not see. The same test could
   be run retrospectively on the proofs of (R'), (P_1), (Q), (V).
4. In Step 5, state the component structure of L precisely (C_s, the empty-clique, singletons) and record s in I_j.
5. In Section 5.20, either prove the "equivalent geometric forms" or call them candidates.
6. The paragraph after the proof ("The proof uses the y-conditions exactly where the computer said they are
   needed") is good and should be kept, with the lemma of (1) added to the list: "the exclusion of T(a)-blocks
   outside supp z needs theta_a(y) = a as well".
7. My SAT encoding of "K4 hypotheses + some T(b)-block outside supp theta_b(a)" runs in 52 s at m = 7 and 26 min at
   m = 8 with Cadical; it may be a cheaper way to extend the evidence for K4 than the full denial of theta_a(b) = a,
   because by the rest of the proof it is equivalent to K4 in P(P_m).

---------------------------------------------------------------------------------------------------------------

## 8. Scripts (all in review-scripts/, run with python3 from that directory)

- `pm.py n` - independent partition-monoid arithmetic; validates fast.theta and fast.commute on P(P_n).
- `k4verify.py [p5_seconds]` - every intermediate statement of Steps 1-6 on the 37,324 instances of P(P_4) and on
  instances of P(P_5) (log: k4verify_p5.log, 242,694 instances).
- `claimtest.py n` - the Step-2 claim and the counting identity under a |><| c |><| b alone, and under the K4
  hypotheses with one dropped.
- `dropmap.py n` - the dependency table of 1.3.
- `step2trace.py` - the sentences of Step 2 traced on the instances lacking only theta_a(y) = a.
- `repairfacts.py` - the ingredients (a)-(d) of the repair in 1.6 on dropped-hypothesis instances.
- `k4gap_sat.py m [--symbreak] [--rank1] [--n0]` - SAT search for the K4 hypotheses with the negation of the claim
  (logs gap_m7.log, gap_m8.log, gap_m9.log).
