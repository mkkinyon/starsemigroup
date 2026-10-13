k0_implies_e1.pf, k0_lemmas.pf  (M. Kinyon, 12-13 Oct 2026, Prover9 with semantic guidance and hints; two days of work)
Theorem: projection algebra axioms + (Q1) + (W2) + K0  |-  (E1).
Convention X*Y = theta_Y(X).  (E1) with constants: z*b = z, b*a = z, b*d = d, c*x = z, c*a = a, c*b = b, e*x = e, e*d = e, d*a = a  =>  b*a = a.
Main proof (k0_implies_e1.pf, 227 steps, 701 s) uses (Q1), (W2), K0 and five lemmas, proved separately in k0_lemmas.pf:
  L1 (clause 33)  a*((a*d)*b) = z           [(Q1) only;            1st proof, clause 18]
  L2 (clause 34)  (a*c)*d = a*d             [(Q1) and (R);         2nd proof, clause 26, denial form]
  L3 (clause 35)  z*(a*d) = d*x             [(Q1) only;            3rd proof, clause 32, denial form]
  L4 (clause 39)  ((d*c)*b)*d = d           [(W2), L1, L3;         4th proof, clause 15]
  L5 (clause 42)  c*d = d                   [(W2), L1, L3;         5th proof, clause 18]
(R) is a consequence of (W2) ((W1) = (R) with a, b exchanged), so everything follows from (Q1) + (W2) + K0.
Mace4 (M.K.): (Q1) + (R) + K0 has no model violating (E1) of order <= 18; (Q1) + K0 alone has one of order 10 (pa8/impl/mk10_k0_e1.json), which violates (R).
The proof texts as sent are in the two .pf files.
