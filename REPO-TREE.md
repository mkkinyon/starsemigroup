# starsemigroup: repository tree as I hold it (17 Oct 2026, commit 4b0747a)

Generated from `git ls-files` of my working copy of the repository (the one the bundle `starsemigroup.bundle` carries). 4469 tracked files. The Mace4 batch directories `embed/pc2mace_*`, `embed/pc34_*`, `embed/pc43_*`, `embed/pcnp*` are condensed to counts and name patterns.

Not in the repository (large, regenerable; they live only in my working directory `/home/claude/pa8w/`): `embed/pa8/k0/k0inst5.pkl` (1.7M instances), `embed/pa8/k13/l1c_inst4_*.npy`, `embed/pa8/k13/l1c_inst5_s1.npy` (521 200 instances), `*.pos`/`*.neg` signature files, `__pycache__`, LaTeX auxiliaries. `embed/pa8/census/q1ext.py` expects `ord<n>.json` and `post8.log` from `embed/pa8/` in its own directory.

## What the directories are (my understanding)

- `README.md`, `.gitignore` — top level. README describes the layout as of 16 Oct; it should mention `paper/`, `embed/pa8/census/`, `embed/pa8/p9/k4.pf1` and the 17 Oct state (paper draft complete, order-9 minimal list).
- `paper/` — `embedding.tex` (the paper, 55 pp., amsart), `embedding.pdf`, `labels.md` (label map and notation decisions). Compiles with `pdflatex` alone (no bibtex; placeholder `thebibliography`).
- `notes/` — `notes-embedding.tex/.pdf` (the running record, 92 pp.), `status-table.tex`, `conditions.in` (axioms and all conditions as Prover9/Mace4 clauses, incl. K0''), `K-catalogue.md`, `paper-outline.md`, the cold-read reports (REPORT = 10 Oct, 11 Oct, 16 Oct K4, 16 Oct K0) and context files, the HANDOFF files (earlier handoffs; superseded by the notes).
- `cnf/` — `dump.py`, README: the SAT (CNF) dump utility for embedding instances.
- `embed/` (top level, 301 files) — the original embedding thread: enumeration of regular *-semigroups (`enum_rss.py`, `enum_bands.py`, `bands_upto10.pkl`), the embedding searches (`embed.py`, `pa_sat.py`, `b2sat.py`), digraph conditions (`digraph*.py`, `hexagon.in`, `triangle.in`, `octagon.in`, `chain*.in/.out`, `disjoint*.in`, `derived*.in`), graph semigroups (`graphsg*.py`, `layered*.py`, `graphsg_survey.*`), the fourth obstruction (`fourth*.py`), the order-7 census (`pa7_*.py/.sh`), `fast.py` (block calculus helpers used by the review scripts live in `review2/`), `mace4parse.py`, `termeval.py`, `layered_search.py` (also provides `canon`), `cand7.json`, `T26_V.json`, and many `.in/.out` Mace4/Prover9 runs.
- `embed/pa7/` — the chunked Mace4 census of order 7 (`pa7_driver.sh`, chunk outputs, `pa7_post.py` results).
- `embed/pa8/` — the order-8/9 census by one-point extension (`extend.py`, `ord1..9.json`, `ext*.log`, `post8.py/.log`, `post9_*.log`, `pass2_9.py`, `cand8*.py/.out`, `cand9.json/.out`), the path-closing searches (`pc1_classify.py`, `pc3_hit.py`, `pc3_verify.py`, `pc3sig_*.pkl`, `fv*.py` and logs), independence (`indep.py`, `indep_*.log`), `newconds.py`, `OVERNIGHT.md`, `README.md`.
  - `census/` — 17 Oct: `q1ext.py` ((Q1)-only extension census of minimal non-embeddable algebras), `q1ext6..9.log/.json`, README.
  - `e1/`, `e6/` — reconnaissance of (E1), (E6) in P(P_4).
  - `gen/` — search for a common generalisation of (R'), (P1), (Q) (none found).
  - `impl/` — implication/independence matrix: `algs.json` (all named algebras: P7, frakP, P8^1..7, cand9[0..6], R9, P(Q0), MK11, Pch3, Pch4, P9), `viol.py`, `viol.json`, `witnesses.py`, `pairs.py`, `rpchain*.py`, Mace4/Prover9 runs `m_*_*.in/.out`, `p_*.in/.out`, `run.log`; `rp2/` the (R'_2) witness of order 10 (`mk10.json`) and its checks.
  - `k0/` — K0 reconnaissance and dropped-hypothesis maps (`k0inst.py`, `k0rel.py`, `k0drop*.py`, `k0prod.py`, `k0claims.py`, `k0pp.py`, logs, README); `k0inst5.pkl` not tracked.
  - `k0pp/` — the order-9 Mace4 model separating K0'' from K0 (`mk9_k0pp.json`, `evalcond.log`, `k0pp5.py/.log`).
  - `k13/` — reconnaissance of the order-9 candidates 1 and 3 and the (L1c) attack (`recon.py`, `run_all.sh`, `satdrop.py`, `degen.py`, `consq.py`, `shallow.py`, `cores.py`, `l1c_*.py`, `lstar.py`, `diag1*.py`, `k1d.py`, logs); instance arrays not tracked.
  - `k2/` — `c2explore.py` (candidate 2).
  - `mace_r2_not_r/` — Mace4 runs separating (R') from (R).
  - `maxsub/` — embeddings of the maximal subalgebras of P^ch_n and P^R'_n (`chemb.py`, `rpemb.py`, `verify7.log`).
  - `n4/` — the 2-path search language with auxiliaries (`qi.py` with `valid(atoms, concl, m)`, searches and logs).
  - `p1/` — (P1) reconnaissance (Step 4 statements tested in P_4, P_5).
  - `p9/` — Prover9/Mace4 inputs and proofs by M.K.: `k4.pf1` (added 17 Oct), `rpp_vs_chain.pf`, `k6_vs_chain.pf`, the inputs `k0_implies_e1.in`, `k4_implies_e6.in`, `k4_implies_s.in`, `k*_vs_proved.in`, lemma runs `lemA..lemD3`, and the (R')/(V)/(E6) derivations. **Missing here, referenced by notes and paper:** `k4.pf2`, `k0_implies_e1.pf`, `k0_lemmas.pf`, `k4_implies_e6.pf` (your Prover9 proofs); please add them to `embed/pa8/p9/`.
  - `q/`, `q2/` (+ `q2/p9/`, `q2/p9s/`) — (Q) reconnaissance: instances, Prover9 derivations in projection-algebra and semigroup language, `u0.py`, `hubtypes` material.
  - `red/` — K4 reconnaissance and reductions (`k4rec*.py`, `k4drop.py`, `k4sat.py`, `k4weak*.py`, `k4zero.py`, `delta*.py`, `deltaW.py`, `thm6.py`, `rpinf.py`, `rpinv.py`, `rpred.py`, logs).
  - `rp/` — (R') reconnaissance (`harness*.py`, Prover9 runs).
  - `rpp/` — (R'') and the chain family (W_n): `ci2.py`, `wn_sat.py`, `lemA_sat.py`, `kinds2.py`, `walk.py`, `winf.py`, `w3ind.in`, README.
  - `v3/` — (V) checks.
  - `w3/` — the order-11 witnesses of (W_3) and of the triangle condition (`model11b.json`, `subsQ0.py`), `evalcond2.py`.
  - `wn/` — the chain witnesses P^ch_n (`family.py`, `check.py`, `gen.py`, `family_check.log`).
- `embed/pc2mace_*`, `pc34_*`, `pc43_*`, `pcnp*` — Mace4 batch runs of the path-closing searches of Section 5.6 of the notes (one `.in`/`.out` pair per hypothesis set); kept for the record.
- `embed/review2/` — the cold reader's scripts of 11 Oct (`fast.py` block calculus, `wsat.py`, `radius3.py`, `winf.py`, ...).
- `review3/`, `review4/` — the cold reads of 16 Oct (K4, with the gap and its repair; K0, with `REPORT.md`, `lemPX.tex`, `thmK0.tex` and the reference implementations `k0claims_ref.py`, `k0drop_ref.py`).
- `rigidity/` — the earlier thread on rigidity of the involution (markdown and `verify*.py`).

## Recent commits (newest first)

- `4b0747a` Paper: \PA = \mathsf{P} for projection algebras
- `3a43772` Paper: motivation (Wagner-Preston analogy, Schein); unjustified extension claim removed
- `b91f309` Q1-only extension census (orders 6-9); P_9 minimal at order 9; paper Section 8 and notes updated
- `ed61474` Paper: Sections 4, 7, census, 8, 9; main theorems corrected
- `868ac5d` K4: hand derivation of theta_z(c)=b; add k4.pf1
- `42eb960` Paper: chain section
- `e0ef8c0` Paper: (P1), (Q), K4; lemmas commuting auxiliary, transport, counting invariant
- `f219108` Paper draft: preliminaries, local structure, (R'), (R), (V), K0
- `220bb0d` (L1c) segment
- `73f99e5` (L1c) exploration; K1d; \mt macro
- `892105e` Reconnaissance of order-9 candidates 1, 3 (Section 5.23)
- `46ca174` Paper outline; recon.py

## Directory counts

- `./`: 2 files
- `cnf/`: 2 files
- `embed/`: 301 files
- `embed/pa7/`: 162 files
- `embed/pa8/`: 81 files
- `embed/pa8/census/`: 10 files
- `embed/pa8/e1/`: 4 files
- `embed/pa8/e6/`: 10 files
- `embed/pa8/gen/`: 9 files
- `embed/pa8/impl/`: 56 files
- `embed/pa8/impl/rp2/`: 32 files
- `embed/pa8/k0/`: 16 files
- `embed/pa8/k0pp/`: 5 files
- `embed/pa8/k13/`: 50 files
- `embed/pa8/k2/`: 1 files
- `embed/pa8/mace_r2_not_r/`: 11 files
- `embed/pa8/maxsub/`: 6 files
- `embed/pa8/n4/`: 39 files
- `embed/pa8/p1/`: 13 files
- `embed/pa8/p9/`: 40 files
- `embed/pa8/q/`: 7 files
- `embed/pa8/q2/`: 69 files
- `embed/pa8/q2/p9/`: 15 files
- `embed/pa8/q2/p9s/`: 10 files
- `embed/pa8/red/`: 167 files
- `embed/pa8/rp/`: 132 files
- `embed/pa8/rpp/`: 116 files
- `embed/pa8/v3/`: 4 files
- `embed/pa8/w3/`: 16 files
- `embed/pa8/wn/`: 30 files
- `embed/pc2mace_Q1_pc2_4_2/`: 120 files
- `embed/pc2mace_Q1_pc2_4_3/`: 368 files
- `embed/pc2mace_R_pc2_4_2/`: 120 files
- `embed/pc2mace_R_pc2_4_3/`: 368 files
- `embed/pc2mace_SR_pc2_4_2/`: 120 files
- `embed/pc2mace_SR_pc2_4_3/`: 368 files
- `embed/pc2mace_S_pc2_4_3/`: 368 files
- `embed/pc34_mace/`: 121 files
- `embed/pc34_mace_Q1/`: 121 files
- `embed/pc34_mace_R/`: 121 files
- `embed/pc34_mace_S/`: 121 files
- `embed/pc43_mace_Q1/`: 73 files
- `embed/pcnp42_mace_Q1/`: 41 files
- `embed/pcnp42_mace_R/`: 41 files
- `embed/pcnp43_mace_Q1/`: 169 files
- `embed/pcnp43_mace_S/`: 169 files
- `embed/pcnp43_mace_SR/`: 169 files
- `embed/review2/`: 24 files
- `notes/`: 15 files
- `paper/`: 3 files
- `review3/`: 1 files
- `review3/review-scripts/`: 7 files
- `review4/`: 4 files
- `review4/review-scripts/`: 7 files
- `rigidity/`: 14 files

## Listing

### `./` (2)

`.gitignore`, `README.md`

### `cnf/` (2)

`README.md`, `dump.py`

### `embed/` (301)

`T26_V.json`, `abstract_lemma.py`, `analyse.py`, `b2sat.py`, `bands_upto10.pkl`, `cand7.json`, `chain.py`, `chain1.in`, `chain1.out`, `chain2.in`, `chain2.out`, `chain2s.in`, `chain2s.out`, `chain3.in`, `chain3.out`, `chain3_31.out`, `chain3s.in`, `chain3s.out`, `chainS.py`, `congr.py`, `congr3.py`, `congs_P3.pkl`, `cs_embed.py`, `cycle.in`, `derived.in`, `derived_hex.py`, `digraph.py`, `digraph2.py`, `digraph3.log`, `digraph3.py`, `digraph4.log`, `digraph4.py`, `digraph_rest.py`, `disjoint.in`, `disjoint2.in`, `disjoint3.in`, `embed.py`, `enum_bands.py`, `enum_rss.py`, `examples.py`, `examples2.py`, `exp1.py`, `fourth.py`, `fourth_pre.py`, `graphsg.py`, `graphsg4.log`, `graphsg_survey.log`, `graphsg_survey.py`, `graphsg_survey.stdout`, `graphsg_thm.py`, `graphsg_thm6.log`, `hex_smallest.pkl`, `hexagon.in`, `hexcheck_p9.py`, `hexmin.py`, `hexmin2.py`, `hexmin3.py`, `hexmin4.py`, `hexmin4_4_03.pkl`, `hexmin_4.pkl`, `hexqi.py`, `hexquot.py`, `hexquot2.py`, `hexsearch.py`, `hexsearch2.py`, `hexsearch3.py`, `hexsearch4.py`, `hexverify.py`, `hinf.py`, `hinf2.py`, `hinf2_hex.py`, `hinf2_k4.py`, `hinf2_pat.py`, `hinf2_run.py`, `hinf_ax12.log`, `hinf_hex10.log`, `hubcheck_rand.py`, `hubsat.py`, `hubtypes.py`, `identities.py`, `invariant.in`, `jobs.sh`, `k3sat.py`, `layered.py`, `layered_search.log`, `layered_search.py`, `layered_search.stdout`, `layered_search2.py`, `layered_search2_4lev.stdout`, `layered_thm.py`, `m172.py`, `m172_sat8.log`, `m172hom.py`, `m172min.py`, `m172min2.py`, `m172min4_0.log`, `m172q.py`, `m172qi.py`, `m172quot.py`, `m172r.py`, `m172s.py`, `m172s5.log`, `mace4parse.py`, `mace_TimpS9.out`, `mace_WnotS9.out`, `mace_disjoint14.out`, `mace_disjoint18.out`, `mace_path11.out`, `mace_path12.out`, `mace_path14.out`, `mace_per19.out`, `mace_square13.out`, `mace_square14.out`, `mace_square15.out`, `mace_stab21.out`, `mace_tri15.out`, `mace_tri17.out`, `mace_tri19.out`, `mace_uni17b.out`, `mace_uni37.out`, `nofull.py`, `nofull3.log`, `nofull3.py`, `normalband.py`, `normalband2.py`, `notes-embedding.log`, `notes-embedding.out`, `notes-embedding.pdf`, `notes-embedding.tex`, `notes-embedding.tex.bak_Rp`, `notes-embedding.tex.bak_V`, `notes-embedding.toc`, `oct14.py`, `oct4c.log`, `octagon.in`, `octcheck.py`, `octcoinc.py`, `octdiag6.log`, `octdiag6.pkl`, `octdiag6.py`, `octmin.py`, `octmin5.log`, `octmin6.log`, `octmin6.py`, `octsub.py`, `octsub5.log`, `octsub5relax.log`, `octsub6.log`, `octsub6.py`, `p4cong.py`, `p4cong2.py`, `p4mu.py`, `p4mu_disjoint.log`, `p4mu_disjoint.py`, `p4mu_hexagon.pkl`, `p4mu_octagon.pkl`, `p4test.log`, `p5mu.log`, `p5mu_disjoint.py`, `p5mu_disjoint2.py`, `p5mu_hexagon.pkl`, `p5mu_table.pkl`, `p9sat.py`, `pa7_driver.log`, `pa7_driver.sh`, `pa7_post.log`, `pa7_post.py`, `pa7_post.stdout`, `pa7_q1S.in`, `pa_1.err`, `pa_1.in`, `pa_1.iso`, `pa_1.out`, `pa_2.err`, `pa_2.in`, `pa_2.iso`, `pa_2.out`, `pa_3.err`, `pa_3.in`, `pa_3.iso`, `pa_3.out`, `pa_4.err`, `pa_4.in`, `pa_4.iso`, `pa_4.out`, `pa_4_embed.pkl`, `pa_5.err`, `pa_5.in`, `pa_5.iso`, `pa_5.out`, `pa_5_embed.pkl`, `pa_6.in`, `pa_6_partial.out`, `pa_6_partial_embed.pkl`, `pa_6_user.out`, `pa_6_user_embed.pkl`, `pa_embed.py`, `pa_embed2.py`, `pa_enum.py`, `pa_sat.py`, `pa_sat_check.py`, `patch_stream.py`, `path.in`, `path2.in`, `path5.py`, `pathclose.py`, `pathclose2.py`, `pathclose2r.py`, `pathclose3.py`, `pathclose4.py`, `pathclose5.py`, `pathclose_check.py`, `pathclose_np.py`, `pc2_3_2.json`, `pc2_4_2.json`, `pc2_4_2.log`, `pc2_4_2_surv.json`, `pc2_4_3.json`, `pc2_4_3.log`, `pc2_4_3_surv.json`, `pc2_mace.py`, `pc33.json`, `pc34.json`, `pc34_prover.log`, `pc3_verify.py`, `pc43.json`, `pc43_surv.json`, `pc_mace.log`, `pc_mace.sh`, `pc_mace43.sh`, `pc_mace_in.py`, `pc_mace_np42.sh`, `pc_mace_np43.sh`, `pc_np_4_2.json`, `pc_np_4_3.json`, `pc_np_4_3_surv.json`, `pc_prover.py`, `pdflatex.log`, `period.in`, `periodic.py`, `periodic2.py`, `periodic3.log`, `periodic3.py`, `periodic3b.log`, `periodic3c.log`, `periodic4.log`, `periodic4.py`, `periodic4c.log`, `periodic_test.py`, `pmon.py`, `q2.py`, `qi.py`, `qi2.py`, `qsearch.py`, `qsub.py`, `qsub3.py`, `qsub4.py`, `qsub5.py`, `qsub6.py`, `relrep.py`, `relrep_all.py`, `rlocal.py`, `rss_nontriv6.pkl`, `rss_nontriv7.pkl`, `rss_nontriv8.pkl`, `rss_nontriv9_snap.pkl`, `rss_upto5.pkl`, `rss_upto5_emb4.pkl`, `rss_upto5_emb5.pkl`, `rss_upto6_snapshot.pkl`, `rss_upto7.pkl`, `run_enum7.py`, `run_enum9.py`, `rwords.py`, `sq13.py`, `sqfilter.py`, `sqfilter14.log`, `sqfilter15.log`, `sqfilter16.log`, `sqfilter2.py`, `sqstar.py`, `sqtrans.py`, `square.in`, `square2.in`, `square3.in`, `stab.in`, `strongsl.py`, `termeval.py`, `tri5.py`, `triangle.in`, `trimin.py`, `uinf.py`, `uniform.in`, `uniform_hex.py`, `walk_hex.py`, `why.py`, `wiring_SimpT.in`, `wiring_TimpS_q1.in`, `wiring_gS.in`, `wiring_gT.in`, `wiringcheck.py`

### `embed/pa7/` (162)

`ALLDONE`, `chunk_0_0.done`, `chunk_0_0.err`, `chunk_0_0.in`, `chunk_0_0.iso`, `chunk_0_0.out`, `chunk_0_1.done`, `chunk_0_1.err`, `chunk_0_1.in`, `chunk_0_1.iso`, `chunk_0_1.out`, `chunk_0_2.done`, `chunk_0_2.err`, `chunk_0_2.in`, `chunk_0_2.iso`, `chunk_0_2.out`, `chunk_0_3.done`, `chunk_0_3.err`, `chunk_0_3.in`, `chunk_0_3.iso`, `chunk_0_3.out`, `chunk_0_4.done`, `chunk_0_4.err`, `chunk_0_4.in`, `chunk_0_4.iso`, `chunk_0_4.out`, `chunk_0_5.done`, `chunk_0_5.err`, `chunk_0_5.in`, `chunk_0_5.iso`, `chunk_0_5.out`, `chunk_0_6.done`, `chunk_0_6.err`, `chunk_0_6.in`, `chunk_0_6.iso`, `chunk_0_6.out`, `chunk_1_0.done`, `chunk_1_0.err`, `chunk_1_0.in`, `chunk_1_0.iso`, `chunk_1_0.out`, `chunk_1_1.done`, `chunk_1_2.done`, `chunk_1_2.err`, `chunk_1_2.in`, `chunk_1_2.iso`, `chunk_1_2.out`, `chunk_1_3.done`, `chunk_1_3.err`, `chunk_1_3.in`, `chunk_1_3.iso`, `chunk_1_3.out`, `chunk_1_4.done`, `chunk_1_4.err`, `chunk_1_4.in`, `chunk_1_4.iso`, `chunk_1_4.out`, `chunk_1_5.done`, `chunk_1_5.err`, `chunk_1_5.in`, `chunk_1_5.iso`, `chunk_1_5.out`, `chunk_1_6.done`, `chunk_1_6.err`, `chunk_1_6.in`, `chunk_1_6.iso`, `chunk_1_6.out`, `chunk_2_0.done`, `chunk_2_1.done`, `chunk_2_2.done`, `chunk_2_2.err`, `chunk_2_2.in`, `chunk_2_2.iso`, `chunk_2_2.out`, `chunk_2_3.done`, `chunk_2_3.err`, `chunk_2_3.in`, `chunk_2_3.iso`, `chunk_2_3.out`, `chunk_2_4.done`, `chunk_2_4.err`, `chunk_2_4.in`, `chunk_2_4.iso`, `chunk_2_4.out`, `chunk_2_5.done`, `chunk_2_5.err`, `chunk_2_5.in`, `chunk_2_5.iso`, `chunk_2_5.out`, `chunk_2_6.done`, `chunk_2_6.err`, `chunk_2_6.in`, `chunk_2_6.iso`, `chunk_2_6.out`, `chunk_3_0.done`, `chunk_3_1.done`, `chunk_3_2.done`, `chunk_3_3.done`, `chunk_3_3.err`, `chunk_3_3.in`, `chunk_3_3.iso`, `chunk_3_3.out`, `chunk_3_4.done`, `chunk_3_4.err`, `chunk_3_4.in`, `chunk_3_4.iso`, `chunk_3_4.out`, `chunk_3_5.done`, `chunk_3_5.err`, `chunk_3_5.in`, `chunk_3_5.iso`, `chunk_3_5.out`, `chunk_3_6.done`, `chunk_3_6.err`, `chunk_3_6.in`, `chunk_3_6.iso`, `chunk_3_6.out`, `chunk_4_0.done`, `chunk_4_1.done`, `chunk_4_2.done`, `chunk_4_3.done`, `chunk_4_4.done`, `chunk_4_4.err`, `chunk_4_4.in`, `chunk_4_4.iso`, `chunk_4_4.out`, `chunk_4_5.done`, `chunk_4_5.err`, `chunk_4_5.in`, `chunk_4_5.iso`, `chunk_4_5.out`, `chunk_4_6.done`, `chunk_4_6.err`, `chunk_4_6.in`, `chunk_4_6.iso`, `chunk_4_6.out`, `chunk_5_0.done`, `chunk_5_1.done`, `chunk_5_2.done`, `chunk_5_3.done`, `chunk_5_4.done`, `chunk_5_5.done`, `chunk_5_5.err`, `chunk_5_5.in`, `chunk_5_5.iso`, `chunk_5_5.out`, `chunk_5_6.done`, `chunk_5_6.err`, `chunk_5_6.in`, `chunk_5_6.iso`, `chunk_5_6.out`, `chunk_6_0.done`, `chunk_6_1.done`, `chunk_6_2.done`, `chunk_6_3.done`, `chunk_6_4.done`, `chunk_6_5.done`, `chunk_6_6.done`, `chunk_6_6.err`, `chunk_6_6.in`, `chunk_6_6.iso`, `chunk_6_6.out`

### `embed/pa8/` (81)

`E6_notS_9.out`, `OVERNIGHT.md`, `README.md`, `base.in`, `cand8.out`, `cand8.py`, `cand8b.py`, `cand9.json`, `cand9.out`, `ext7_0.log`, `ext7_1.log`, `ext8_0.log`, `ext8_1.log`, `ext9_0.log`, `extend.py`, `fv43.py`, `fv43b.py`, `fv9.py`, `fv9_3.log`, `fv9_3_k5.log`, `fv_4_2.log`, `fv_4_3.log`, `fv_4_3_k4.log`, `fv_4_3_m4.log`, `fv_4_3_m4_k5.log`, `indep.py`, `indep_census.log`, `indep_mace.log`, `indep_mace2.log`, `newconds.py`, `ord1.json`, `ord2.json`, `ord3.json`, `ord4.json`, `ord5.json`, `ord6.json`, `ord7.json`, `ord8.json`, `pa8_driver.sh`, `pa8_post.py`, `pass2_0.out`, `pass2_1.out`, `pass2_2.out`, `pass2_6.out`, `pass2_6b.out`, `pass2_9.py`, `pass2_9_0.log`, `pass2_9_1.log`, `pass2_9_2.log`, `pass2_9_6.log`, `pc1_4_3_size4.pkl`, `pc1_4_3_size5.pkl`, `pc1_classified.json`, `pc1_classify.log`, `pc1_classify.py`, `pc3_hit.py`, `pc3_verify.py`, `pc3sig_4_2.pkl`, `post8.log`, `post8.py`, `post9_3.log`, `qi_all.jsonl`, `qi_all.py`, `qi_all9.jsonl`, `qi_all9.py`, `qi_all9_a.log`, `qi_all9_b.log`, `qi_all_a.log`, `qi_all_b.log`, `qi_all_c.log`, `qi_extract.py`, `run_indep.py`, `run_indep2.py`, `sat8.log`, `sat8.py`, `verify6.log`, `verify6.py`, `verify7.log`, `verify7.py`, `verify7b.py`, `vexp.py`

### `embed/pa8/census/` (10)

`README.md`, `q1ext.py`, `q1ext6.json`, `q1ext6.log`, `q1ext7.json`, `q1ext7.log`, `q1ext8.json`, `q1ext8.log`, `q1ext9.json`, `q1ext9.log`

### `embed/pa8/e1/` (4)

`cl_e1.in`, `e1_cl.in`, `e1_e1p.in`, `e1p_e1.in`

### `embed/pa8/e6/` (10)

`e6_inst.py`, `e6_rel.py`, `gL.in`, `gL2.in`, `g__c_d__a___a_.in`, `g_a__c_d____c_d_.in`, `g_a_b___a_.in`, `g_a_c___b_c_.in`, `g_a_d___c_d_.in`, `g_b_a___a_.in`

### `embed/pa8/gen/` (9)

`check.log`, `check.py`, `probe.log`, `probe.py`, `search.log`, `search.py`, `search2.log`, `search2.py`, `tables.py`

### `embed/pa8/impl/` (56)

`P9.json`, `algs.json`, `explain_S.log`, `frakP.json`, `m_K0_E1.in`, `m_K4_E6.in`, `m_K4_S.in`, `m_K6_R.in`, `m_K6_Rpp.in`, `m_K6_W2.in`, `m_Rpp_K6.in`, `m_Rpp_R.in`, `m_Rpp_W2.in`, `m_W2_K6.in`, `m_W2_R.in`, `m_W2_Rpp.in`, `m_W3_K6.in`, `m_W3_R.in`, `m_W3_Rpp.in`, `m_W4_K6.in`, `m_W4_R.in`, `m_W4_Rpp.in`, `mk10_k0_e1.json`, `mk8_k0.json`, `mk8_k4.json`, `p_K0_E1.in`, `p_K4_E6.in`, `p_K4_S.in`, `p_K6_R.in`, `p_K6_Rpp.in`, `p_K6_W2.in`, `p_Rpp_K6.in`, `p_Rpp_R.in`, `p_Rpp_W2.in`, `p_W2_K6.in`, `p_W2_R.in`, `p_W2_Rpp.in`, `p_W3_K6.in`, `p_W3_R.in`, `p_W3_Rpp.in`, `p_W4_K6.in`, `p_W4_R.in`, `p_W4_Rpp.in`, `pairs.py`, `r_rmirror.in`, `rp2ind.in`, `rp2ind.log`, `rp3ind.in`, `rp3ind.log`, `rpchain.py`, `rpchain2.py`, `run.log`, `unsettled.json`, `viol.json`, `viol.py`, `witnesses.py`

### `embed/pa8/impl/rp2/` (32)

`R1.json`, `R1_T.json`, `R2.json`, `R2_T.json`, `R3.json`, `R3_T.json`, `R4.json`, `R4_T.json`, `R5.json`, `R5_T.json`, `README.md`, `an10.py`, `emb10.py`, `emb10_full.log`, `emb10_max.log`, `iso8.py`, `minsets.log`, `minsets.py`, `mk10.json`, `mk10.py`, `mk10_T.json`, `rp2_m6.log`, `rp2_m6.py`, `rp3ind.in`, `rpchk.log`, `rpchk.py`, `rpfam.py`, `simp.py`, `st10.py`, `syntax.log`, `w4chk.py`, `w4ind.in`

### `embed/pa8/k0/` (16)

`README.md`, `idtest.py`, `k0claims.py`, `k0claims4.log`, `k0claims5.log`, `k0claims5_sum.log`, `k0drop.log`, `k0drop.py`, `k0drop2.log`, `k0drop2.py`, `k0inst.py`, `k0inst5.log`, `k0pp.py`, `k0prod.py`, `k0rel.py`, `l0test.py`

### `embed/pa8/k0pp/` (5)

`README.md`, `evalcond.log`, `k0pp5.log`, `k0pp5.py`, `mk9_k0pp.json`

### `embed/pa8/k13/` (50)

`README.md`, `consq.py`, `consq_K1b.log`, `consq_K1c.log`, `consq_K1d.log`, `consq_K3b.log`, `cores.log`, `cores.py`, `degen.log`, `degen.py`, `diag1.log`, `diag1.py`, `diag1b.log`, `diag1b.py`, `k1d.py`, `l1c_explore.py`, `l1c_explore2.py`, `l1c_explore2_4.log`, `l1c_explore3.py`, `l1c_explore3_4.log`, `l1c_explore4.log`, `l1c_facts.py`, `l1c_facts2.log`, `l1c_facts2.py`, `l1c_p5.log`, `l1c_p5.py`, `l1c_stm5.log`, `l1c_stm5.py`, `lstar.py`, `recon.py`, `recon_K1a_4.log`, `recon_K1b_4.log`, `recon_K1c_4.log`, `recon_K1d_4.log`, `recon_K3a_4.log`, `recon_K3b_4.log`, `recon_K3c_4.log`, `run_all.log`, `run_all.sh`, `satdrop.py`, `satdrop_4.log`, `satdrop_5.log`, `satdrop_6.log`, `satdrop_run.log`, `shallow.py`, `shallow_K1b.log`, `shallow_K1c.log`, `shallow_K1c_5.log`, `shallow_K1d.log`, `shallow_K3b.log`

### `embed/pa8/k2/` (1)

`c2explore.py`

### `embed/pa8/mace_r2_not_r/` (11)

`r2_not_r.in`, `r2_not_r_4.in`, `r2_not_r_4.out`, `r2_not_r_5.in`, `r2_not_r_5.out`, `r2_not_r_6.in`, `r2_not_r_6.out`, `r2_not_r_7.in`, `r2_not_r_7.out`, `r2_not_r_8.in`, `r2_not_r_8.out`

### `embed/pa8/maxsub/` (6)

`README.md`, `chemb.py`, `extract.log`, `extract.py`, `rpemb.py`, `verify7.log`

### `embed/pa8/n4/` (39)

`README.md`, `b3m7.py`, `catalog.log`, `catalog.py`, `census_neg.py`, `checkB3.py`, `checkB3b.py`, `checkK.py`, `checkK0.log`, `decode.py`, `decode2.py`, `explain2.py`, `explain3.py`, `explain3b.py`, `explain3b_0.log`, `explain3b_all.log`, `explain3c.log`, `explain3c.py`, `explain9.py`, `hit4.c`, `hits_4_3c.txt`, `hits_5_2b.txt`, `hits_5_4.txt`, `mace_gen.py`, `min9.log`, `min9.py`, `minimise9.py`, `pathclose4.py`, `pathclose4b.py`, `qi.py`, `qi9_readable.txt`, `quick9.py`, `struct9.py`, `var6.py`, `varB.py`, `verify6_2.py`, `verify6_2b.py`, `verify_5_2b.log`, `verify_hits.py`

### `embed/pa8/p1/` (13)

`h1.py`, `h2.py`, `h3.py`, `h4.py`, `h5.py`, `inst5_0.log`, `inst5_1.log`, `inst5_2.log`, `instP4.pkl`, `p1_inst.py`, `p1_inst5.py`, `p1_rel.py`, `p1_sep.py`

### `embed/pa8/p9/` (40)

`E6_S1.in`, `E6_S1.out`, `E6_S2.in`, `E6_S2.out`, `Rp_R1.in`, `Rp_R1.out`, `Rp_R2.in`, `Rp_R2.out`, `V.in`, `V.out`, `V2.in`, `V2.out`, `V3.in`, `V3.out`, `check_conditions.py`, `conditions.in`, `head.in`, `head2.in`, `k0_implies_e1.in`, `k0_implies_e1_README.txt`, `k0_vs_proved.in`, `k4.pf1`, `k4_implies_e6.in`, `k4_implies_s.in`, `k4_vs_proved.in`, `k5_vs_proved.in`, `k6_vs_chain.in`, `k6_vs_chain.pf`, `lemA.in`, `lemA.out`, `lemC.in`, `lemC.out`, `lemD.in`, `lemD.out`, `lemD2.in`, `lemD2.out`, `lemD3.in`, `lemD3.out`, `rpp_vs_chain.in`, `rpp_vs_chain.pf`

### `embed/pa8/q/` (7)

`q1.py`, `q_ex.py`, `q_long.py`, `q_rel.py`, `q_sep.py`, `q_words.log`, `q_words.py`

### `embed/pa8/q2/` (69)

`NOTES_Q.md`, `coarsen.py`, `coarsen2.py`, `cross.py`, `cycle.py`, `drop.py`, `drop2.py`, `drop3.py`, `efacts.py`, `efacts2.py`, `h1.py`, `h2.py`, `h3.py`, `h4.py`, `hadrop.py`, `hq.py`, `inst4.py`, `inst5.py`, `inst6.py`, `instQ4.pkl`, `k3b.py`, `k3drop.py`, `k6p5.py`, `norm.py`, `norm2.py`, `run6.py`, `split.py`, `suff.py`, `suff2.py`, `t1.py`, `t10.py`, `t11.py`, `t12.py`, `t13.py`, `t14.py`, `t15.py`, `t16.py`, `t17.py`, `t18.py`, `t19.py`, `t2.py`, `t20.py`, `t21.py`, `t22.py`, `t23.py`, `t24.py`, `t24b.py`, `t25.py`, `t26.py`, `t3.py`, `t4.py`, `t5.py`, `t6.py`, `t7.py`, `t8.py`, `t9.py`, `u0.py`, `uset.py`, `vtest.py`, `wb.py`, `words.py`, `words2.py`, `words3.py`, `yc.py`, `ymax.py`, `ymin.py`, `ynon.py`, `yrev.py`, `yset.py`

### `embed/pa8/q2/p9/` (15)

`base.txt`, `g_cd.in`, `g_e_cd.in`, `g_goal.in`, `g_u_le_e.in`, `g_u_le_e2.in`, `g_ua.in`, `g_ya_le_e.in`, `g_ya_le_e2.in`, `g_yd.in`, `g_yd2.in`, `g_z_le_f.in`, `m4_ydy.in`, `m4_ydy_S.in`, `p9_ydy_S.out`

### `embed/pa8/q2/p9s/` (10)

`base.txt`, `base2.txt`, `g_ud.in`, `g_ud2.in`, `g_yc_ybc.in`, `g_ycb.in`, `g_yd_ybd.in`, `g_ydy.in`, `g_ydy2.in`, `g_ydy2.out`

### `embed/pa8/red/` (167)

`README.md`, `alg_by.in`, `alg_by.out`, `alg_cy.in`, `alg_cy.out`, `blocktypes.py`, `canon.py`, `canon2.py`, `cex.py`, `cex2.py`, `cexA.py`, `cexA2.py`, `cexpair.py`, `chainends.py`, `chains3.py`, `chk_ii.py`, `claims.py`, `classtypes.py`, `closing.py`, `comp1.py`, `compress.py`, `contract.log`, `contract.py`, `contract2.py`, `contract3.py`, `dag.py`, `dag_m5.log`, `dbg.py`, `delta.py`, `delta6.py`, `deltaW.py`, `deltaW5.log`, `dista.py`, `endmin.py`, `ends5.py`, `endstep.py`, `equiv.py`, `findx.log`, `findx.py`, `five.py`, `g12.py`, `g12all.py`, `g12cex.py`, `g12dep.py`, `g1step.py`, `g2prime.py`, `genq.py`, `goal.py`, `goal2.py`, `goal3.py`, `goal4.py`, `goal5.py`, `goal5_m5.log`, `ids.log`, `ids.py`, `ids_w2.log`, `ids_w2.py`, `ids_w2_long.log`, `ids_w2_long.py`, `inst.py`, `inst4.log`, `inv.py`, `inv2.py`, `inv2_m4_K3.log`, `inv2_m4_K3_distinct.log`, `inv2_m4_K4.log`, `inv3.py`, `inv3_m5_K4.log`, `inv4.py`, `inv4_m4_K3.log`, `inv4_m4_K4.log`, `inv5.py`, `inv5_m4_K3.log`, `inv5close.py`, `inv5close_m5.log`, `inv6.py`, `inv6_m4.log`, `inv6_m5.log`, `invfam.py`, `invfam_m5.log`, `k4chk.py`, `k4drop.py`, `k4drop2.py`, `k4full.py`, `k4rank.py`, `k4rec10.py`, `k4rec11.py`, `k4rec12.py`, `k4rec2.py`, `k4rec3.py`, `k4rec4.py`, `k4rec5.py`, `k4rec6.py`, `k4rec7.py`, `k4rec8.py`, `k4rec9.py`, `k4red.py`, `k4sat.py`, `k4weak.py`, `k4weak4.log`, `k4weak_alg.log`, `k4weak_alg.py`, `k4zero.py`, `l12.py`, `l12b.py`, `lemA2_sat.py`, `lemA3_sat.py`, `lemA4_sat.py`, `lemA_dec.py`, `lemma_a.py`, `m2cex.py`, `m6targets.log`, `m6targets.py`, `m7targets.log`, `meets.py`, `modules.py`, `modules_m6a.log`, `modules_m6b.log`, `nf6.log`, `nf6.py`, `normalform.py`, `normalform2.py`, `normalform3.py`, `normalform4.py`, `obstr.py`, `pairstat.py`, `pos3.py`, `pq.py`, `pqdec.py`, `pqdec2.py`, `pqdec3.py`, `pqdec4.py`, `prop2.py`, `propA.py`, `r4.py`, `radfam.py`, `red_rp2.log`, `red_rp2_l2.log`, `red_w2.log`, `red_w2_l2.log`, `redsearch.py`, `rel.py`, `rpinf.py`, `rpinv.py`, `rpred.py`, `s1314.log`, `s1314.py`, `shorten.py`, `sigma.py`, `stab.py`, `stab5.log`, `stab6.log`, `stab6.py`, `stab6b.log`, `t1.py`, `t1loc.py`, `t1loc2.py`, `t1loc3.py`, `t1loc4.py`, `t1loc_m4_K3.log`, `thm6.py`, `thm6_5.log`, `tind.py`, `tind2.py`, `tmin.py`, `whichfail.py`, `ychk.py`

### `embed/pa8/rp/` (132)

`batch_words.log`, `batch_words.sh`, `blocks.py`, `core.m4.in`, `core.m4_3.out`, `core.m4_4.out`, `core.m4_5.out`, `core.m4_6.out`, `core.m4_7.out`, `g_ab.in`, `g_ab.out`, `g_ax.in`, `g_ax.out`, `g_cy.in`, `g_cy.out`, `g_xa.in`, `g_xa.out`, `g_xab.in`, `g_xab.out`, `g_xb.in`, `g_xb.out`, `h13_5.log`, `h5_5.log`, `harness.py`, `harness10.py`, `harness10_ex.pkl`, `harness11.py`, `harness11_ex.pkl`, `harness12.py`, `harness12_ex.pkl`, `harness13.py`, `harness13_ex.pkl`, `harness2.py`, `harness2_ex.pkl`, `harness3.py`, `harness3_ex.pkl`, `harness4.py`, `harness4_ex.pkl`, `harness5.py`, `harness5_ex.pkl`, `harness6.py`, `harness6_ex.pkl`, `harness7.py`, `harness7_ex.pkl`, `harness8.py`, `harness8_ex.pkl`, `harness9.py`, `harness9_ex.pkl`, `harness_ex.pkl`, `inst3.pkl`, `inst4.pkl`, `inst5_s0.pkl`, `inst5_s1.pkl`, `m4_w.m4.in`, `m4_w.m4_10.out`, `m4_w.m4_3.out`, `m4_w.m4_4.out`, `m4_w.m4_5.out`, `m4_w.m4_6.out`, `m4_w.m4_7.out`, `m4_w.m4_8.out`, `m4_w.m4_9.out`, `m4_w2.m4.in`, `m4_w2.m4_3.out`, `m4_w2.m4_4.out`, `m4_w2.m4_5.out`, `m4_w2.m4_6.out`, `m4_w2.m4_7.out`, `p83.interp`, `p83test.txt`, `pa_ava.in`, `pa_ava.out`, `pa_base.txt`, `pa_core1.in`, `pa_core1.out`, `pa_core2.in`, `pa_core2.out`, `pa_cy.in`, `pa_cy.m4.in`, `pa_cy.m4_3.out`, `pa_cy.m4_4.out`, `pa_cy.m4_5.out`, `pa_cy.m4_6.out`, `pa_cy.m4_7.out`, `pa_cy.m4_8.out`, `pa_cy.m4_9.out`, `pa_cy.out`, `pa_mx.in`, `pa_mx.out`, `pa_uw.in`, `pa_uw.out`, `pa_w.in`, `pa_w.out`, `pa_w2a.in`, `pa_w2a.out`, `pa_w2b.in`, `pa_w2b.out`, `pa_wu.out`, `pa_xa.in`, `pa_xa.m4.in`, `pa_xa.m4_3.out`, `pa_xa.m4_4.out`, `pa_xa.m4_5.out`, `pa_xa.m4_6.out`, `pa_xa.m4_7.out`, `pa_xa.m4_8.out`, `pa_xa.m4_9.out`, `pa_xa.out`, `pa_yc.in`, `pa_yc.m4.in`, `pa_yc.m4_3.out`, `pa_yc.m4_4.out`, `pa_yc.m4_5.out`, `pa_yc.m4_6.out`, `pa_yc.m4_7.out`, `pa_yc.m4_8.out`, `pa_yc.m4_9.out`, `pa_yc.out`, `rp_inst.py`, `rp_inst5.py`, `rp_inst5_0.log`, `rp_inst5_1.log`, `rp_inst5_7.log`, `rp_min.py`, `rp_min3b.py`, `rp_min4.log`, `rp_min4.py`, `rp_rel.py`, `rp_words.py`, `rss_base.txt`, `words4.txt`, `words4.txt.bak`

### `embed/pa8/rpp/` (116)

`README.md`, `alg_sat.py`, `alg_sat2.log`, `alg_sat2.py`, `axioms.txt`, `base.txt`, `base2.txt`, `c4ex.py`, `chain3.log`, `chain3.py`, `chain4.log`, `chain4.py`, `chk_chain.log`, `chk_chain.py`, `ci2.log`, `ci2.py`, `deep.py`, `ex1.py`, `g_cffc.in`, `g_eaefeae.in`, `g_ebbe.in`, `g_ecfc.in`, `g_fbfece.in`, `h1.in`, `h10.in`, `h11.in`, `h12.in`, `h2.in`, `h21.in`, `h22.in`, `h23.in`, `h24.in`, `h25.in`, `h26.in`, `h27.in`, `h28.in`, `h3.in`, `h31.in`, `h32.in`, `h33.in`, `h34.in`, `h35.in`, `h36.in`, `h37.in`, `h38.in`, `h4.in`, `h41.in`, `h42.in`, `h43.in`, `h5.in`, `h6.in`, `h7.in`, `h8.in`, `h9.in`, `harness.py`, `harness10.py`, `harness11.py`, `harness12.py`, `harness13.py`, `harness14.py`, `harness15.py`, `harness16.py`, `harness2.py`, `harness3.py`, `harness4.py`, `harness5.py`, `harness6.py`, `harness7.py`, `harness8.py`, `harness9.py`, `joins.py`, `kinds.py`, `kinds2.py`, `kinds3.py`, `lemA6.log`, `lemA7.log`, `lemA_ex.py`, `lemA_sat.py`, `pb.txt`, `pb2.txt`, `red.in`, `rel.py`, `rel2.py`, `rpp_inst.py`, `rpp_inst5.py`, `rpp_inst5_0.log`, `rpp_w2.in`, `rpp_w2_p9.in`, `sc1.in`, `sc2.in`, `subhyp.py`, `v3.in`, `v3p.in`, `v4.in`, `v4p.in`, `w2_inst.py`, `w2_inst5.py`, `w2_inst5_0.log`, `w2_rpp.in`, `w2_rpp_p9.in`, `w2_sample.txt`, `w2_w3_p9.in`, `w3ind.in`, `w3ind8.in`, `w3ind9.in`, `w4_sample.txt`, `walk.py`, `walk2.py`, `walk3.py`, `walk4.py`, `wn_sat.log`, `wn_sat.py`, `wn_sat3.log`, `words.py`, `words2.py`, `words_w2.py`

### `embed/pa8/v3/` (4)

`id1.in`, `m_v3.in`, `q1_v3.in`, `v3_v.in`

### `embed/pa8/w3/` (16)

`chk_Q1.in`, `chk_R.in`, `chk_S.in`, `chk_Tri.in`, `embed11.py`, `embed11_78.log`, `evalcond.py`, `evalcond2.py`, `mace_check.py`, `model11.json`, `model11.py`, `model11b.json`, `model11b.py`, `subs11.log`, `subs11.py`, `subsQ0.py`

### `embed/pa8/wn/` (30)

`P2.json`, `P2_T.json`, `P3.json`, `P3_T.json`, `P3_omit_c.json`, `P4.json`, `P4_T.json`, `P5.json`, `P5_T.json`, `P6.json`, `P6_T.json`, `check.py`, `family.py`, `family_check.log`, `gen.py`, `iso.py`, `parse.py`, `show.py`, `wn2.json`, `wn2_T.json`, `wn3.json`, `wn3_T.json`, `wn_2_known.in`, `wn_2_sv.in`, `wn_3_known.in`, `wn_3_sv.in`, `wn_4_known.in`, `wn_4_sv.in`, `wn_5_known.in`, `wn_5_sv.in`

### `embed/pc2mace_Q1_pc2_4_2/` (120)

`#.done` x60, `#.in` x60

### `embed/pc2mace_Q1_pc2_4_3/` (368)

`#.done` x184, `#.in` x184

### `embed/pc2mace_R_pc2_4_2/` (120)

`#.done` x60, `#.in` x60

### `embed/pc2mace_R_pc2_4_3/` (368)

`#.done` x184, `#.in` x184

### `embed/pc2mace_SR_pc2_4_2/` (120)

`#.done` x60, `#.in` x60

### `embed/pc2mace_SR_pc2_4_3/` (368)

`#.done` x184, `#.in` x184

### `embed/pc2mace_S_pc2_4_3/` (368)

`#.done` x184, `#.in` x184

### `embed/pc34_mace/` (121)

`#.done` x30, `#.err` x30, `#.in` x30, `#.out` x30, `ALLDONE` x1

### `embed/pc34_mace_Q1/` (121)

`#.done` x30, `#.err` x30, `#.in` x30, `#.out` x30, `ALLDONE` x1

### `embed/pc34_mace_R/` (121)

`#.done` x30, `#.err` x30, `#.in` x30, `#.out` x30, `ALLDONE` x1

### `embed/pc34_mace_S/` (121)

`#.done` x30, `#.err` x30, `#.in` x30, `#.out` x30, `ALLDONE` x1

### `embed/pc43_mace_Q1/` (73)

`#.done` x18, `#.err` x18, `#.in` x18, `#.out` x18, `ALLDONE` x1

### `embed/pcnp42_mace_Q1/` (41)

`#.done` x10, `#.err` x10, `#.in` x10, `#.out` x10, `ALLDONE` x1

### `embed/pcnp42_mace_R/` (41)

`#.done` x10, `#.err` x10, `#.in` x10, `#.out` x10, `ALLDONE` x1

### `embed/pcnp43_mace_Q1/` (169)

`#.done` x42, `#.err` x42, `#.in` x42, `#.out` x42, `ALLDONE` x1

### `embed/pcnp43_mace_S/` (169)

`#.done` x42, `#.err` x42, `#.in` x42, `#.out` x42, `ALLDONE` x1

### `embed/pcnp43_mace_SR/` (169)

`#.done` x42, `#.err` x42, `#.in` x42, `#.out` x42, `ALLDONE` x1

### `embed/review2/` (24)

`acomp.py`, `acomp5.log`, `blk.py`, `check2.py`, `check3.py`, `closing.py`, `fast.py`, `rad6.log`, `rad7.log`, `radius2.py`, `radius3.py`, `tn.py`, `tn2.py`, `tn5.log`, `w_2_6_ab.log`, `w_2_6_ba.log`, `w_3_6_ab.log`, `w_3_6_ba.log`, `w_4_6_ab.log`, `w_4_6_ba.log`, `winf.py`, `winf5.log`, `winf6.log`, `wsat.py`

### `notes/` (15)

`HANDOFF-Q-proved.md`, `HANDOFF-UPDATE.md`, `HANDOFF-summary-for-James.md`, `HANDOFF.md`, `K-catalogue.md`, `cold-read-CONTEXT-11-Oct.md`, `cold-read-REPORT-11-Oct.md`, `cold-read-REPORT-16-Oct-K0.md`, `cold-read-REPORT-16-Oct.md`, `cold-read-REPORT.md`, `conditions.in`, `notes-embedding.pdf`, `notes-embedding.tex`, `paper-outline.md`, `status-table.tex`

### `paper/` (3)

`embedding.pdf`, `embedding.tex`, `labels.md`

### `review3/` (1)

`CONTEXT.md`

### `review3/review-scripts/` (7)

`claimtest.py`, `dropmap.py`, `k4gap_sat.py`, `k4verify.py`, `pm.py`, `repairfacts.py`, `step2trace.py`

### `review4/` (4)

`CONTEXT.md`, `REPORT.md`, `lemPX.tex`, `thmK0.tex`

### `review4/review-scripts/` (7)

`k0claims_ref.py`, `k0claims_ref4.log`, `k0claims_ref5.log`, `k0drop_ref.py`, `k0drop_ref4.log`, `misc_ref.py`, `ya_eq_u.py`

### `rigidity/` (14)

`01-summary.md`, `02-preliminaries.md`, `03-main-theorem.md`, `04-case-k-equals-2.md`, `05-counterexamples.md`, `06-all-inversions.md`, `07-global-structure.md`, `08-rigid.md`, `two-inversions-full.md`, `verify.py`, `verify2.py`, `verify3.py`, `verify4.py`, `verify5.py`
