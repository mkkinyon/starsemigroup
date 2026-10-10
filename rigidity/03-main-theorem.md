# 3. The main theorem

Coordinates as in Lemmas A and B of `02-preliminaries.md`: $S=\mathcal M^0[G;I,I;P]$, $p_{ii}=1$, $p_{ji}=p_{ij}^{-1}$, $(i,g,j)^*=(j,g^{-1},i)$, and $+$ corresponds to a permutation $\rho$ of $I$ satisfying $(\ast)$. Write $e_i=(i,1,i)$ for the $*$-projections and $e_{ij}=(i,p_{ij},j)=e_ie_j$.

## 3.1 Orbit flatness

Call a subset $B\subseteq I$ **flat** if $p_{ij}\ne0$ and $p_{ij}p_{jl}=p_{il}$ for all $i,j,l\in B$. (Equivalently the $B\times B$ block of $P$ is $p_{ij}=c_ic_j^{-1}$ for some $c\colon B\to G$; equivalently the idempotents $\{e_{ij}: i,j\in B\}$ form a band, see 3.3.)

**Lemma C (orbits are flat).** *Every $\rho$-orbit $B=\{i_0,i_1=\rho i_0,\dots,i_{m-1}\}$ is flat.*

*Proof.* Write $p_{ab}$ for $p_{i_ai_b}$ with indices mod $m$, and $d_a:=p_{a,a+1}$; note $d_a\ne0$ because $p_{\rho i,i}\ne0$ for all $i$. Put $k=i_a$, $j=i_{b+1}$ in $(\ast)$: $\rho k=i_{a+1}$, $\rho^{-1}j=i_b$, so
$$p_{a+1,b}=p_{a+1,a}\,p_{a,b+1}\,p_{b+1,b},\qquad\text{i.e.}\qquad p_{a,b+1}=d_a\;p_{a+1,b}\;d_b\quad\text{(in }G^0).\tag{$\ast\ast$}$$
Claim: $p_{a,a+n}=d_ad_{a+1}\cdots d_{a+n-1}$ for all $a$ and all $n\ge0$ (empty product $=1$). For $n=0,1$ this is $p_{aa}=1$ and the definition of $d_a$. For $n\ge1$, $(\ast\ast)$ with $b=a+n$ gives $p_{a,a+n+1}=d_a\,p_{a+1,(a+1)+(n-1)}\,d_{a+n}=d_a(d_{a+1}\cdots d_{a+n-1})d_{a+n}$ by induction. In particular every $p_{ab}$ is nonzero, and for $b=a+n_1$, $c=b+n_2$ ($n_1,n_2\ge0$) we get $p_{ab}p_{bc}=(d_a\cdots d_{b-1})(d_b\cdots d_{c-1})=p_{a,a+n_1+n_2}=p_{ac}$. $\square$

(Taking $n=m$ shows $d_ad_{a+1}\cdots d_{a+m-1}=1$: the holonomy around the cycle is trivial.)

## 3.2 Consequences for $\phi$

By $(\dagger)$ of `02-preliminaries.md`, $\phi(i,g,j)=(\rho^{-1}i,\;p_{\rho^{-1}i,i}\,g\,p_{j,\rho j},\;\rho j)$. Iterating and using Lemma C to telescope ($p_{\rho^{-2}i,\rho^{-1}i}\,p_{\rho^{-1}i,i}=p_{\rho^{-2}i,i}$, all indices in one orbit):
$$\phi^n(i,g,j)=\big(\rho^{-n}i,\ p_{\rho^{-n}i,\,i}\;g\;p_{j,\,\rho^nj},\ \rho^nj\big)\qquad(n\ge0).$$
Hence $\phi^n=\mathrm{id}$ on $S$ iff $\rho^n=\mathrm{id}$ (if $\rho^n=\mathrm{id}$ the middle entry is $p_{ii}gp_{jj}=g$). So **the order of $\phi$ on a completely 0-simple regular $*$-semigroup equals the order of $\rho$**, the lcm of its cycle lengths; the group $G$ contributes nothing.

## 3.3 The orbit bands

**Proposition D.** *Let $B=\{i_0,\dots,i_{m-1}\}$ be a $\rho$-orbit with $m\ge2$ and put $E_B=\{e_{i_ai_b}:0\le a,b<m\}=\{e_{i_a}e_{i_b}\}$. Then:*

1. *$E_B$ is a square band: $e_{i_ai_b}\mapsto(a,b)$ is an isomorphism $E_B\to\mathbb Z_m\times\mathbb Z_m$.*
2. *$E_B$ is closed under $*$ and $+$, with $e_{i_ai_b}^*=e_{i_bi_a}$ and $e_{i_ai_b}^+=e_{i_{b-1}i_{a+1}}$.*
3. *On $E_B$ the two inversions are distinct, and $\phi|_{E_B}$ has order exactly $m$.*

