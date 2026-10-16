# Reconnaissance of the order-9 candidates 1 and 3 (17 Oct 2026), notes Section 5.23

- recon.py COND n [cap] [budget]: instances in P(P_n) (sampled (a,c,b)-triples), dropped-hypothesis map for a><b,
  consequence atoms on the full instances.  recon_*_4.log/.pkl.  NB: the "atoms still valid without it" lists of
  sampled (STOPPED) dropped sets are unreliable; use shallow.py (SAT) instead.
- satdrop.py m [COND..]: SAT validity of each condition and of each single-hypothesis drop in P(P_m); satdrop_4,5,6.log:
  all six hold for m <= 6, every hypothesis essential already at m = 4.
- degen.py: K1a, K3a, K3c force a = b (they contain u = v, i.e. ab = ba); K1b, K1c, K3b do not.  degen.log.
- consq.py COND: the P_4 consequence atoms re-verified by SAT at m = 4, 5 (consq_*.log).
- shallow.py COND: for each consequence atom and each hypothesis h, whether the atom follows without h (SAT, m = 4):
  "needs" lists the hypotheses whose removal breaks it (shallow_*.log).
- cores.py: the identification cores (L1b), (L1c), (L3b) = the conditions minus their closing half-matching;
  valid for m <= 6, every hypothesis essential at m = 5 (cores.log).
Transcription error found and corrected: K3a, K3b had "b <= y" (and "b <= z") for the half-matchings byb = b, bzb = b
(catalog.log: th_b(y) = b); with the order relations candidate 3 does not violate them.
