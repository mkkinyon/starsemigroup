# 6. All inversions on a completely 0-simple regular $*$-semigroup

Setting as in Lemma A: $S=\mathcal M^0[G;I,I;P]$, $p_{ii}=1$, $p_{ji}=p_{ij}^{-1}$ (zeros symmetric), $(i,g,j)^*=(j,g^{-1},i)$, $e_i=(i,1,i)$. By Lemma B the inversions of $S$ correspond to permutations $\rho$ of $I$ with $p_{\rho i,i}\ne0$ satisfying $(\ast)$. Substituting $k=\rho^{-1}u$, $j=\rho v$ in $(\ast)$ and inverting, $(\ast)$ is equivalent to its **quadrilateral form**
$$p_{u,\rho v}\;=\;p_{u,\rho u}\;p_{\rho u,v}\;p_{v,\rho v}\qquad\text{for all }u,v\in I:\tag{Q}$$
the path $u\to\rho u\to v\to\rho v$ has the same holonomy as the edge $u\to\rho v$. Think of $P$ as a $G^0$-valued connection on the complete graph on $I$; a "gauge change" $p_{ij}\mapsto c_ip_{ij}c_j^{-1}$ ($c\colon I\to G$) is the Rees isomorphism $(i,g,j)\mapsto(i,c_igc_j^{-1},j)$, which preserves the normal form of Lemma A and the formula for $*$. A set $B\subseteq I$ is *flat* if all $p_{ij}$ ($i,j\in B$) are nonzero and $p_{ij}p_{jl}=p_{il}$ on $B$; equivalently $P|_{B\times B}$ is gauge-equivalent to the all-ones block.

For cycles $C,C'$ of $\rho$ with chosen base points $u\in C$, $v\in C'$, put
$$T_{u,v}(a,b)\;:=\;p_{u,\rho^au}\;p_{\rho^au,\rho^bv}\;p_{\rho^bv,v}\in G^0,$$
the holonomy of the path $u\to\rho^au\to\rho^bv\to v$ (well defined mod $|C|$ in $a$ and mod $|C'|$ in $b$ once $C,C'$ are flat).

## Theorem E

*Let $\rho$ be a permutation of $I$ with $p_{\rho i,i}\ne0$ for all $i$. The following are equivalent.*

1. *$\rho$ arises from an inversion of $S$, i.e. $(\ast)$ / (Q) holds.*
2. *Every $\rho$-cycle is flat, and for any two cycles $C,C'$ with base points $u,v$ the holonomy $T_{u,v}(a,b)$ depends only on $a+b$ (hence only on $a+b \bmod \gcd(|C|,|C'|)$).*
3. *After a gauge change, $p_{ij}=1$ whenever $i,j$ lie in the same $\rho$-cycle, and*
$$p_{\rho i,\,j}=p_{i,\,\rho j}\qquad\text{for all }i,j\in I,\tag{H}$$
*i.e. $P$ is constant on the orbits of $(i,j)\mapsto(\rho^{-1}i,\rho j)$ — which is precisely the action of $\phi$ on $\mathcal H$-classes. In these coordinates*
$$\phi(i,g,j)=(\rho^{-1}i,\ g,\ \rho j),\qquad (i,g,j)^+=(\rho^{-1}j,\ g^{-1},\ \rho i).$$

*Proof.* (1)⇒(2): cycles are flat by Lemma C. Fix $u\in C$, $v\in C'$. Using flatness on $C$ and $C'$ to expand $p_{u,\rho^{a+1}u}=p_{u,\rho^au}\,p_{\rho^au,\rho^{a+1}u}$ and $p_{\rho^bv,v}=p_{\rho^bv,\rho^{b+1}v}\,p_{\rho^{b+1}v,v}$, one sees that $T_{u,v}(a+1,b)=T_{u,v}(a,b+1)$ is exactly (Q) at the pair $(\rho^au,\rho^bv)$. So $T$ is constant along anti-diagonals: $T(a,b)=T(a+b,0)=T(0,a+b)$, and the first expression is periodic mod $|C|$, the second mod $|C'|$, in $a+b$.
(2)⇒(1): every pair $(u',v')$ is $(\rho^au,\rho^bv)$ for cycles' base points, and (Q) at $(u',v')$ is $T(a+1,b)=T(a,b+1)$, as just shown.
(2)⇔(3): take the gauge $c_i:=p_{ui}$ where $u$ is the base point of the cycle of $i$. Flatness gives $p_{ij}=p_{iu}p_{uj}=c_i^{-1}c_j$ on each cycle, so the new $p'_{ij}=c_ip_{ij}c_j^{-1}=1$ there; and $p'_{\rho^au,\rho^bv}=T_{u,v}(a,b)$ by definition, so (H) for $p'$ is $T(a+1,b)=T(a,b+1)$. Conversely, given (3), (Q) reads $p_{u,\rho v}=p_{\rho u,v}$, which is (H); and (Q) is invariant under gauge changes (it expresses that a certain map is an inversion). The formulas for $\phi$ and $+$ come from $(\dagger)$ and Lemma B with all $p_{i,\rho^{\pm1} i}=1$. $\square$

## Consequences and reformulations

**(a) A normal form for a pair of inversions.** In the coordinates of (3) both inversions are "in normal form at once": $*$ swaps rows and columns, $+$ swaps them and then relabels by $\rho$, and $\phi$ is the pure coordinate permutation $(i,g,j)\mapsto(\rho^{-1}i,g,\rho j)$. Condition (H) is exactly the condition that this coordinate permutation is an automorphism. So, conceptually:

