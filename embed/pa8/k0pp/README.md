# K0'' and M.K.'s order-9 model (16 Oct 2026)

K0'': a><c><b, yc=cy, theta_y(b)=theta_b(a), theta_a(z)=a, theta_b(z)=b, theta_y(z)=theta_a(b) => a><b
(the K0 hypotheses with theta_z(a)=theta_z(b) replaced by theta_a(z)=a). Proved in every P_X by the proof of
Theorem 5.50 (it only uses theta_a(z)=a and theta_b(z)=b of the z-conditions).

- mk9_k0pp.json : M.K.'s Mace4 model of order 9 satisfying (Q1) and K0 but not K0'' (T[i][j] = i*j = theta_j(i);
                  a,b,c,y,z = 0,1,2,3,4). It is isomorphic to candidate 5 of the order-9 census (cand9.json).
- evalcond.log  : all labelled conditions of notes/conditions.in evaluated on it (w3/evalcond2.py): it violates
                  exactly K0'' and K5 and satisfies everything else, so K0'' is independent of all other listed
                  conditions, and candidate 5 is proved non-embeddable without K5.
- k0pp5.py/.log : K0'' on a random sample of P(P_5): 769 385 instances, 0 violations.
