# K0 in every partition monoid (16 Oct 2026, evening)

Theorem 5.50 of notes-embedding.tex: a><c><b, yc=cy, theta_y(b)=theta_b(a), theta_b(z)=b,
theta_z(a)=theta_z(b), theta_y(z)=theta_a(b)  =>  a><b.  Hence (E1) (via k0_implies_e1.pf) and
P_8^1 is minimal non-embeddable; all seven order-8 candidates are settled.

Scripts (fast.py bit calculus from review2/review-scripts):
- k0inst.py n [budget]  : K0 instances in P(P_n); k0inst4.pkl (68455), k0inst5.pkl (1 720 529 in 1500 s,
                           1 514 807 with a != b, 0 violations) -- pkl files not committed.
- k0rel.py              : always-true relations among a,b,c,y,z,u,v,p,w,q,r,s,t,... on the P_4 instances.
- k0drop.py, k0drop2.py : dropped-hypothesis maps (k0drop.log, k0drop2.log) used during the reconnaissance.
- k0prod.py             : product identities in P_4 (pm.py); yz = yaz, zy = zay, ab = azb hold on all instances.
- k0claims.py n [budget]: dropped-hypothesis map for the claims of the proof of Theorem 5.50
                           (k0claims4.log: all of P_4; k0claims5.log: random (a,c) pairs of P_5).
- k0pp.py               : the variant K0'' (theta_z(a)=theta_z(b) replaced by theta_a(z)=a) in P_4.
- idtest.py, l0test.py  : two side checks (theta_z(a)=theta_z(b) does not imply theta_z(aba)=theta_z(a)).
