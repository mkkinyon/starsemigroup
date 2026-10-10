# 7. Global structure: inversions as twists of $*$ by permutations of $P^*$

$(S,*)$ is a finite regular $*$-semigroup, $P^*$ its set of projections. For a permutation $\rho$ of $P^*$ define
$$\phi_\rho(x):=\rho^{-1}(xx^*)\;x\;\rho(x^*x),\qquad x^{+_\rho}:=\phi_\rho(x^*)=\rho^{-1}(x^*x)\;x^*\;\rho(xx^*).$$

## Theorem G

1. *Every inversion $+$ of $S$ equals $+_\rho$ for exactly one permutation $\rho$ of $P^*$, namely $\rho(e)=e^{+*}e^{+}$; and then $\phi_\rho(x)=x^{*+}$ is the automorphism $\phi$ of the earlier sections.*
2. *Conversely, for a permutation $\rho$ of $P^*$, the map $+_\rho$ is an inversion if and only if $\phi_\rho$ is an automorphism of $S$.*

So the inversions of $(S,*)$ are in bijection with $\mathcal A(S,*):=\{\rho\in\mathrm{Sym}(P^*):\phi_\rho\in\mathrm{Aut}(S)\}$. In particular $|\mathrm{Inv}(S)|\le|\mathrm{Aut}(S)|$.

*Proof.* (1) Let $+$ be an inversion and $\rho(e)=e^{+*}e^+$. By Lemma B, on each $\mathcal D$-class $\rho$ is the permutation $e_i\mapsto e_{\rho i}$ of Lemma A's coordinates, and $(i,g,j)^+=(\rho^{-1}j,\ p_{\rho^{-1}j,j}\,g^{-1}\,p_{i,\rho i},\ \rho i)$ (since $q_j^{-1}=p_{\rho^{-1}j,j}$, $q_{\rho i}^{-1}=p_{i,\rho i}$). But for $x=(i,g,j)$ we have $x^*x=e_j$, $xx^*=e_i$, and
$$e_{\rho^{-1}j}\,(j,g^{-1},i)\,e_{\rho i}=(\rho^{-1}j,\ p_{\rho^{-1}j,j}\,g^{-1}\,p_{i,\rho i},\ \rho i),$$
so $x^+=x^{+_\rho}$. Uniqueness: $\rho$ is recovered from $+$ by the formula defining it. Replacing $x$ by $x^*$ gives $x^{*+}=\phi_\rho(x)$.

(2) Suppose $\phi:=\phi_\rho\in\mathrm{Aut}(S)$. Since $\phi(x)\in SxS$, $\phi$ moves every $\mathcal J$-class downwards; an automorphism permutes the finite poset of $\mathcal J$-classes, and a permutation of a finite poset with $\phi(J)\le J$ for all $J$ is the identity (each orbit is a descending cycle). So $\phi$ preserves $\mathcal D$-classes, hence $\rho^{-1}(e)\,e\,\rho(e)=\phi(e)\in D_e$, hence $\rho(e)\ge_{\mathcal J}e$ for all $e$, and the same cycle argument shows $\rho$ preserves $\mathcal D$-classes. In Lemma A's coordinates on $D^0$, $\phi(i,g,j)=e_{\rho^{-1}i}(i,g,j)e_{\rho j}=(\rho^{-1}i,\ p_{\rho^{-1}i,i}\,g\,p_{j,\rho j},\ \rho j)$, and $\phi(e_i)\in D$ forces $p_{\rho^{-1}i,i}\ne0\ne p_{i,\rho i}$. Now $x\mapsto\phi(x^*)$ is an anti-automorphism, and
$$x\,\phi(x^*)\,x=(i,\ g\,p_{j,\rho^{-1}j}\,p_{\rho^{-1}j,j}\,g^{-1}\,p_{i,\rho i}\,p_{\rho i,i}\,g,\ j)=(i,g,j)=x,$$
$$\phi(x^*)^*=\big(\rho^{-1}(x^*x)\,x^*\,\rho(xx^*)\big)^*=\rho(xx^*)\,x\,\rho^{-1}(x^*x)=\phi_{\rho^{-1}}(x),$$
and $\phi_{\rho^{-1}}\phi_\rho=\mathrm{id}$ by the coordinate formula, so $x^{++}=\phi(\phi_{\rho^{-1}}(x))=x$. Thus $+_\rho$ is an inversion; its associated permutation is $e\mapsto e^{+*}e^{+}=e_{\rho i}e_ie_{\rho^{-1}i}e_ie_{\rho i}=e_{\rho i}=\rho(e)$. Conversely, if $+_\rho$ is an inversion then $\phi_\rho(x)=x^{*+_\rho}$ is an automorphism. $\square$

