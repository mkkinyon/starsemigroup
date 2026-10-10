#!/bin/sh
# Enumerate order-7 projection algebras with Q1 and (S) in 49 chunks (values of 0*1 and 1*0), each written to its
# own file when complete, so that the run can be resumed after a container restart.
export PATH=/home/claude/bin:$PATH
cd /mnt/user-data/outputs/starsemigroup/embed/pa7
for k in 0 1 2 3 4 5 6; do for j in 0 1 2 3 4 5 6; do
  f=chunk_${k}_${j}
  [ -f $f.done ] && continue
  # swapping the elements 0 and 1 maps chunk (k,j) to chunk (s(j),s(k)), s = (0 1); run only one of each pair
  sk=$k; sj=$j; [ $k = 0 ] && sk=1; [ $k = 1 ] && sk=0; [ $j = 0 ] && sj=1; [ $j = 1 ] && sj=0
  if [ $sj -lt $k ] || { [ $sj -eq $k ] && [ $sk -lt $j ]; }; then echo skipped > $f.done; continue; fi
  sed "s/^end_of_list\./0 * 1 = $k.\n1 * 0 = $j.\nend_of_list./" ../pa7_q1S.in > $f.in
  mace4 -b 3000 -f $f.in 2> $f.err | interpformat standard | isofilter > $f.tmp 2> $f.iso
  mv $f.tmp $f.out
  grep -c interpretation $f.out > $f.done
done; done
echo ALLDONE > ALLDONE
