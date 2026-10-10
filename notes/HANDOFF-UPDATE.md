# Handoff update (13 September 2026) — Project B only, for the EXISTING talk-preparation session

This is an *update* to the handoff you already have (`HANDOFF.md`, dated 11 September). You are not
starting fresh: you have already built the slide deck for M. Kinyon's talk, and the purpose of this
update is to let you fix the last few slides, which describe the "current state of play" and the
open questions. Everything before Section 5.4 of the notes (`notes-embedding.pdf`, now 45 pages,
attached) is unchanged, and the Project A material is unchanged. Below: (1) what changed, in the
order it happened; (2) the exact current list of obstructions with statements and witnesses;
(3) what is proved / verified / open; (4) which statements on the old slides are now out of date
and what to replace them with. Theorem numbers refer to the attached PDF.

Conventions as before: θ_p(q) = pqp; q ≤ p iff q = pqp; p ⋈ q ("matched") iff pqp = p and
qpq = q; commuting means pq = qp (⟺ θ_p(q) = θ_q(p)); P(S) is the projection algebra; P_X the
partition monoid; "embeds" means *-embeds. The notation 𝔓 (6 elements), 𝔓_9, P(Q_0), Q(G,⊥),
(Q1), triangle, (S) is as in the old handoff.

---------------------------------------------------------------------------------------------------

## 1. What changed since 11 September

### 1a. Graph semigroups are completely understood (Theorem 5.8, Section 5.4)
For a graph G = (V,E) and a colouring ⊥: V → B, the graph semigroup Q(G,⊥) embeds in some P_X iff
⊥ is a proper colouring (this is (Q1)) and every *bichromatic* subgraph G[V_m, V_n] (edges between
two colour classes) is a disjoint union of complete bipartite graphs — equivalently, no bichromatic
induced path on 4 vertices. The second condition is exactly (S) for these semigroups. The proof
gives an explicit embedding by rank-≤1 partitions with |X| = |V| + (number of bicliques) + 2|B|.
So 𝔔 (the 4-path with colours w,z,w,z) is the smallest bad case *because* it is a bichromatic P_4.
A layered generalisation (Definition 5.10, Theorem 5.12, Section 5.5) is also completely decided by
(Q1) + (S); it contains 𝔓_9. Conclusion: no further obstructions live in these families.

### 1b. A fourth obstruction, (R), found by a census of order 7 (Section 5.6)
All projection algebras of order 7 satisfying (Q1) and (S) were enumerated: 1663 up to
isomorphism (295 of order 6). All satisfy the triangle condition; all but one embed in P(P_m), m ≤ 6.
The exception is the 7-element algebra 𝔓_7 = {a,c,b,x,u,v,w} (Definition 5.14): the projection
algebra of the graph semigroup Q(path a–c–b, injective colouring ⊥a=u, ⊥c=v, ⊥b=w) with one extra
projection x, where u,v ≤ x, x commutes with a and with c (xa = u, xc = v), and x "sees b as it
sees c": θ_x(b) = v. It violates

  (R)  a ⋈ c, b ⋈ c, xa = ax, xc = cx, θ_x(b) = θ_x(c)  ⇒  a ⋈ b.

Theorem 5.16: (R) holds in every P_X (hand proof, nine steps, same block-chasing style as (S) but
without any computer step). There is a 19-element regular *-semigroup 𝔗_19 with P(𝔗_19) = 𝔓_7
(Q(a–c–b,⊥) with x adjoined, x·(p,q) = (λp, ⊥q), λa=λu=u, λc=λb=λv=λw=v). So:
* the smallest regular *-semigroup satisfying (Q1), the triangle condition and (S) that embeds in
  no partition monoid has order between 9 and 19 (was "9 to 20");
* (R) defines a proper quasivariety (not a variety in disguise): a 26-element 𝔗_26, embeddable in
  P_5, maps *-homomorphically onto 𝔗_19 (Remark 5.17). Same as was known for (Q1), triangle, (S).
* (Q1), triangle, (S), (R) are pairwise independent (𝔓_7 satisfies (S), 𝔓 satisfies (R)).

