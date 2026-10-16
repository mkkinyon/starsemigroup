#!/bin/bash
# reconnaissance of K1a..K3c in P_4, 150 s per enumeration, logs per condition (restart-safe: skips finished ones)
cd /home/claude/pa8w/embed/pa8/k13
for C in K1a K1b K1c K3a K3b K3c; do
  if [ -f recon_${C}_4.pkl ]; then continue; fi
  python3 recon.py $C 4 400000 150 > recon_${C}_4.log 2>&1
done
echo ALLDONE > run_all.done
