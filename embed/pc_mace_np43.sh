#!/bin/sh
# For each candidate i in pc_np_4_3.json: Mace4 search (sizes 2..9) for a projection algebra with Q1, (S), (R),
# the path hypotheses and the candidate's atoms, violating the conclusion.  Output $DIR/i.out
export PATH=/home/claude/bin:$PATH
cd /mnt/user-data/outputs/starsemigroup/embed; MODE=${1:-SR}; DIR=pcnp43_mace_$MODE; mkdir -p $DIR
n=$(python3 -c "import json; print(len(json.load(open('pc_np_4_3.json'))))")
i=0
while [ $i -lt $n ]; do
  f=$DIR/$i
  if [ ! -f $f.done ]; then
    python3 pc_mace_in.py 3 pc_np_4_3.json $i $MODE > $f.in
    mace4 -n 2 -N 9 -m 1 -b 2000 -f $f.in > $f.out 2> $f.err
    grep -c "interpretation(" $f.out > $f.done
  fi
  i=$((i+1))
done
echo ALLDONE > $DIR/ALLDONE
