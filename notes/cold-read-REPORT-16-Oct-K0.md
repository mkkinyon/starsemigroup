# Referee report: Theorem 5.50 (K0 holds in every partition monoid)

Files read: `thmK0.tex` (theorem, proof, post-proof paragraph), `lemPX.tex` (Lemma 1.1), `CONTEXT.md`.
Scripts (mine, in `review-scripts/`): `k0claims_ref.py` (claim checker; logs `k0claims_ref4.log`,
`k0claims_ref5.log`), `k0drop_ref.py` (own instance generator + dropped-hypothesis map for P_4; log
`k0drop_ref4.log`), `ya_eq_u.py`, `misc_ref.py`. The author's `k0claims.py` was not used; I used the
bit calculus `review2/review-scripts/fast.py` (re-validated against the union-find multiplication
`review3/review-scripts/pm.py` on all of P_3: 0 discrepancies in 484 pairs) and Lemma 1.1(c) was
re-checked on all 1512 matched pairs of P_4 (0 violations). Total CPU ~7.5 min.

## Verdict

**The proof is correct, with one gap in presentation at Step 1 that has an easy repair, and two
sentences whose stated justification is too short.** No step silently assumes a ⋈ b; every count is
non-tautological; the cases the request asked about (T(y)-block meeting an N(a)- and a T(a)-block,
blocks of y leaving supp a ∪ supp b ∪ supp c, crossing block meeting an N(b)-block, empty diagonal cells,
m = 1, m = 0) are all covered by the argument as written. Numerically every intermediate claim holds
on all 68 455 instances of P(P_4) and on a 150 000-instance random sample of P(P_5), and the
dropped-hypothesis map (my own generator, P_4) reproduces the dependencies the post-proof paragraph
claims.

## Issues

### Issue 1 (Step 1, gap in justification; repairable). Sentence:

> "by (Q1), $ay=ya$ and $by=yb$, and then $\theta_y(a)=ya=u$, $\theta_y(b)=yb=v$."

$\theta_y(b)=v$ is a hypothesis, but $\theta_y(a)=u$ is **not** (the hypothesis is
$\theta_y(z)=u$, not $\theta_y(a)=u$), and nothing said so far implies it: from $u\le y$, $u\le a$,
$ay=ya$ one gets only $u\le ya$ (indeed $ya\cdot u\cdot ya=y(aua)y=yuy=u$), i.e. $ya\ge u$; the meet
of two commuting projections can be strictly larger than a common lower bound. The claim is used
essentially: Step 2 "Consequences" ("The $\T$-blocks of $u=ya$ are the classes $U_1,\dots,U_n$ of type (i)
... the $U_j$ are the sets $M_j\cap\supp a$ ... every $M_j$ meets $\supp b$"), Step 3 (the blocks of
$u=ya$ inside $\supp y$) and Step 6 (the chain argument inside $U_j$, which needs $U_j$ to be a single
type (i) class containing $A_1,A_2$) all depend on $ya=u$. If $M_j\cap\supp a$ were a union of two type (i)
classes, Step 6 would produce no crossing block and no contradiction.

**Repair** (uses only facts proved later in the same Step 1, so the sentence just has to be moved after
"$\theta_a(z)=a$"): with $aza=a$, $ay=ya$, $yzy=u$ and $aua=u$,
$$ (ya)\,z\,(ya) \;=\; y(aza)y \;=\; yay \;=\; ya, \qquad (ya)\,z\,(ya) \;=\; (ay)\,z\,(ya) \;=\; a(yzy)a \;=\; aua \;=\; u, $$
so $ya=u$. (Checked with union-find products on 9 780 P_4 instances: 0 violations, `misc_ref.py`.)
This is a four-line algebraic identity; the rest of the proof is unchanged. Side observation (P_4,
`ya_eq_u.py`): $ya=u$ already follows from $a\bowtie c\bowtie b$, $yc=cy$, $\theta_y(b)=v$ and $u\le y$
alone (0 failures in 31 675 instances), but fails if any of these three is dropped (10 780 / 7 066 /
24 182 failures), so a $z$-free proof may exist; the algebraic one above is the natural one here.

