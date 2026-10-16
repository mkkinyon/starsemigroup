# Context for the cold read of 16 Oct 2026

You are an independent referee. The project studies which finite projection algebras (the sets of projections of
regular *-semigroups with the operations theta_p(q) = pqp) embed in the projection algebra P(P_X) of a partition
monoid. The notes (notes-embedding.tex / .pdf, 85 pages) are the authors' running record; the authors are M. Kinyon
(Prover9/Mace4 computations, cited "M.K.") and an AI assistant (hand proofs and Python computations). Two earlier
cold reads exist (previous-cold-read-11-Oct.md is the most recent; it covered Sections 5.14-5.19). Please do not
rely on the previous reader's verdicts; form your own.

Conventions (Lemma 1.1 of the notes): a projection p of P_X is a partition eps_p of X with some blocks marked
transversal (T(p)-blocks, their union is supp p) and the rest nontransversal (N(p)-blocks); rk p = number of
T-blocks. theta_p(q) = pqp; "q <= p" means theta_p(q) = q; "p ~ q" means pq = qp; "p |><| q" (matched) means
pqp = p and qpq = q. Lemma 1.1(a) describes theta_p(q) blockwise; Lemma 1.1(b) describes the classes of
eps_p v eps_q when p ~ q (four types (i)-(iv)); Lemma 1.1(c) says a matched pair gives a bijection of T-blocks.
In Prover9 files the notation is x*y = theta_y(x). The projection-algebra axioms used (Prover9 labels PA2-PA5)
are listed at the top of code/k4.pf2.

What is NEW since the cold read of 11 Oct, and what you are asked to check (in order of importance):

1. Section 5.21 (subsec:K4), Theorem 5.49: "K4 holds in every partition monoid", proved on 16 Oct by a hand
   argument with three labels per point. This is the main item. Read the proof (Steps 1-6) with maximal
   scepticism; every step should be checkable from Lemma 1.1, Lemma 5.40 (the counting invariant) and the
   hypotheses. The algebraic inputs are: theta_z(c) = b (M.K., Prover9, file k4.pf1 -- NOT available to you;
   treat it as a cited lemma and say whether anything else depends on it), the identity theta_y(u) = theta_y(z)
   (derived in Step 1 from the axioms; please verify that derivation), and the general fact theta_p(q) |><| theta_q(p).
   The consequences claimed: (E6) proved, P_8^6 minimal non-embeddable.
   The 37,324 instances of the K4 hypotheses in P(P_4) are in code/k4inst4.pkl (a pickled list of dicts
   with keys a,b,c,y,z; projections in the representation of code/fast.py: (tuple of block bitmasks, supp bitmask)).
   code/k4chk.py checks the lemmas of the proof on them. Note that in P(P_m), m <= 7, the statement being proved
   is itself verified (SAT), so instances can only test the lemmas, not the final contradiction; in all those
   instances |I_j| = 1. You may write your own checks (fast.py has projections(m), theta, join, commute, matched,
   show, parse).
2. The paragraph "K4: reductions, and the case z = b" at the end of Section 5.20: the rank lemma, the case z = b,
   and the structural facts. Also M.K.'s Prover9 proof code/k4.pf2 (K4-hypotheses + c*z=b + (b*y)*a=a |- a|><|b):
   check that its assumptions are the K4 hypotheses in the x*y = theta_y(x) convention.
3. Section 5.20 (subsec:count): Lemma 5.40 (invariance), Corollary 5.41, Lemma 5.42 (contraction), Lemma 5.43,
   Theorem 5.44 (end step), Theorem 5.45 ((W_n) for all n), Theorem 5.46 (no finite basis), Theorem 5.47
   ((R'') and K6 from (W_2), Prover9 proofs in code/rpp_vs_chain.pf, k6_vs_chain.pf), Theorem 5.48 ((E1) from
   (Q1)+(W2)+K0; only the README of that proof is available). These were written on 11-13 Oct, after the previous
   cold read, and have not been refereed. Lemma 5.40 and Theorem 5.44 are also used in Theorem 5.49.
4. A correction made on 15 Oct in the proof of Theorem 5.23 ((R')), Step 1 (iv): the earlier text justified
   u |><| v by "hh* |><| h*h for every h", which is false; the new text gives a direct verification. Check the
   new text, and grep the notes for any other use of the false principle.
5. The consistency of status-table.tex and of the header comments of conditions.in with the notes (evidence levels:
   proved / verified in P(P_m) for small m / no embedding found must never be conflated).

Deliverable: a markdown report REPORT.md in this directory, in the style of previous-cold-read-11-Oct.md (what you
read, what you checked by computer and how, verdict per item with precise locations, a list of errors from serious
to cosmetic, and suggestions). Put any scripts you write in review-scripts/. Be concrete: if a step of a proof is
wrong or incomplete, say exactly which claim fails and, if possible, give a counterexample or the missing argument.
Do not try to reprove everything from scratch; do try to break Theorem 5.49.