> *A second inversion on $S$ is the same thing as a permutation $\rho$ of the index set $I$ such that, after a gauge change, the sandwich matrix is $\rho$-Hankel — $p_{\rho i,j}=p_{i,\rho j}$ — with all-ones blocks on the $\rho$-cycles. The inversion is distinct from $*$ iff $\rho\ne\mathrm{id}$.*

**(b) The free parameters.** Choose a partition of $I$ into cycles (i.e. $\rho$) and, for each ordered pair of distinct cycles $(C,C')$, a function
$$f_{CC'}\colon\ \mathbb Z/\gcd(|C|,|C'|)\longrightarrow G^0,\qquad f_{C'C}(n)=f_{CC'}(n)^{-1},$$
and set $p_{\rho^au,\rho^bv}=f_{CC'}(a+b)$, $p\equiv1$ on $C\times C$. Every such choice gives a completely 0-simple regular $*$-semigroup carrying the second inversion $\rho$, and every $(S,*,+)$ with a completely 0-simple $S$ arises this way. (Regularity of $P$ is automatic from $p_{ii}=1$.) The orbit bands of `03-main-theorem.md` are the diagonal blocks; the $f_{CC'}$ describe how they are glued. Note the gluing between cycles of coprime lengths is a single element of $G^0$.

**(c) Beyond rectangular groups.** The theorem produces completely simple regular $*$-semigroups with two inversions that are *not* orthodox. The smallest kind: $G=\mathbb Z_3=\langle t\rangle$, $I=\{u,\rho u,v,\rho v\}$ (two 2-cycles), $f_{CC'}(0)=1$, $f_{CC'}(1)=t$:
$$P=\begin{pmatrix}1&1&1&t\\1&1&t&1\\1&t^{-1}&1&1\\t^{-1}&1&1&1\end{pmatrix},$$
which is not flat (the triangle $u,\rho u,v$ has holonomy $t$), so $S=\mathcal M[\mathbb Z_3;4,4;P]$ ($48$ elements) is not a rectangular group; it has exactly two inversions, $*$ and the one with $\rho=(u\ \rho u)(v\ \rho v)$, with $k=2$. The two $2\times2$ orbit bands sit inside a semigroup whose idempotents do not form a band.

**(d) Why $3$ rows gave "$6$ or $1$".** With $|I|=3$ any nontrivial $\rho$ is a transposition or a $3$-cycle. A $3$-cycle makes $I$ one flat cycle; a transposition $(u\ \rho u)$ fixing $w$ makes $\{u,\rho u\}$ flat, and (Q) at $(w,u)$ with $\rho w=w$ reads $p_{w,\rho u}=p_{ww}\,p_{wu}\,p_{u,\rho u}=p_{wu}\,p_{u,\rho u}$, so the triangle $\{w,u,\rho u\}$ is flat too. Either way $P$ is flat, $S\cong G\times(3\times3\text{ band})$, and all $3!$ permutations occur. For $|I|\ge4$ this collapse no longer happens, as (c) shows.

**(e) Structure of the set of inversions.** If $\rho$ is admissible so is every power $\rho^n$: in the coordinates of (3), $x\mapsto\phi^n(x^*)$ is $(i,g,j)\mapsto(\rho^{-n}j,g^{-1},\rho^ni)$, visibly an inversion. So the inversions of $S$ form a union of "cyclic families" $\{x\mapsto\phi^n(x^*)\}_{n}$ through $*$. They are **not** in general closed under the natural composition $\rho_1\rho_2$: e.g. two $3$-cycles glued by $f=(0,t,0)$ over $\mathbb Z_3$ admit $7$ permutations — the six that act on both cycles "in step" plus one that swaps the cycles — and composing the swap with the others leaves the admissible set. (This is in contrast to the square band, where all of $\mathrm{Sym}(I)$ occurs.)

**(f) Whole finite $S$.** Everything applies $\mathcal D$-class by $\mathcal D$-class: a second inversion on a finite regular $*$-semigroup is a family of admissible $\rho_D$ on the principal factors, with the constraint that the resulting anti-automorphism respects products between different $\mathcal D$-classes. The theorem above says nothing about that last constraint; that is where the non-completely-simple structure enters.

## Computer check (`verify2.py`)

For each of the following, the script (i) finds all inversions by brute force on the multiplication table, reads off $\rho$ from the $+$-projections, and confirms the set of $\rho$'s equals the set of permutations satisfying $(\ast)$; (ii) checks, for *every* permutation of $I$, that $(\ast)$ holds iff (2) holds; (iii) performs the gauge change of (3) and checks the all-ones cycle blocks and (H); (iv) checks closure under powers and tests closure under composition:

* the $4\times4$ example of (c) over $\mathbb Z_3$ — exactly $2$ inversions, $S$ not orthodox;
* six random "Hankel" constructions of (b) over $\mathbb Z_3$ and $S_3$ with cycle types $[3,3],[1,2,2],[2,2],[1,3]$, including ones with zero entries — the built-in $\rho$ is always admissible;
* all $27$ skew-symmetric $P$ over $\mathbb Z_3$ with $3$ rows.

All assertions pass; the $[3,3]$ example is the one exhibiting non-closure under composition in (e).