### Issue 2 (Step 2, first half; justification too short). Sentence:

> "So $N$ is a union of $\T(c)$-blocks, and the $\N(b)$-block $N$ contains some $C_k$, impossible."

An $\N(b)$-block containing a $\T(c)$-block is **not** impossible for $b\bowtie c$: in P_3,
$b=(0\,2)[1]$, $c=[0](1\,2)$ are matched and the $\N(b)$-block $\{0,2\}$ contains $C=\{0\}$
(`misc_ref.py`). What makes the case impossible is that $N\subseteq\supp c$: $N$ is a block of $b$, hence
lies in one $\Delta_l$, which contains exactly one $\T(c)$-block, so $N=C_l$, a $\T(c)$-block that is an
$\N(b)$-block, contradicting Lemma 1.1(c). The second half of Step 2 does spell out exactly this
argument for the $(y,c)$/$\Delta$ decomposition, so only the first half needs the extra clause.

### Issue 3 (Step 6, wording). Sentence:

> "so some $\T(y)$-block of $U_j$ meets $A_1$ and $A_2$"

Connectivity of $U_j$ by alternating chains gives a $\T(y)$-block meeting two $\T(a)$-blocks of $U_j$,
not necessarily $A_1$ and $A_2$. Harmless: either relabel (choose $1,2$ as two indices met by one
crossing block), or note that what is used is only "$K_j$ contains a crossing block", after which Step 5
gives $A_i\subseteq D_i\subseteq L'_i$ for every $i\in I_j$.

### Remarks (no action needed)

* Step 5: "$K_F$, which meets $\supp a$ in nothing (its intersection with $\supp y$ is $F$)" is correct
  but uses $\supp a\subseteq\supp y$ (each $A_i\subseteq U_j\subseteq\supp y$, Step 2), which could be said.
  Numerically $K_F\cap\supp a=\emptyset$ holds in all full-hypothesis instances and fails in 11 364
  instances of the $-\theta_y(z)=u$ column, as expected.
* Step 1, rank count for $\theta_a(z)=a$: not a tautology; it uses $\rk p=m=\rk a$ from
  $b=\theta_b(z)\bowtie\theta_z(b)=p$ and $b\bowtie c$. Fails (5 868 resp. 996 instances) when
  $\theta_b(z)=b$ resp. $\theta_z(a)=\theta_z(b)$ is dropped.
* Step 4(c) "every block of $z$ lies in one cell" is trivially true (a block of $z$ is inside one class
  of each join); it is used only as a step in the chain argument, so this is fine.
* Empty diagonal cells occur in valid instances (24 of 68 455 in P_4, 136 of 150 000 in the P_5 sample),
  e.g. $a=[0][1](2\,3)$, $b=(0\,2)[1][3]$, $c=[0](1\,2)[3]$, $y=1$, $z=a$: both $D_1,D_2$ are empty and
  $A_i\not\subseteq L'_i$. The proof is consistent with this: it claims $A_i\subseteq D_i$ only when $K_j$
  contains a crossing block, and no full-hypothesis instance has one (see below).
* $m=1$: $n<m$ forces $n=0$, but every $A_i$ lies in a type (i) class $U_j$, so $n\ge1$ when $m\ge1$;
  $m=0$ is trivial. Covered.
* Crossing block meeting an $\N(b)$-block: excluded in 4(a) by "every $\N$-block of $b$ meeting a
  $\T(y)$-block contains it" plus $Y\cap A_{i'}\subseteq\Delta_{i'}$; correct. A $\T(y)$-block meeting both
  an $\N(a)$-block and a $\T(a)$-block is excluded by Lemma 1.1(b) for the commuting pair $(y,a)$ (types
  (i)/(ii)). Points of $\T(y)$-blocks outside $\supp a\cup\supp b\cup\supp c$ occur (32 296 instances in
  P_4) and are harmless: such a block is then inside an $\N$-block of $a$, of $b$ and of $c$.

