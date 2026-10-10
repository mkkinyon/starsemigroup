# 2. Preliminaries and the Rees-matrix normal form

**Terminology.** Throughout these notes, *inversion* is shorthand for *involutory antiautomorphic inversion*: a map $x\mapsto x^\dagger$ with $x^{\dagger\dagger}=x$, $(xy)^\dagger=y^\dagger x^\dagger$ and $xx^\dagger x=x$. All three properties are used in every structure statement (Lemma B's formula comes from $xx^+x=x$, condition $(\ast)$ from anti-automorphy, and involutivity is what makes ${*}\circ{+}$ an automorphism whose inverse is ${+}\circ{*}$), and the brute-force searches in the scripts enforce all three. A mere choice of inverses $x\mapsto x'\in V(x)$ is never meant; see §7 for why the two notions behave very differently.

## 2.1 Standard facts

Let $(S,*)$ be a regular $*$-semigroup. Applying $*$ to $xx^*x=x$ gives $x^*xx^*=x^*$, so $x^*\in V(x)$ (the set of inverses of $x$). Consequently $x\,\mathcal R\,xx^*$, $x\,\mathcal L\,x^*x$, and $x^*\in R_{x^*x}\cap L_{xx^*}$; also $x^*\,\mathcal D\,x$.

**Fact 1.** *Each $\mathcal R$-class and each $\mathcal L$-class of $S$ contains exactly one $*$-projection.* Existence: $xx^*\in R_x$ and $x^*x\in L_x$. Uniqueness: if $e,f\in P^*$ and $e\,\mathcal R\,f$ then $e=fe$, $f=ef$, so $e=e^*=(fe)^*=e^*f^*=ef=f$.

**Fact 2.** *Two inverses of $x$ lying in the same $\mathcal H$-class are equal* (Green's lemma / the standard description of $V(x)$).

Now let $+$ be a second inversion. Both $x^*$ and $x^+$ are inverses of $x$.

**Fact 3.** *If $P^*\subseteq P^+$ then ${*}={+}$.* Indeed $P^*$ and $P^+$ are both transversals of the $\mathcal R$-classes (Fact 1), so $P^*\subseteq P^+$ forces $P^*=P^+$. Then $xx^*$ and $xx^+$ are $+$-projections in $R_x$, hence equal, and likewise $x^*x=x^+x$; so $x^*,x^+$ are inverses of $x$ in the same $\mathcal H$-class $R_{x^*x}\cap L_{xx^*}$, hence equal by Fact 2.

So if ${*}\ne{+}$, some $e\in P^*$ satisfies $e^+\ne e$; more precisely, if $a^*\ne a^+$ then at least one of $aa^*$, $a^*a$ is not $+$-fixed (the argument of Fact 3 applied to $x=a$).

**Fact 4.** With $\phi(x)=x^{*+}$ (an automorphism, being a composite of two anti-automorphisms) we have $x^+=\phi(x^*)$ and $\phi^{-1}(x)=x^{+*}$. For $e\in P^*$: $\phi(e)=e^+$ and $\phi^{-1}(e)=e^{+*}$, and both lie in $V(e)$ — the first because $+$ is an inversion, the second because an anti-automorphism maps $V(e)$ onto $V(e^*)=V(e)$. Both are idempotents (anti-automorphisms preserve idempotents).

## 2.2 Reduction to one $\mathcal D$-class (finite case)

Assume $S$ finite and ${*}\ne{+}$. Since $*$ and $+$ preserve $\mathcal D$-classes, there is a $\mathcal D$-class $D$ with ${*}|_D\ne{+}|_D$. Both $*$ and $+$ map the ideals $J(x)=S^1xS^1$ and $I(x)=J(x)\setminus D$ ($x\in D$) to themselves, so both induce inversions on the principal factor $D^0=D\cup\{0\}$, which is completely 0-simple ($S$ finite, $D$ regular). A rectangular band inside $D^0$ not containing $0$ is a rectangular band inside $S$ with the same multiplication (a rectangular band containing $0$ is $\{0\}$, since $x0x=x$ forces $x=0$). So it suffices to prove everything for completely 0-simple $S$; the completely simple case is included (no zero, or ignore it).

## 2.3 Normal form for one inversion

Let $S=\mathcal M^0[G;I,\Lambda;P]$ be completely 0-simple with an inversion $*$. Write $H_{i\lambda}$ for the $\mathcal H$-class $\{(i,g,\lambda)\}$; it is a group iff $p_{\lambda i}\ne0$. By Fact 1 there is a bijection $\sigma\colon I\to\Lambda$ such that the $*$-projection of $R_i$ lies in $H_{i,\sigma i}$. For $x\in H_{i\lambda}$ we have $x^*\in R_{x^*x}\cap L_{xx^*}$, where $xx^*$ is the projection of $R_i$ (so $L_{xx^*}=L_{\sigma i}$) and $x^*x$ is the projection of $L_\lambda$ (so $R_{x^*x}=R_{\sigma^{-1}\lambda}$). Hence
$$x\in H_{i\lambda}\ \Longrightarrow\ x^*\in H_{\sigma^{-1}\lambda,\ \sigma i}.$$
Re-index $\Lambda$ by $I$ via $\sigma$, so that $\sigma=\mathrm{id}$, $p_{ii}\ne0$, and (after the Rees normalisation $(i,g,\lambda)\mapsto(i,gp_{\lambda\lambda},\lambda)$, which replaces $p_{\lambda j}$ by $p_{\lambda\lambda}^{-1}p_{\lambda j}$) $p_{ii}=1$ for all $i$.

Now $(i,g,j)^*=(j,f_{ij}(g),i)$ for some bijections $f_{ij}$. The inversion identity gives $(i,g,j)=(i,gp_{jj}f_{ij}(g)p_{ii}g,j)=(i,gf_{ij}(g)g,j)$, so $f_{ij}(g)=g^{-1}$:
$$(i,g,j)^*=(j,g^{-1},i).$$
Anti-automorphy: for $p_{jk}\ne0$, $\big((i,g,j)(k,h,l)\big)^*=(l,h^{-1}p_{jk}^{-1}g^{-1},i)$ must equal $(l,h^{-1},k)(j,g^{-1},i)=(l,h^{-1}p_{kj}g^{-1},i)$, and for $p_{jk}=0$ the right side must be $0$. Hence

**Lemma A.** *A completely 0-simple regular $*$-semigroup is, up to isomorphism, $\mathcal M^0[G;I,I;P]$ with $p_{ii}=1$, $p_{ji}=p_{ij}^{-1}$ (in $G^0$, with $p_{ij}=0\iff p_{ji}=0$), and $(i,g,j)^*=(j,g^{-1},i)$. Its $*$-projections are $e_i:=(i,1,i)$, and the idempotent of a group $\mathcal H$-class $H_{ij}$ is $e_{ij}:=(i,p_{ij},j)=e_ie_j$.*

(The converse is a direct check. Note $e_ie_j=(i,p_{ij},j)$ is idempotent whenever $p_{ij}\ne0$: $(i,p_{ij}p_{ji}p_{ij},j)=(i,p_{ij},j)$.)

## 2.4 All inversions on such an $S$

Keep the coordinates of Lemma A and let $+$ be any inversion on $S$. By the same reasoning there is a permutation $\rho$ of $I$ with the $+$-projection of $R_i$ in $H_{i,\rho i}$ (so $p_{\rho i,i}\ne0$), and $x\in H_{ij}\Rightarrow x^+\in H_{\rho^{-1}j,\rho i}$. Writing $(i,g,j)^+=(\rho^{-1}j,f(g),\rho i)$, the inversion identity $(i,g,j)(\rho^{-1}j,f(g),\rho i)(i,g,j)=(i,\,g\,p_{j,\rho^{-1}j}\,f(g)\,p_{\rho i,i}\,g,\,j)$ forces
$$(i,g,j)^+=\big(\rho^{-1}j,\ q_j^{-1}\,g^{-1}\,q_{\rho i}^{-1},\ \rho i\big),\qquad q_j:=p_{j,\rho^{-1}j}\ (\ne0).$$
This map is automatically an involution. Comparing $\big((i,g,j)(k,h,l)\big)^+=(\rho^{-1}l,\ q_l^{-1}h^{-1}p_{jk}^{-1}g^{-1}q_{\rho i}^{-1},\ \rho i)$ with
$(k,h,l)^+(i,g,j)^+=(\rho^{-1}l,\ q_l^{-1}h^{-1}\,q_{\rho k}^{-1}\,p_{\rho k,\rho^{-1}j}\,q_j^{-1}\,g^{-1}q_{\rho i}^{-1},\ \rho i)$ and using $q_{\rho k}=p_{\rho k,k}$, $p_{jk}^{-1}=p_{kj}$:

**Lemma B.** *With $S$ as in Lemma A, the inversions of $S$ are in bijection with the permutations $\rho$ of $I$ satisfying $p_{\rho i,i}\ne0$ for all $i$ and*
$$p_{\rho k,\,\rho^{-1}j}\;=\;p_{\rho k,\,k}\;p_{kj}\;p_{j,\,\rho^{-1}j}\qquad\text{for all }j,k\in I\quad(\ast)$$
*(an identity in $G^0$; in particular $p_{\rho k,\rho^{-1}j}=0\iff p_{kj}=0$). The inversion attached to $\rho$ is the formula displayed above; $\rho=\mathrm{id}$ gives $*$. Its projections are the idempotents $e_{i,\rho i}$; in terms of Fact 1, $\rho$ is the map $e_i\mapsto e_{\rho i}$, i.e.* $\rho(e)=e^{+*}e^{+}$ *(the $*$-projection $\mathcal L$-related to $e^+$), which is how $\rho$ was defined coordinate-free in the summary.*

Consistency check with your square-band example: $G$ trivial, $(\ast)$ is vacuous, every permutation $\rho$ of $I$ qualifies, giving $|I|!$ inversions, and the formula reads $(i,j)^+=(\rho^{-1}j,\rho i)$, i.e. your $(x,y)^+=(y\alpha,x\alpha^{-1})$ with $\alpha=\rho^{-1}$.

Finally, in these coordinates
$$\phi(i,g,j)=\big((i,g,j)^*\big)^+=(j,g^{-1},i)^+=\big(\rho^{-1}i,\ p_{\rho^{-1}i,\,i}\;g\;p_{j,\,\rho j},\ \rho j\big).\qquad(\dagger)$$
