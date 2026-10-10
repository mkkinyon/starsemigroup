# Overnight jobs (M.K.'s machine)

All scripts are resumable; a job killed in the morning can be restarted the next evening with the same command.
Work in the `pa8/` directory of the kit (`embed_kit.tgz`), with python3, pysat (`pip install python-sat`) and numpy.
If the kit is unpacked somewhere else than as `.../embed/pa8`, set `EMBED_DIR` to the `embed` directory.

## Job A: DONE (Sept 2026): Q True 40538 s, E1 True 183 s, E6 True 1265 s; P2 skipped (follows from Q).
## Job A: verify the unproved conditions in P(P_7)   (one process each, hours each; independent)
    python3 verify7b.py 7 Q   > v7_Q.log  2>&1
    python3 verify7b.py 7 P2  > v7_P2.log 2>&1
    python3 verify7b.py 7 E6  > v7_E6.log 2>&1
    python3 verify7b.py 7 E1  > v7_E1.log 2>&1
Output: "NAME m = 7 valid: True/False (seconds)".  A False would be a counterexample in P_7 (the script does not
print it; tell me and I will extract it).  These are the only conditions whose status is "verified for m <= 6".
(Q) and (P2) at m = 6 took 20 s to 12 min; expect m = 7 to take 10-100 times longer.  Not resumable, but
each is a single SAT call, so just rerun if killed.

## Job B: the census of order 10 by extension   (several nights; resumable at every step)
Step 9 -> 10, K parts in parallel (K = number of cores; the 8 -> 9 step took 40 min on two cores, expect 10-20x):
    python3 extend.py 9 10 0 K > ext9_0.log 2>&1 &
    python3 extend.py 9 10 1 K > ext9_1.log 2>&1 &
    ...                                             (parts 0..K-1; checkpoints ext9_<part>.ckpt, restart = same command)
    python3 extend.py 9 10 -1 K                     (merge when all parts report completion -> ord10.json)
Then the analysis (triangle condition, embeddability for m <= 7; resumable line by line, logs post10_<part>.log):
    python3 post8.py 10 7 PART NPARTS  > post10_PART.out 2>&1      for PART = 0..NPARTS-1
Each algebra costs from milliseconds (backtracking for m <= 4) to minutes (SAT at m = 7), so this will take
several nights for ~600k algebras; the m = 7 SAT calls dominate.  Afterwards the algebras with "embeds": null
are the candidates; `pass2_9.py`-style m = 8 runs and the newconds filter can wait for me.
What we learn: the number of candidate obstructions of order 10 (the sequence is 1, 7, 8 so far), whether the
eight known conditions plus (E6'), (E1') catch all of them, and the number of points needed at order 10.

Priorities if time is short: Job A first (small, decisive), then Job B step 9 -> 10 (one night), then post8 nights.
