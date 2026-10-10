# 5. Counterexamples to "$|A|=k$", and the computer check

## 5.1 A single square band

$A=\{1,2,3,4,5\}$, $S=A\times A$, $(x,y)^*=(y,x)$, $(x,y)^+=(y\beta,x\beta^{-1})$ with $\beta=(1\,2)(3\,4\,5)$.

* $\phi(x,y)=\big((y,x)\big)^+=(x\beta,y\beta^{-1})$, so $\phi^n=\mathrm{id}$ iff $\beta^n=1$, i.e. $k=6$.
* A square band $A'\times A'$ with $|A'|=6$ has $36$ elements; $|S|=25$. So the conjecture fails.
* What the theorem gives instead: $\rho=\beta$ (on $P^*=\{(x,x)\}$), with cycles $\{1,2\}$ and $\{3,4,5\}$; the orbit bands are $\{1,2\}\times\{1,2\}$ and $\{3,4,5\}\times\{3,4,5\}$, on which $*$ and $+$ differ and $\phi$ has orders $2$ and $3$; $\operatorname{lcm}(2,3)=6=k$.

Any $\beta$ whose cycle type has lcm larger than every part, on a set too small to hold a $k\times k$ band, does the same (e.g. $\beta=(1\,2)(3\,4\,5)$ on $6$ points fixing $6$ gives $k=6$ with $|S|=36$, and then the whole $S$ is a band of the right size — so the size obstruction alone is not the full story; see 5.2).

## 5.2 Right size, but not flat

Take $S=B_2^0\cup B_3^0$, the $0$-direct union of a $2\times2$ and a $3\times3$ square band ($14$ elements; products across the two bands are $0$), with $*$ the swap on each band and $+$ the inversion twisted by $(1\,2)$ on $B_2$ and by $(3\,4\,5)$ on $B_3$. Then $k=6$, $\rho$ has cycles of lengths $2$ and $3$, and again there is no union of cycles of size $6$ (only $5$ projections).

To see the *other* failure mode, adjoin a third component, a $1\times1$ band $\{u\}$ with $u^*=u^+=u$ (or, as in the script, use $\mathcal M^0[\{1\};6,6;P]$ with $P$ block-diagonal with blocks of sizes $2,3,1$). Now the union $B$ of all cycles has size $6=k$ and $\rho|_B\ne\mathrm{id}$, but $\{ef:e,f\in B\}$ contains $0$ (products across components), so $B$ is not flat and there is no $*$,$+$-closed $6\times6$ band by Remark 3.5. The obstruction is no longer size — the $37$-element version has room for a $36$-element band — but the cross-orbit entries of $P$.

## 5.3 What the script `verify.py` does

`find_inversions(mul)` takes a bare multiplication table and finds **all** involutory antiautomorphic inversions by backtracking with propagation (an anti-automorphism is determined by its values on a generating set); it assumes none of the structure theory. `analyse_pair(mul, star, plus)` then computes $\phi$, $k$, $P^*$, $\rho(e)=e^{+*}e^+$, and asserts, for every pair of inversions found:

* $\rho$ is a permutation of $P^*$ and $k=\operatorname{lcm}$ of its cycle lengths (Theorem, part 1);
* for every cycle of length $m\ge2$, $\{e_ae_b\}$ has $m^2$ elements, is a rectangular band, is closed under $*$ and $+$ with $(e_ae_b)^*=e_be_a$ and $(e_ae_b)^+=e_{b-1}e_{a+1}$, and $\phi$ has order exactly $m$ on it (part 2);
* whether the original conjecture holds, via the criterion of Remark 3.5.

Semigroups tested (all pairs of inversions in each):

| semigroup | $|S|$ | #inversions | $(k;\ \text{cycle lengths of }\rho)$ observed | $|A|=k$ attainable? |
|---|---|---|---|---|
| square bands $n\times n$, $n=2,3,4$ | 4, 9, 16 | $n!$ | e.g. $n=4$: $(2;1,1,2),(2;2,2),(3;1,3),(4;4)$ | yes in all cases |
| $5\times5$ band, the pair of §5.1 | 25 | — | $(6;2,3)$ | **no** |
| $(5\times5\text{ band})^1$ | 26 | 120 | includes $(6;1,2,3)$ | **no** for that pair |
| $\mathcal M[S_3;3,3;P]$, $P$ flat | 54 | 6 | $(2;1,2)$, $(3;3)$ | yes |
| $\mathcal M[S_3;3,3;P']$, $P'$ not flat | 54 | 1 | — | — |
| $\mathcal M[\mathbb Z_3;3,3;P]$, all 27 skew-symmetric $P$ | 27 | 6 if flat, else 1 | $(2;1,2)$, $(3;3)$ | yes |
| $\mathcal M^0[\mathbb Z_2;4,4;P]$, $P$ block-diagonal | 33 | 4 | $(2;1,1,1,2)$, $(2;1,2,2)$ | yes |
| $B_2^0\cup B_3^0$ (§5.2, 14 elements) | 14 | 12 | includes $(6;1,2,3)$ | **no** for that pair |
| $\mathcal M^0[\{1\};6,6;P]$, blocks $2,3,1$ | 37 | 12 | includes $(6;1,1,2,3)$ | **no** for that pair |

Two side observations from the runs, both consistent with the theory: (i) on a $3$-row completely simple regular $*$-semigroup there are either $3!=6$ inversions (when $P$ is flat, i.e. $S\cong G\times(3\times3\text{ band})$) or just one — because any nontrivial $\rho$ on $3$ points, together with $(\ast)$, forces the whole $3\times3$ block to be flat; (ii) the group part never changes $k$, as predicted in §3.2.

Run with `python3 verify.py`; it finishes in well under a second and raises an `AssertionError` if any claim fails (none does).