### 1c. A uniform view: path-closing conditions (Section 5.7)
(S) and (R) have the same shape: a matched path p_0 ⋈ p_1 ⋈ … ⋈ p_n, an auxiliary projection x tied to
the vertices by commutation/order/"sees two vertices alike" (θ_x(p_i) = θ_x(p_j)) / "is seen alike"
(θ_{p_i}(x) = θ_{p_j}(x)), conclusion p_0 ⋈ p_n:
  (R): n = 2, x commutes with p_0, p_1, and sees p_1, p_2 alike.
  (S): n = 3, x = p_1 p_3 = p_3 p_1, and x is seen alike by p_0 and p_2.
A systematic search of this scheme (one or two auxiliaries, paths of length ≤ 4, at most three atoms)
found nothing beyond (S), (R) and consequences of (Q1). With FOUR atoms it does (see 1d).

### 1d. Census of order 8 (Section 5.8) — seven more candidate obstructions
Method (Lemma 5.18): a maximal element of a finite projection algebra can always be deleted, so the
algebras of order n+1 satisfying a set of quasi-identities are the one-point extensions of those of
order n. Counts of projection algebras with (Q1)+(S)+(R): 1, 2, 5, 16, 62, 295, 1662, 10828, 80039
for orders 1–9 (1662 = 1663 − 𝔓_7). Order 8: all satisfy the triangle condition; 10821 embed in
P(P_m), m ≤ 7; the remaining SEVEN, 𝔓_8^1, …, 𝔓_8^7, embed in no P(P_m) with m ≤ 8 (SAT, 25 s to
2.6 h each) and all their proper subalgebras embed, so each is a candidate minimal non-embeddable
algebra. Six of them are "graph semigroup on 4 vertices with 3 colours, plus one projection x"
(the same pattern as 𝔓_7); 𝔓_8^7 is different (a 5-element bottom band, 4 elements above).
Each violates a new quasi-identity (Proposition 5.19), verified in all P(P_m), m ≤ 6:

  (R′)  a ⋈ c, b ⋈ c, xc = cx, θ_x(a) = θ_x(c), ya = ay, θ_x(b) = θ_y(b)  ⇒  a ⋈ b
        [witness 𝔓_8^3; also violated by 𝔓_7; (R′) ⇒ (R) in every projection algebra: put
        x′ = xc, y′ = x. So (R′) supersedes (R). Verified up to m = 7.]
  (V)   bcb = b, ata ≤ b, ctc ≤ a  ⇒  ata ≤ btb    (in fact ata = btb)
        [witness 𝔓_8^7; four variables; PROVED for all P_X: Theorem 5.20, see 1e.]
  (P_1) p_0 ⋈ p_1 ⋈ p_2 ⋈ p_3, x commutes with p_0 and p_1, θ_{p_0}(x) = θ_{p_2}(x),
        θ_x(p_1) = θ_x(p_3)  ⇒  p_0 ⋈ p_3   [witness 𝔓_8^2; verified up to m = 7]
  (Q)   p_0 ⋈ p_1 ⋈ p_2 ⋈ p_3, x commutes with p_0, θ_{p_1}(x) = θ_{p_3}(x), y commutes with p_0 and
        p_2, θ_y(p_1) = θ_y(p_2)  ⇒  p_0 ⋈ p_3   [witnesses 𝔓_8^5 and 𝔓_8^4; with y = x it is the
        condition (P_2), and (P_2) ⇒ (S) (path d–b–c–a, x = cd), so (Q) supersedes (S)]
  (E_6) dbd = d, aca = a, ada = a, u ≤ c, u ≤ d, bcb = aua  ⇒  aua = a   [witness 𝔓_8^6]
  (E_1) a nine-atom equational condition in 7 variables [witness 𝔓_8^1] (Proposition 5.19(e)).
(P_1) and (Q) are path-closing conditions with four atoms; (V), (E_6), (E_1) are of a new,
"equational" shape (no matched pair in the conclusion).

Order 9 (Remark 5.22(3)): of the 80039 algebras, 163 contain one of the seven (and violate the
corresponding condition), 1 more violates (R′), and 79 875 satisfy every known condition; of these,
79 868 embed (79 783 with m ≤ 7, and 85 that need m = 8, among them 39 semilattices with 8
join-irreducibles), and SEVEN embed in no P(P_m) with m ≤ 8 — the candidates of order 9. So the count of candidate
minimal non-embeddable projection algebras is 1, 7, 7 for orders 7, 8, 9: the obstructions are
diversifying, not converging.

