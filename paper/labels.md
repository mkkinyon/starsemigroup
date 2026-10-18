# Labels of the quasi-identities: research names, paper macros, and candidate memorable names

Status: the paper (`embedding.tex`) uses the research labels through macros, so that a renaming is a
one-line change per condition. Candidate names are collected here for a later phase (low priority,
per M.K., 17 Oct); nothing has been renamed yet. (Tri) is the model of a good name.

| research label | macro      | statement (abbreviated)                                                                      | mechanism / candidate names |
|----------------|------------|-----------------------------------------------------------------------------------------------|-----------------------------|
| (Q1)           | `\Qone`    | r ≤ p, q ⇒ pq = qp                                                                              | projections with a common lower bound commute. Candidates: (PC) "projection condition" (East et al.'s usage), (LB) "lower bounds". The clash with the unrelated (Q) is the reason to rename one of the two. |
| (Tri)          | `\Tri`     | triangle condition                                                                              | keep. |
| (D_E)          | —          | digraph conditions                                                                              | keep (indexed family). |
| (S)            | `\Wire`    | a⋈c⋈b⋈d, cd = dc, θ_a(cd) = θ_b(cd) ⇒ a⋈d                                                      | closes a 4-cycle; the auxiliary is the product of two commuting vertices. Candidates: (Sq) "square", (Cy4). |
| (R)            | `\Rcond`   | a⋈c⋈b, x~a, x~c, θ_x(b) = θ_x(c) ⇒ a⋈b                                                          | one auxiliary commuting with two vertices and seeing the third alike. Corollary of (R′). Candidates: (A1) "alike, one auxiliary". |
| (R′)           | `\Rp`      | a⋈c⋈b, x~c, θ_x(a) = θ_x(c), y~a, θ_x(b) = θ_y(b) ⇒ a⋈b                                          | two auxiliaries, "sees alike" twice. Candidates: (A2). |
| (R″)           | `\Rpp`     | order-9 relative, verified only                                                                 | remark only. |
| (V)            | `\Vcond`   | bcb = b, ata ≤ b, ctc ≤ a ⇒ ata = btb                                                          | crosswise restrictions; proof reduces to θ_c(θ_b(t)) = θ_c(t). Candidates: (Cross), (X). |
| (P_1)          | `\Pone`    | a⋈c⋈b⋈d, x~a, x~c, θ_a(x) = θ_b(x), θ_x(c) = θ_x(d) ⇒ a⋈d                                        | length-3 path, one auxiliary. |
| (P_2)          | `\Ptwo`    | (intermediate between (Q) and (S))                                                              | corollary of (Q). |
| (Q)            | `\Qcond`   | a⋈c⋈b⋈d, x~a, θ_c(x) = θ_d(x), y~a, y~b, θ_y(c) = θ_y(b) ⇒ a⋈d                                  | length-3 path, two auxiliaries; implies (P_2), (S). Must not be confused with (Q1): rename one of them. |
| K4             | `\Kfour`   | a⋈c⋈b, aya = a, b ≤ z, y~c, θ_z(y) = θ_b(a), θ_z(a) = θ_a(b) ⇒ a⋈b                              | an auxiliary above a vertex. Candidates: (Ab) "above", (Up). |
| K0             | `\Kzero`   | a⋈c⋈b, y~c, θ_y(b) = θ_b(a), θ_b(z) = b, θ_z(a) = θ_z(b), θ_y(z) = θ_a(b) ⇒ a⋈b                   | a half-matched auxiliary that sees a and b alike. Candidates: (Hm) "half-matched", (Hf). |
| K0″            | —          | K0 with θ_z(a) = θ_z(b) replaced by θ_a(z) = a                                                   | same proof; K0″ ⇒ K0 in finite algebras (descent), K0 ⇏ K0″. |
| (E_1), (E_6)   | `\Eone`, `\Esix` | census conditions, consequences of K0, K4 with (Q1), (W_2)                                 | keep as census labels or drop in favour of K0, K4. |
| (W_n)          | `\Wn`, `\Wn[k]` | chain conditions                                                                           | keep; "W" for wiring/chain is fine. (W_∞) for the infinite form. |
| (R′_n)         | —          | hybrid chain family, verified for small n only                                                  | remark only. |

Principles for the final choice (to be settled with M.K.): one letter family per mechanism (commuting
auxiliary, half-matched auxiliary, auxiliary above a vertex, chains); no label that is a prefix of another
((Q) vs (Q1)); the witness table in §5.1 and the status table must use the same names.

Notation (17 Oct): the projection algebra of a regular *-semigroup is `\PA(S)` = $\mathsf{P}(S)$ in the paper; `\P` = $\mathcal P$ is reserved for partition monoids $\mathcal P_X$. The notes still use $\mathcal P$ for both.

## Decisions of 18 Oct (M.K.): final labels in the paper

| research | paper | macro |
|---|---|---|
| (Q1) | (PC) | `\Qone` |
| (S) | (Sq) | `\Wire` |
| (R) | (A1) | `\Rcond` |
| (R') | (A2) | `\Rp` |
| (R'') | (A2') | `\Rpp` |
| (V) | (X) | `\Vcond` |
| K4 | (Ab) | `\Kfour` |
| K0 | (Hm) | `\Kzero` |
| K0'' | (Hm') | `\Hmp` |
| (Tri), (P_1), (P_2), (Q), (E_1), (E_6), (W_n), (D_E) | unchanged | |

"matched" and `\mt` are kept (not "friendly"/F). Internal LaTeX labels (`subsec:K0`, `thm:K4`, ...) and the notes keep the research names.