## Reducing "$\phi_\rho\in\mathrm{Aut}(S)$" to local and gluing conditions

**Lemma H.** *Let $S$ be a regular semigroup and $\phi\colon S\to S$ a map with $\phi(ab)=\phi(a)\phi(b)$ whenever (i) $ab\,\mathcal R\,a$, or (ii) $ab\,\mathcal L\,b$, or (iii) $a,b$ are idempotents (projections suffice in a regular $*$-semigroup). Then $\phi$ is an endomorphism.*

*Proof.* Given $a,b$, pick $a'\in V(a)$, $b'\in V(b)$ (in the $*$-case $a'=a^*$, $b'=b^*$) and put $f=a'a$, $e=bb'$; then $af=a$, $eb=b$, $ab=(afe)b$. One checks $afe\,\mathcal L\,fe$ (as $fe=a'(afe)$), $(afe)b\,\mathcal R\,afe$ (as $afe=ae=(ab)b'$), $af\,\mathcal L\,f$ and $eb\,\mathcal R\,e$. Hence $\phi(ab)\overset{(i)}=\phi(afe)\phi(b)\overset{(ii)}=\phi(a)\phi(fe)\phi(b)\overset{(iii)}=\phi(a)\phi(f)\phi(e)\phi(b)\overset{(ii),(i)}=\phi(af)\phi(eb)=\phi(a)\phi(b)$. $\square$

**Theorem G′.** *For a permutation $\rho$ of $P^*$, $\phi_\rho\in\mathrm{Aut}(S)$ iff*

* *(L) $\rho$ preserves each $\mathcal D$-class and is admissible on each principal factor in the sense of Theorem E (equivalently, $\phi_\rho$ restricts to an automorphism of every $D^0$); and*
* *(G) $\phi_\rho(ab)=\phi_\rho(a)\phi_\rho(b)$ for all pairs $a,b$ from different $\mathcal D$-classes with $ab\,\mathcal R\,a$ or $ab\,\mathcal L\,b$, and for all pairs of projections $a,b$.*

*Proof.* (L) makes $\phi_\rho$ a bijection of $S$ and multiplicative on pairs $a,b\in D$ with $ab\in D$ (then $ab\,\mathcal R\,a$ by stability); together with (G) all pairs of Lemma H are covered. $\square$