Caveat (stated in the notes): apart from (V), the order-8/9 non-embeddability claims are SAT
evidence (m ≤ 8), not proofs; embeddable algebras of order 9 exist that need 8 points, so "no
embedding for small m" is not conclusive in general.

### 1e. (V) is proved (Theorem 5.20)
The proof is short compared to (R): writing z = ata, w = ctc, s = btb, three identities valid in
every projection algebra with (Q1) reduce the claim to the single statement
  θ_c(θ_b(t)) = θ_c(t)   ("c cannot distinguish t from its restriction to b"),
and this is proved in P_X by a chain-transfer argument. So 𝔓_8^7 is a proved minimal non-embeddable
projection algebra, the third after 𝔓 and 𝔓_7.

### 1f. Independence (Section 5.9, Proposition 5.23)
Among (Q1), Tri, (S), (R), (R′), (V), (P_1), (P_2), (Q), (E_6), (E_1):
* implications (all by explicit substitution, valid in every projection algebra):
  (Q) ⇒ (P_2) ⇒ (S), and (R′) ⇒ (R). Nothing else implies anything else.
* the eight conditions (Q1), Tri, (R′), (V), (P_1), (Q), (E_6), (E_1) are independent: each fails
  in a finite projection algebra satisfying all the other conditions in the list —
  Q(K_2, const) [order 3] for (Q1), P(Q_0) [11] for Tri, 𝔓_8^3 for (R′), 𝔓_8^7 for (V),
  𝔓_8^2 for (P_1), 𝔓_8^5 for (Q), 𝔓_8^6 for (E_6), 𝔓_8^1 for (E_1).
* (V) neither implies nor is implied by any other condition.
* the seven order-9 candidates satisfy all eleven conditions.

---------------------------------------------------------------------------------------------------

## 2. The current list of obstructions, in one table

| condition | first shown | status in P_X | smallest witness (violates only this one) |
|---|---|---|---|
| (Q1) projections with a common lower bound commute | known | proved | Q(K_2, const), 3 projections |
| Tri (triangle / matching-pattern conditions) | Thm 4.2 | proved | P(Q_0), 11 projections (61-element Q_0) |
| (S) wiring condition | Thm 5.6 | proved (finite SAT step) | 𝔓, 6 projections (20-element 𝔔) — now a consequence of (Q) |
| (R) | Thm 5.16 | proved (by hand) | 𝔓_7, 7 projections (19-element 𝔗_19) — now a consequence of (R′) |
| (R′) | Prop 5.19(a) | verified m ≤ 7 | 𝔓_8^3 (also fails in 𝔓_7) |
| (V) | Thm 5.20 | proved (by hand) | 𝔓_8^7 |
| (P_1) | Prop 5.19(c) | verified m ≤ 7 | 𝔓_8^2 |
| (Q) (⊃ (P_2) ⊃ (S)) | Prop 5.19(d) | verified m ≤ 6 | 𝔓_8^5 |
| (E_6) | Prop 5.19(e) | verified m ≤ 6 | 𝔓_8^6 |
| (E_1) | Prop 5.19(e) | verified m ≤ 6 | 𝔓_8^1 |

Irredundant list: (Q1), Tri, (R′), (V), (P_1), (Q), (E_6), (E_1) — eight independent conditions,
three of them proved for all P_X ((Q1), Tri, (V)), plus the two proved-but-superseded (S), (R).

---------------------------------------------------------------------------------------------------

## 3. Numbers you may want on a slide

* Projection algebras with (Q1)+(S)+(R), orders 1–9: 1, 2, 5, 16, 62, 295, 1662, 10828, 80039.
* Up to order 6: embeddable iff (Q1) + triangle + (S) (unchanged). Up to order 7: iff additionally
  (R) (one exception, 𝔓_7). Order 8: seven exceptions to (Q1)+Tri+(S)+(R); order 9: seven more
  (plus the ones containing order-8 exceptions).
* Regular *-semigroups: up to order 8, embeddable iff (Q1) (unchanged). Smallest counterexample to
  "(Q1) + triangle + (S) suffice": order between 9 and 19 (𝔗_19). Smallest counterexample to
  "(Q1) + triangle suffice": still 𝔔 with 20 elements as the known one, but 𝔗_19 is smaller and
  also satisfies (S), so "9 to 19" is the current bound for both statements.
