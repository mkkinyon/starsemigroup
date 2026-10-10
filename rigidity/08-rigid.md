# 8. Rigid regular $*$-semigroups (unique inversion)

Call $(S,*)$ **rigid** if $*$ is its only inversion. Inverse semigroups are rigid; §7 shows the converse fails already for a 5-element band. This section collects what the structure theory says about rigidity, and an honest assessment of how much more there is to say.

## 8.1 What rigidity is

By Theorem G, $S$ is rigid iff $\mathcal A(S,*)=\{\mathrm{id}\}$: no non-identity permutation $\rho$ of $P^*$ makes $x\mapsto\rho^{-1}(xx^*)\,x\,\rho(x^*x)$ an automorphism. So rigidity is the absence of a certain kind of symmetry. Two layers:

* **locally rigid**: every principal factor $D^0$ is rigid, i.e. no $\mathcal D$-class admits a non-identity $\rho$ satisfying $(\ast)$ (equivalently, by Theorem E, no $\mathcal D$-class has a partition into $\rho$-cycles with all-ones blocks and a $\rho$-Hankel sandwich matrix after a gauge change, other than the trivial one);
* **rigid**: no non-identity $\rho$ is admissible globally.

Locally rigid $\Rightarrow$ rigid (a non-identity admissible $\rho$ is non-identity on some $\mathcal D$-class). The converse fails: the 5-element band $T$ is rigid but its band $\mathcal D$-class is the $2\times2$ band, which has two inversions. Note also that a $\mathcal D$-class with exactly two $\mathcal R$-classes is never locally rigid (a $2\times2$ block is always flat), so a rigid $S$ with such a $\mathcal D$-class is rigid only because of the gluing.

## 8.2 Rigidity is generic (completely simple case)

**Proposition.** *Let $|I|=n\ge3$ and $G$ a finite group. Among the $|G|^{\binom n2}$ sandwich matrices $P$ in the normal form of Lemma A (unit diagonal, $p_{ji}=p_{ij}^{-1}$), the fraction for which $\mathcal M[G;I,I;P]$ is not rigid is at most $(n!-1)/|G|$.* For $n=2$ the semigroup is never rigid; for $n=1$ it is a group.

*Proof.* Fix a non-identity permutation $\rho$ of $I$ and $u$ with $\rho u\ne u$. If $\rho^2u\ne u$, condition (Q) at $(u,\rho u)$ reads $p_{u,\rho^2u}=p_{u,\rho u}\,p_{\rho u,\rho^2u}$, an equation between three distinct edges of the complete graph on $I$. If $\rho^2u=u$, pick $v\notin\{u,\rho u\}$; (Q) at $(u,v)$ reads $p_{u,\rho v}=p_{u,\rho u}\,p_{\rho u,v}\,p_{v,\rho v}$, and the edge $\{u,\rho v\}$ differs from the other three edges appearing. In either case the equation determines one entry of $P$ uniquely in terms of others, so at most $|G|^{\binom n2-1}$ matrices satisfy it. Summing over the $n!-1$ non-identity $\rho$ gives the bound. $\square$

For $n=3$ the exact answer is $1-1/|G|$ (rigid iff $P$ is not flat, §6(d)); checked numerically for $G=\mathbb Z_2,\mathbb Z_3,\mathbb Z_5,\mathbb Z_7$. So among completely simple regular $*$-semigroups with at least three $\mathcal R$-classes, rigidity is the rule and a second inversion the exception — the opposite of the intuition one might get from bands.

## 8.3 Closure properties

* $S^0$ and $S^1$ are rigid iff $S$ is: the new element is alone in its $\mathcal D$-class, so any admissible $\rho$ fixes it, and $\phi_\rho$ is an automorphism of $S^0$ (resp. $S^1$) iff its restriction is one of $S$.
* Direct products: in the tested cases ($T\times T$, $T\times M$, $M\times M$ with $M=\mathcal M[\mathbb Z_2;3,3;P]$ rigid) the product of rigid semigroups is rigid. I do not have a proof: $\mathcal D$-classes of $S_1\times S_2$ are products $D_1\times D_2$, and a permutation of $P_1^*\times P_2^*$ need not be a product of permutations (for $B_2\times B_2\cong 4\times4$ band there are $24$ admissible $\rho$ but only $4$ product ones), so the argument would have to use the gluing. This is a natural open question.
* Not closed under subsemigroups or $*$-subsemigroups ($B_2\subset T$), nor under $*$-homomorphic images (every $\mathcal M[G;I,I;P]$ maps onto the square band $I\times I$, which has $|I|!$ inversions), nor under ideals in general.

So rigidity is not a variety- or quasivariety-like property, and it is not inherited in either direction. This is the main reason I would not expect a structure theory of rigid regular $*$-semigroups that goes beyond the general theory.

## 8.4 Assessment

The situation seems to be exactly parallel to *asymmetric graphs* (graphs with trivial automorphism group): by Theorem G, inversions are certain automorphisms of $S$, so "unique inversion" is a "no symmetry" condition; such conditions are generic (§8.2), non-hereditary (§8.3), and have no structure theory of their own — the structure theory is that of the ambient class, plus a symmetry computation. What the present notes add is that the symmetry computation is completely explicit: rigidity of $S$ is decided by (a) the $\rho$-Hankel analysis of each sandwich matrix (Theorem E) and (b) the equivariance of the Schützenberger representations (Theorem G′). In particular:

* if every $\mathcal D$-class of $S$ is locally rigid, $S$ is rigid, and this is a condition on sandwich matrices alone;
* if $S$ is a monoid and, for every $\mathcal D$-class $D$, the group of units acts on $P^*\cap D$ with trivial centraliser in $\mathrm{Sym}(P^*\cap D)$, then $S$ is rigid (§7);
* the only way for a *band* $\mathcal D$-class (or any $\mathcal D$-class with a flat cycle) to sit inside a rigid $S$ is through such gluing constraints, as in the 5-element example.

Where a deeper theory might exist is for the *intermediate* class of locally rigid semigroups, since local rigidity is a property of the principal factors alone and behaves better under the usual constructions (for instance it is inherited by ideals, whose principal factors are principal factors of $S$, and it passes to $S^0$ and $S^1$). Even there, though, the content reduces to a statement about sandwich matrices: no cycle of any permutation of the rows is flat and compatible in the sense of Theorem E. I would be happy to be proved wrong by a more clever invariant, but I do not see one.

## Computer check (`verify4.py`)

Confirms: the 5-element band has a unique inversion and every band element has two inverses; $T\times T$, $T\times M$, $M\times M$ are rigid; and the rigid fraction of 3-row sandwich matrices over $\mathbb Z_q$ is exactly $1-1/q$ for $q=2,3,5,7$.
