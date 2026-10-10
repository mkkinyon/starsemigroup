# pa8/maxsub — explicit embeddings of the maximal subalgebras of P^ch_n and P^{R'}_n  (notes, Section 5.18)

- `extract.py fam n [mmax]` — SAT embeddings (pa_sat.solve) of the maximal subalgebras, printed as block lists (`extract.log`); used to find the patterns.
- `chemb.py nmax` — the explicit embeddings for P^ch_n (`make(n, omit)`), verified against the table for n <= nmax.
- `rpemb.py nmax` — the same for P^{R'}_n.
- `verify7.log` — both families verified for n <= 7 (98 maximal subalgebras, 0 wrong products).
Blocks: `[..]` transversal, `(..)` non-transversal; bottom elements are rank 0; pairs p_l, q_l are the T-blocks of x_l.