**The gluing condition in Schützenberger form.** Fix $D$ with the coordinates of Theorem E for $\rho|_D$, so $\phi_\rho(i,g,j)=(\rho^{-1}i,g,\rho j)$. For $s\in S$, left multiplication by $s$ acts on $D^0$ by a row-monomial matrix: $s\cdot(i,g,j)=(s\cdot i,\ \omega_i(s)\,g,\ j)$ or $0$, with $s\cdot i\in I$ and $\omega_i(s)\in G$ independent of $g,j$ (Green's lemma). Multiplicativity of $\phi=\phi_\rho$ on pairs $(s,x)$, $x\in D$, $sx\in D$, reads
$$\rho^{-1}(s\cdot i)=\phi(s)\cdot\rho^{-1}(i),\qquad \omega_i(s)=\omega_{\rho^{-1}i}(\phi(s)),$$
i.e. the row representation of $\phi(s)$ on $D$ is the conjugate by $\rho$ of that of $s$; dually for columns. In particular, **if $\phi(s)=s$ then the row and column representations of $s$ on every $\mathcal D$-class commute with $\rho$.** This applies to every $s$ in a $\mathcal D$-class on which $\rho$ is trivial — for instance every $\mathcal D$-class consisting of a single $\mathcal H$-class (the group of units of a monoid, any $\mathcal D$-class that is a group): $\phi_\rho(i,g,i)=(i,g,i)$ there, since $|I|=1$ forces $\rho=\mathrm{id}$.

## A family where the gluing condition is everything

Let $H\le\mathrm{Sym}(A)$ act on a set $A$ and let $S=H\cup(A\times A)$ with $H$ a group, $A\times A$ the square band, and
$$h\,(a,b)=(ha,\,b),\qquad (a,b)\,h=(a,\,h^{-1}b).$$
This is a semigroup (the band is an ideal), and $h^*=h^{-1}$, $(a,b)^*=(b,a)$ is an inversion. Locally there is no constraint: the band admits all $|A|!$ permutations of its projections $\{(a,a)\}$, and $H$ admits only the identity. Globally, Theorem G says $\rho\leftrightarrow\alpha\in\mathrm{Sym}(A)$ works iff $\phi_\rho(a,b)=(\alpha^{-1}a,\alpha b)$ is compatible with the action: $\phi(h(a,b))=(\alpha^{-1}ha,\alpha b)$ must equal $h\,\phi(a,b)=(h\alpha^{-1}a,\alpha b)$. Hence
$$\mathrm{Inv}(S)\;\longleftrightarrow\;C_{\mathrm{Sym}(A)}(H).$$
For $|A|=3$: $H=1,\ \langle(01)\rangle,\ \langle(012)\rangle,\ \mathrm{Sym}(3)$ give $6,2,3,1$ inversions (verified by brute force). So the number of inversions is not determined by the principal factors, and no gluing condition weaker than "$\phi_\rho$ is an automorphism" can be expected in general: the answer here is a centraliser in $\mathrm{Aut}(S)$.

## Further consequences

* **Closure properties.** $\mathcal A(S,*)$ is closed under powers ($\phi_{\rho}^n=\phi_{\rho^n}$, using flatness of orbits), hence under inverses, and under conjugation by automorphisms of $S$ commuting with $*$. It is not closed under composition in general (§6(e)).
* **$k$ and the orbit bands** (Theorem of §3) are now statements about $\rho\in\mathcal A(S,*)$: $k=\operatorname{ord}(\rho)$, and each cycle $(e_0\cdots e_{m-1})$ of $\rho$ carries the band $\{e_ae_b\}$.
* **$\rho$ preserves the natural order, but not the projection algebra.** Recall the natural order on $P^*$: $e\le f$ iff $e=ef=fe$. *Every admissible $\rho$ is an automorphism of the poset $(P^*,\le)$.* Indeed, let $e\le f$ and put $u=e^+$, $v=f^+$. Applying the anti-automorphism $+$ to $e=ef=fe$ gives $u=vu=uv$, and applying $*$ gives $u^*=v^*u^*=u^*v^*$. With $\rho(e)=u^*u$, $\rho(f)=v^*v$:
$$\rho(e)\rho(f)=u^*(uv)v^*v=u^*u\,(vv^*v)=u^*uv=u^*u=\rho(e),\qquad
\rho(f)\rho(e)=v^*v\,(v^*u^*)u=(v^*vv^*)u^*u=(uv)^*u=u^*u=\rho(e),$$
so $\rho(e)\le\rho(f)$. Since $\rho^{-1}$ is the permutation attached to the inversion ${*}{+}{*}$, it is order-preserving too. By contrast, $\rho$ need **not** preserve the projection-algebra operation $e\mapsto fef$: in $\mathcal M^0[\mathbb Z_3;6,6;P]$ with two $3$-cycles glued by $f=(0,t,0)$, two of the seven admissible $\rho$ fail $\rho(fef)=\rho(f)\rho(e)\rho(f)$, because they change the zero pattern of $P$ — (H) only forces $p_{\rho i,\rho j}=p_{i,\rho^2j}$. The two facts are compatible: distinct projections in one $\mathcal D$-class are incomparable, so the order lives entirely between $\mathcal D$-classes (where $\rho$ behaves), while $fef$ still detects whether $p_{ij}=0$ inside a $\mathcal D$-class (where $\rho$ may scramble it). Numerically checked on $(5\times5\text{ band})^1$, $H\cup(3\times3)$ and the $\mathcal M^0$ example above.
* **Uniqueness.** $S$ has a unique inversion iff $\mathcal A(S,*)=\{\mathrm{id}\}$; a nontrivial $\rho$ needs a $\mathcal D$-class with a flat $\rho$-cycle of length $\ge2$ (Lemma C) whose Schützenberger representations are $\rho$-equivariant. Two simple sufficient conditions for uniqueness: every $\mathcal D$-class is a single $\mathcal H$-class (semilattices of groups); or $S$ is a monoid whose unit group acts on the projections of every $\mathcal D$-class with trivial centraliser in $\mathrm{Sym}(P^*\cap D)$ (as $\mathrm{Sym}(3)$ does in the family above).

* **Unique inversion does not mean inverse.** If $S$ is not inverse, some $x$ has $|V(x)|>1$, so there are always maps $x\mapsto x'\in V(x)$ other than $*$; but such a broad-sense inversion need not be involutory or antiautomorphic, and its existence says nothing about a second inversion in our sense. Indeed every $\mathcal M[\mathbb Z_3;3,3;P]$ with non-flat $P$, and $\mathrm{Sym}(3)\cup(3\times3\text{ band})$ above, have exactly one inversion without being inverse. The smallest example is a **5-element band**: $S=\{s\}\cup(\{0,1\}\times\{0,1\})$ with $s^2=s$, $s(a,b)=(0,b)$, $(a,b)s=(a,0)$, and $s^*=s$, $(a,b)^*=(b,a)$. It is a band with two $\mathcal D$-classes and non-commuting idempotents, so not inverse; a second inversion would need the swap of $\{0,1\}$ to commute with the row action of $s$, which is the constant map $0$ — impossible. (Brute force: one inversion, and $|V(x)|=4$ for each of the four band elements, as in any rectangular band.) Nothing smaller works: the only non-inverse regular $*$-semigroup of order $\le4$ is the $2\times2$ band, which has two inversions.

## Summary: the structure theory

A pair of inversions on a finite regular $*$-semigroup is the same as a pair $\big((S,*),\rho\big)$ with $\rho$ a permutation of the projection set such that $\phi_\rho\colon x\mapsto\rho^{-1}(xx^*)\,x\,\rho(x^*x)$ is an automorphism. This splits into:

1. **local data** — on each $\mathcal D$-class, a partition into $\rho$-cycles and a $\rho$-Hankel sandwich matrix with all-ones cycle blocks (Theorem E); the cycles are the orbit bands and $k=\operatorname{ord}(\rho)$;
2. **gluing data** — equivariance of the Schützenberger representations under $\rho$ (Theorem G′ / Lemma H), a condition that genuinely depends on the whole of $S$ and can cut the local count down to $1$.

## Computer check (`verify3.py`)

For square bands, the $14$-element $0$-direct union, the four $H\cup(3\times3)$ semigroups, the non-orthodox $\mathcal M[\mathbb Z_3;4,4;P]$ and the $109$-element $\mathcal M^0[\mathbb Z_3;6,6;P]$: every brute-force inversion equals $+_\rho$ for $\rho(e)=e^{+*}e^+$; for every permutation $\rho$ of $P^*$ (when $|P^*|!$ is small), "$+_\rho$ is an inversion" ⟺ "$\phi_\rho$ is an automorphism" ⟺ "$\phi_\rho$ is bijective and multiplicative on the pairs of Lemma H"; the counts for $H\cup(3\times3)$ equal $|C_{\mathrm{Sym}(3)}(H)|$; and the projection-algebra failure is exhibited. All assertions pass.