* Proper quasivarieties: (Q1), triangle, (S), (R) all define classes not closed under
  *-homomorphic images; the class of embeddable regular *-semigroups is not closed under
  *-homomorphic images either (𝔗_26 → 𝔗_19, 26 and 19 elements; previously 32 → 20).

---------------------------------------------------------------------------------------------------

## 4. What on the old final slides is now out of date

Likely statements on the old slides, and their replacements:

1. "Three necessary conditions: (Q1), triangle, (S); pairwise independent; up to order 6 they are
   also sufficient." → Still true, but incomplete: add (R) (order 7) and the seven order-8
   candidates; the honest current picture is "eight independent conditions, three proved, and the
   list is not closing up" (Section 5.9). If the talk should stay light, present (S) and (R) as
   the two proved wiring/path-closing conditions and say that a census of orders 8–9 produced
   further conditions, one of which — (V) — is proved and is only four variables long.

2. "Smallest counterexample to (Q1)+triangle has order between 9 and 20." → between 9 and 19
   (𝔗_19, projection algebra 𝔓_7 of order 7, condition (R)).

3. "Are there further wiring-type obstructions?" (open question) → Yes: (R) (Section 5.6), then
   (R′), (P_1), (Q), (E_6), (E_1), (V) (Section 5.8). The path-closing scheme (Section 5.7) is the
   uniform way to present (S), (R), (R′), (P_1), (Q): a matched path plus auxiliary projections, with
   the conclusion that the path closes.

4. "Which coloured graphs give embeddable Q(G,⊥)?" (open question) → Answered, Theorem 5.8: ⊥ proper
   and every bichromatic subgraph a disjoint union of complete bipartite graphs (no bichromatic
   induced P_4); (Q1) and (S) suffice for graph semigroups and for layered graph semigroups
   (Theorem 5.12). Good slide: the picture of the 4-path w–z–w–z as the forbidden bichromatic P_4.

5. "Is the quasivariety generated by the P(P_X) finitely based?" → still open, and the evidence now
   points the other way: candidate minimal non-embeddable algebras of orders 7, 8, 9 number 1, 7, 7,
   and the conditions they violate have at least three different shapes.

6. "Nothing is currently conjectured to be sufficient" → unchanged; the natural conjecture "finitely
   many forbidden coloured-graph configurations" looks less plausible than it did.

7. Proved-by-hand list → add Theorem 5.8 (graph semigroups), Theorem 5.12 (layered), Theorem 5.16
   ((R)), Theorem 5.20 ((V)), Lemma 5.18 (census by extension), Proposition 5.23 (independence).
   Computer-verified only: the non-embeddability of 𝔓_8^1–𝔓_8^6 and of the seven order-9
   candidates (m ≤ 8), and the validity of (R′), (P_1), (Q), (E_6), (E_1) (m ≤ 6 or 7).

Suggested final-slide text (adjust to the talk's tone):
"State of play. Necessary conditions known to hold in every P_X: (Q1), the triangle (matching-
pattern) condition, the wiring condition (S), the path-closing condition (R), and the four-variable
condition (V): bcb = b, ata ≤ b, ctc ≤ a ⇒ ata = btb. Conjectured (verified in P_6, P_7): four more.
They are independent, none is a variety condition, and they are exactly what is needed up to order
7 (projection algebras). A census of orders 8 and 9 — made possible by the observation that a
maximal projection can always be deleted — produced 7 + 7 further candidate obstructions, so the
list is not finite as far as we can see. Graph semigroups Q(G,⊥) are completely understood: embeddable
iff ⊥ is proper and no bichromatic induced P_4. Smallest known counterexample to (Q1)+triangle:
19 elements; smallest possible: ≥ 9."

---------------------------------------------------------------------------------------------------

## 5. Files

* `notes-embedding.pdf` (45 pp., attached) — the current notes; Sections 5.4–5.9 are the new
  material (Theorem 5.8, 5.12, 5.16, 5.20; Propositions 5.15, 5.19, 5.23; Definition 5.14 gives the
  table of 𝔓_7; the seven tables of 𝔓_8^k are printed in Section 5.8).
* The full code and census data are in `embed_kit.tgz` (`embed/pa8/README.md` explains the census
  scripts); you do not need them for the slides.