## Numerical results

### Full hypotheses (`k0claims_ref.py`)

All 68 455 instances of P(P_4) (m-distribution 0:12854, 1:50743, 2:4731, 3:126, 4:1) and 150 000 random
instances of P(P_5) (m: 0:17247, 1:119971, 2:12343, 3:428, 4:11). **0 failures** for every claim:
$u\le a,v\le b,u\le y,v\le y$; $ya=ay$, $by=yb$; $\theta_y(a)=u$; $\rk p=m$; $\theta_a(z)=a$; $L_i$ and $L'_i$
distinct; every $A_i$ and every $B_i$ meets $\supp y$; no $\N(y)$-block is a union of $\T(a)$- or of
$\T(b)$-blocks; every $\N(y)$-block is an $\N(a)$-, $\N(b)$- (and $\N(c)$-) block; every $\T(y)$-block lies in
$\supp a$ or in an $\N(a)$-block (same for $b$, $c$); every $\N$-block of $a,b,c$ meeting a $\T(y)$-block
contains it; $\{U_j\}=\{M_j\cap\supp a\}$, every $M_j$ meets $\supp b$, $\#U=n=\rk(ya)$; classes of
$\varepsilon_y\vee\varepsilon_z$ meeting $\supp y$ are the $K_j$ (meeting $\supp z$) and $K_F$ (missing
$\supp z$); crossing blocks $\subseteq\bigcup(A_i\cap B_i\cap C_i)\subseteq\bigcup D_i$; non-crossing
$\T(y)$-blocks, $\N(y)$-blocks and $z$-blocks in one cell; classes of $\varepsilon_y\vee\varepsilon_z$ in one
cell or (with a crossing block) in $\bigcup D_i$; $A_i\subseteq D_i$ when $K_j$ has a crossing block, else in
one cell; $\varepsilon_a\le\varepsilon_b\vee\varepsilon_z$; $\varepsilon_a\vee\varepsilon_b\le\varepsilon_b\vee\varepsilon_z$;
$n=m$; $a\bowtie b$.

Caveat: under the full hypotheses **no instance contains a crossing block** (as must be, since $a\bowtie b$
holds), so claims 4(a), the crossing case of 4(d) and the diagonal case of Step 5 are vacuous there; they
are exercised only in the dropped-hypothesis columns below (1 812 / 96 / 2 424 instances with crossing
blocks in the $-yc=cy$ / $-\theta_y(b)=v$ / $-\theta_y(z)=u$ columns).

### Dropped-hypothesis map, P_4 (`k0drop_ref.py`, own generator; entries = failures / instances in the column; each column keeps $a\bowtie c\bowtie b$ and all other hypotheses)

