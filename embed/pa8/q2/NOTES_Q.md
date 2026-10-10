# Working notes for the hand proof of (Q)   (session of 17 Sept 2026)

Path a|><|c|><|b|><|d; A_i <-> C_i (Gamma_i) <-> B_i (Delta_i) <-> D_i (Lambda_i); sigma(A_i) = D_i.
Hypotheses: x~a, th_c(x)=th_d(x); y~a, y~b, th_y(c)=th_y(b).  Goal a|><|d  <=>  rk(ad)=s  <=> th_a(d)=a.

## Reductions / algebraic facts (all verified P_4 exhaustively + P_5 samples; some PA-proved)
* WLOG x = u := xa = ax <= a  (theta_c(u)=theta_d(u) still holds; PA-provable? verified).  cd=dc (Q1). z := th_c(u)=th_d(u) <= c,d.
* u <= th_a(d) (PA proof: (u*d)*a = u*(d*a)).  th_y(d)=th_y(b) holds in P_X (Prover9 fails in 120s).
* T->N relabelling of a u-group keeps validity: WLOG u has rank 0. Non-hub groups may be T-labelled.
* w := th_b(z) <= b satisfies th_c(w)=th_d(w)=z (transport). z is a valid reversed-path y (z~c, z~d, th_z(b)=th_z(c)).
* Word identities: ud = ucd = ucbd; udu = u; y ad = y abd = y acbd; ycb = yb; ydb = yb; ybd = yd; yc = ybc; yd = ybd;
  y aba y = yay; (ya) d (ya) = ya;  c ad c = c d c.  (ad = acbd FAILS in 24/3156 P_4 paths.)
* Valid y's closed under th_{y1}(y2) for commuting pairs; no canonical y (no least/greatest in general). Rank-0 y exists iff ab=ba.

## Structure from u (groups P of T(a)-indices; A_G, C_G, B_G, D_G unions over G)
* Pi_1 := eps_u v eps_c = eps_u v eps_d = eps_a v eps_z; classes Gamma_G = U_{i in G} Gamma_i and plain W (no T(a),T(c)).
* From b's side (w): Delta_G = Lambda_G (:= U Delta_i = U Lambda_i, i in G), and traces: for each G either
  NON-HUB: C_G subset supp d, C_G = D_G = Gamma_G ∩ supp d, N(c)|Gamma_G = N(d)|Gamma_G;
  HUB: C_G in N(d), D_G = E'_G is a single N(c)-block (inside Delta_G=Lambda_G); Gamma_G ∩ supp d = E_G in N(c) or empty,
       E_G = D_{pi(G)} = E'_{pi(G)}; pi: {hubs with trace} u {plain W with trace} -> {hubs} bijection.
* Other N(c)-blocks are N(d)-blocks and vice versa.  |G|<=2 for hubs (Hb).  pi need not be identity (2-cycles of singleton hubs occur).
* Hub wiring: Lambda(C_G) = Lambda_j for some j in G (so contains D_j, B_j); Delta(E_G) = Delta_k for some k in pi(G).
* CLAIM (A) [proved by hand, see below]: plain classes W contain no T(d)-blocks; hence every hub has nonempty trace, pi permutes hubs.
* Coarsening along u-groups preserves path and u but NOT y.  SPLITTING works (verified): d1 := T-blocks {D_k: k in non-hub groups} u {C_i : i in hub groups},
  N-blocks N(c).  Then (a,c,b,d1) and (a,d1,b,d) are (Q)-instances.  So (Q) <= (Q-nh: no hubs) + (Q-h: c,d agree on non-hub classes).

## Structure from y
* Pi^a = eps_y v eps_a classes: T-lab A_H (= U T(y) = U T(a)), N-lab A_H (single N(y)-block = U T(a)), N(a)-blocks (N(y) or U T(y)), common.
  Pi^b similarly with Q_G (T-lab/N-lab), F (N(b) = U T(y)), common.   K-classes of eps_y v eps_c meeting supp y: trace Q_G (meets supp c) or F (misses supp c).