*Proof.* (1) By Lemma C, $e_{i_ai_b}e_{i_ci_d}=(i_a,\,p_{ab}\,p_{bc}\,p_{cd},\,i_d)=(i_a,p_{ad},i_d)=e_{i_ai_d}$, and the $m^2$ elements lie in distinct $\mathcal H$-classes. (2) $(i_a,p_{ab},i_b)^*=(i_b,p_{ab}^{-1},i_a)=(i_b,p_{ba},i_a)$. For $+$, Lemma B gives $(i_a,p_{ab},i_b)^+=(i_{b-1},\ q_{i_b}^{-1}p_{ab}^{-1}q_{i_{a+1}}^{-1},\ i_{a+1})$ with $q_{i_b}=p_{b,b-1}$ and $q_{i_{a+1}}=p_{a+1,a}$, so the middle entry is $p_{b-1,b}\,p_{ba}\,p_{a,a+1}=p_{b-1,a+1}$ by flatness. (3) In the coordinates of (1), $*$ is $(a,b)\mapsto(b,a)$ and $+$ is $(a,b)\mapsto(b-1,a+1)$; they differ as $m\ge2$. Their composite $\phi$ is $(a,b)\mapsto(a-1,b+1)$, of order $m$. $\square$

## 3.4 Main theorem

**Theorem.** *Let $S$ be a finite regular $*$-semigroup, $+$ a second inversion with ${+}\ne{*}$, $\phi(x)=x^{*+}$ of order $k$, and $\rho\colon P^*\to P^*$, $\rho(e)=e^{+*}e^{+}$. Then $\rho$ is a permutation of $P^*$ preserving $\mathcal D$-classes, $\rho(e)=e\iff e^+=e$, and*

1. *$k$ is the order of $\rho$ (the lcm of its cycle lengths);*
2. *for every cycle $(e_0\,e_1\cdots e_{m-1})$ of $\rho$ with $m\ge2$, $E=\{e_ae_b\}$ is a square band $\cong\mathbb Z_m\times\mathbb Z_m$ closed under $*$ and $+$, on which $*$ and $+$ restrict to distinct inversions ($(e_ae_b)^*=e_be_a$, $(e_ae_b)^+=e_{b-1}e_{a+1}$) and on which $\phi$ has order exactly $m$;*
3. *at least one cycle of length $m\ge2$ exists; the set of such $m$ has lcm $k$; and $E\subseteq\langle e_0\rangle_{\cdot,*,+}$.*

*Proof.* Work one $\mathcal D$-class $D$ at a time (§2.2). On $D^0$ in the coordinates of Lemma A, $e_i\mapsto e_{\rho i}$ is the map $e\mapsto e^{+*}e^+$ (Lemma B), so $\rho$ is a permutation of $P^*\cap D$; $\rho(e_i)=e_i$ iff $e_i^+\in H_{ii}$ iff $e_i^+=e_i$ ($e_i^+$ is an idempotent and $H_{ii}$ contains only one). If ${*}={+}$ on $D$ then $\phi|_D=\mathrm{id}$ and $\rho|_D=\mathrm{id}$; otherwise $\rho|_D\ne\mathrm{id}$ by Fact 3 (applied to $D^0$). (1) is §3.2 together with $k=\operatorname{lcm}_D\operatorname{ord}(\phi|_D)$. (2) is Proposition D. For (3), some $D$ has ${*}|_D\ne{+}|_D$, so $\rho$ has a nontrivial cycle; the lcm statement is (1); and $e_{a+1}=\rho(e_a)=e_a^{+*}e_a^{+}$, so the whole cycle, and hence $E$, lies in the subalgebra generated by $e_0$. $\square$

**Corollary.** *The original conjecture (a $*$,$+$-closed square band $A\times A$ with $|A|=k$ and distinct restrictions) holds whenever $k$ is a prime power — in particular for $k=2$ and for $k$ prime — because then some cycle of $\rho$ has length exactly $k$.*

## 3.5 Remark: exactly when $|A|=k$ is attainable

Let $E\cong A\times A$ be any square band in $S$ closed under $*$ and $+$ on which they differ. $E$ lies in a single $\mathcal D$-class $D$ (it is a simple subsemigroup, and $\mathcal D=\mathcal J$). Distinct idempotents of $E$ are in distinct $\mathcal H$-classes of $S$, and two elements of $E$ that are $\mathcal L$-related in $E$ but in different rows cannot be $\mathcal R$-related in $S$; so the rows of $E$ are $|A|$ distinct $\mathcal R$-classes $B\subseteq I$ of $D$ and the columns are $|A|$ distinct $\mathcal L$-classes $C$. Since $*$ maps $H_{ij}\to H_{ji}$, $C=B$; since $+$ maps $H_{ij}\to H_{\rho^{-1}j,\rho i}$, $\rho B=B$. Each $H_{ij}$ ($i,j\in B$) is a group $\mathcal H$-class containing exactly one idempotent, $e_{ij}$, so $E=\{e_{ij}:i,j\in B\}$ and the band condition $e_{ij}e_{jl}=e_{il}$ says $B$ is flat. Finally ${*}\ne{+}$ on $E$ iff $\rho|_B\ne\mathrm{id}$. Conversely every flat $\rho$-invariant $B$ with $\rho|_B\ne\mathrm{id}$ gives such an $E$ (same computation as Proposition D). Therefore:

> *A $*$,$+$-closed square band $A\times A$ with $|A|=k$ and distinct restrictions exists iff some $\mathcal D$-class contains a union $B$ of $\rho$-cycles with $|B|=k$, $\rho|_B\ne\mathrm{id}$, and $B$ flat.*

Single cycles are always flat (Lemma C); unions of cycles need not be, and there need not be a union of the right size at all. Both failure modes occur in `05-counterexamples.md`.