| statement | full | $-yc{=}cy$ | $-\theta_y(b){=}v$ | $-\theta_b(z){=}b$ | $-\theta_z(a){=}\theta_z(b)$ | $-\theta_z(a){=}\theta_z(b)$, $+\theta_a(z){=}a$ | $-\theta_y(z){=}u$ |
|---|---|---|---|---|---|---|---|
| instances | 68455 | 385121 | 255925 | 74323 | 69451 | 68455 | 2142054 |
| violate full hypotheses | 0 | 316666 | 187470 | 5868 | 996 | 0 | 2073599 |
| $a\bowtie b$ | 0 | 33206 | 168 | 5868 | 996 | 0 | 9852 |
| $\theta_a(z)=a$ | 0 | 0 | 0 | 5868 | 996 | 0 | 0 |
| $\theta_y(a)=u$ | 0 | 0 | 0 | 0 | 0 | 0 | 898216 |
| $u\le y$ (and $ya=ay$) | 0 | 0 | 0 | 0 | 0 | 0 | 898216 |
| every $A_i$ meets $\supp y$ | 0 | 31394 | 72 | 0 | 0 | 0 | 8424 |
| every $B_i$ meets $\supp y$ | 0 | 31394 | 5604 | 0 | 0 | 0 | 7020 |
| $\N(y)$-blocks are $\N(a)$-blocks | 0 | 31394 | 72 | 0 | 0 | 0 | 417906 |
| $\N(y)$-blocks are $\N(b)$-blocks | 0 | 31394 | 116482 | 0 | 0 | 0 | 7020 |
| $\T(y)$-block in $\supp c$ or in an $\N(c)$-block | 0 | 165944 | 0 | 0 | 0 | 0 | 0 |
| $\T(y)$-block in $\supp b$ or in an $\N(b)$-block | 0 | 0 | 101084 | 0 | 0 | 0 | 0 |
| $\T(y)$-block in $\supp a$ or in an $\N(a)$-block | 0 | 0 | 0 | 0 | 0 | 0 | 557710 |
| $U_j=M_j\cap\supp a$ (as sets) | 0 | 31394 | 72 | 0 | 0 | 0 | 434940 |
| $K_j$/$K_F$ description of $\varepsilon_y\vee\varepsilon_z$ | 0 | 0 | 0 | 0 | 0 | 0 | 2049321 |
| crossing $Y\subseteq\bigcup(A_i\cap B_i\cap C_i)$ | 0 | 1728 | 72 | 0 | 0 | 0 | 192 |
| crossing $Y\subseteq\bigcup D_i$ | 0 | 1704 | 72 | 0 | 0 | 0 | 120 |
| non-crossing $\T(y)$-block in one cell | 0 | 204 | 34366 | 0 | 0 | 0 | 204970 |
| $\N(y)$-block in one cell | 0 | 96 | 16977 | 0 | 0 | 0 | 32581 |
| class of $\varepsilon_y\vee\varepsilon_z$: one cell / in $\bigcup D_i$ | 0 | 1908 | 50461 | 0 | 0 | 0 | 236105 |
| $A_i\subseteq D_i$ if crossing in $K_j$, else one cell | 0 | 1776 | 23424 | 1872 | 996 | 0 | 206720 |
| $\varepsilon_a\le\varepsilon_b\vee\varepsilon_z$ | 0 | 1908 | 50461 | 1872 | 996 | 0 | 605650 |
| $\varepsilon_a\vee\varepsilon_b\le\varepsilon_b\vee\varepsilon_z$ | 0 | 1908 | 50461 | 1872 | 996 | 0 | 605650 |
| $U_j$ with $\ge2$ $A_i$ has a crossing block | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

(Full table with all 45 rows in `review-scripts/k0drop_ref4.log`.) The column instance counts agree with
the author's independent generator (316666 / 187470 / 5868 / 996 / 2073599 violating instances).

Reading of the map against the proof's stated dependencies (post-proof paragraph):
* Step 1's $\theta_a(z)=a$ fails exactly when $\theta_b(z)=b$ or $\theta_z(a)=\theta_z(b)$ is dropped, and
  with $\theta_z(a)=\theta_z(b)$ replaced by $\theta_a(z)=a$ every claim (and $a\bowtie b$) still holds in
  P_4 (last-but-one column), as the paragraph asserts.
* Step 2 (no type (iii); $\N(y)$-blocks are $\N(a)$-, $\N(b)$-blocks) fails without $yc=cy$ or without
  $\theta_y(b)=v$, and nowhere else, as the proof uses exactly these.
* $\theta_y(a)=u$ (Issue 1) fails only without $\theta_y(z)=u$ (898 216 instances, precisely those in
  which $u\le y$ fails), so the claim is true under the hypotheses; the issue is purely one of
  justification.
* Step 4(a) (crossing blocks) and the one-cell confinement of non-crossing and $\N(y)$-blocks fail without
  $yc=cy$, without $\theta_y(b)=v$ and without $\theta_y(z)=u$ (and never without the $z$-hypotheses), as
  claimed; Step 5 fails without any single hypothesis. So the proof is not using less than it says.