* N(y)-blocks are (U T(a) or N(a)) and (U T(b) or N(b)): 4 kinds: common group (A_H = Q_G'), BRIDGE (N(b), U T(a)), CO-BRIDGE (N(a), U T(b)), common N(a)∩N(b).
* (Y7) N(b)-block meeting supp c u supp d is an N(y)-block, hence a-good.  (Y10'') every a-block Z: Z∩(supp c u supp d) ⊆ supp b, or Z ⊆ an N(b)-block.
* T(y)-blocks meet supp c u supp d only inside supp b; in a class Gamma_G they meet C_G only at diagonal-b points C_m∩D_m∩B_m.
* K-argument: N(b)-blocks on a Delta-path starting at a T(c)-block, or on a Lambda-path starting at a T(d)-block, are N(y)-blocks (else the class K of eps_y v eps_c
  (resp. eps_y v eps_d) of a T(y)-block inside it would contain the T(c)- (T(d)-) block, contradicting the trace description).
* (T(c)-blocks in K_{Q_G}) = {C_i : B_i ⊆ Q_G} (from ycb=yb); same for d.  (L2) bridge Q: Delta(Q) contains C_m => A_m ⊆ Q.  (L1 false.)
* Lemma Y-A: an a-block meeting two T(d)-blocks D_k, D_l meets them inside B_k, B_l.  Lemma U-B: no a-block meets two T(d)-blocks inside supp b (uses only u-structure).
  => K3: every a-block meets <= 1 T(d)-block.  K6: every T(d)-block meets <= 1 T(a)-block.  Hd: every N(d)-block (incl. hubs) meets <= 1 T(a)-block (needs both u,y).
* off-diagonal points C_m ∩ D_k (k≠m) lie in N(b)-blocks (N(y), a-good); A_i ∩ D_k ⊆ C_i.

## Claim (A) proof sketch
Suppose D_j ⊆ E_W ⊆ W plain. Lambda-path D_j,F_1,E_1,...,B_j: F's are N(y)∩N(b), a-good; a-good N(b)-block meeting W is an N(a)-block ⊆ W (W has no T(a)); so path stays in W.
B_j ⊆ N(y)-block Q => Q ∈ N(a) ⊆ W => B_j ⊆ W; then Delta-path from C_j to B_j (N(b)'s are N(y), a-good) stays in W backwards => C_j ⊆ W, contradiction.
B_j ⊆ supp y (T-lab): a T(y)-block of B_j meets F_m ∈ N(y)∩N(a): impossible unless m=0, i.e. B_j ∩ D_j ≠ ∅; then E_W ∈ Delta_j; Delta-path from C_j to E_W stays in W backwards => C_j ⊆ W, contradiction.

## Non-hub class Gamma_G (T-lab): needed statements (all verified)
kappa := components of graph on N(a)|Gamma_G ⊔ N(c)∩N(d)|Gamma_G.  alpha(kappa) = the A it touches (<=1), gamma = the C (<=1, same index).
(T1) each kappa touches <= 1 T(d)-block.  (T2') D's attached to A_i (directly or via kappa with alpha=i) : <= 1.  (E5) >= 1.  (T4'),(E6) dually.
In the rank-0-y case (ab=ba): (T1),(T2'),(E5) proved by Lambda/Delta-path arguments (co-bridges force index equality; commons propagate Lambda∩Delta classes; a bridge Q ⊇ A_i meeting C_i at p gives Q ∈ Delta_i, and Q ∈ Delta_k via an N(c)-block meeting A_i in Delta_k forces i=k).
(E6) reduces to (T4') by counting (tau: G->G injective iff surjective).

## Hub classes: open.  H1',H2' wiring; (h1) singleton->2-hub must be excluded; (h2) 2-hub->2-hub matching; (h3) |G|>=3 excluded.

## Files: q2/hq.py (harness), t*.py (claims), instQ4.pkl, instQ5_*.pkl, split.py, coarsen.py, p9/ (Prover9).

## 18 Sept 2026: (Q) PROVED (notes Section 5.11, Theorem thm:Q; Props prop:Qnh, prop:Qh)
Key facts that closed the hub case:
* F0: Pi_1 = eps_u v eps_d = rho v eps_u  =>  every rho-class inside Gamma_G contains some A_i (h3.py). Makes (d) of the
  old hub-free proof trivial; z <= th_d(a), u <= th_a(d), th_{ya}(d)=ya are NOT needed.
* b-side only: |G| <= 2 for hubs and CROSS WIRING of 2-hubs G={k,l}: C_G <= Lambda_l, D_G <= Delta_k, so
  C_k <= Delta_k ∩ Lambda_l, D_l <= Delta_k ∩ Lambda_l, C_k ∩ supp b = D_l ∩ supp b = ∅ (h1.py, h4.py V10).
* Step 3 lemma (*): classes K of eps_y v eps_c of the second kind (trace an N(b)-block F ⊆ supp y) swallow every
  Delta_m- or Lambda_k-path started at F or at a c-block of K (covered-set induction; handles B_m on the path).
* Rigidity: a defined non-diagonal pair (k,m) propagates along chains of N-type N(a)-blocks and commons; b-type blocks
  reset to diagonal/undefined.
* Hub class Gamma_G, nu = components of N(a) ∪ commons ∪ {C_G}: Claim 1 (h2 H2) nu's N(a)-blocks meet <= 1 T(d);
  Claim 2 (H3) <= 1 D attached per A_i; => tau: G -> pi(G) surjective, |pi(G)| <= |G|, counting over the permutation pi
  gives equality; Claim 3 (H1) nu touches <= 1 T(a). Conclusion: each rho-class = {A_i, D_tau(i)} + N-blocks.
* Splitting (Step 6 old) and cycle-undoing are no longer needed; Prop Qnh applies to non-hub classes of any instance.
Files: h1.py (cross wiring, examples), h2.py (H1-H5, nonhub_ok, size, pi), h3.py (F0), h4.py (V3-V10 contact rules).
Refereed twice by an independent session (gaps: T(b)-block on Delta/Lambda paths -> lemma (*); shortest-path convention;
trace argument via theta_d(w) instead of ud=ucbd).
