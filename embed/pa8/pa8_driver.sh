#!/bin/sh
# Order-8 census of projection algebras with Q1, (S), (R) and 0 minimal (WLOG), in 4096 chunks indexed by the
# values (k,l,m,r) = (0*1, 0*2, 1*2, 2*1); chunks equivalent under the swap 1<->2 are skipped.
# Each chunk writes chunk_k_l_m_r.out (isofiltered models) and .done (count) when finished, so runs are resumable
# and chunks can be shared between machines.  Usage: sh pa8_driver.sh [up|down]   (order of processing)
export PATH=/home/claude/bin:$PATH
cd "$(dirname "$0")"
DIR=${1:-up}
list=""
for k in 0 1 2 3 4 5 6 7; do for l in 0 1 2 3 4 5 6 7; do for m in 0 1 2 3 4 5 6 7; do for r in 0 1 2 3 4 5 6 7; do
  list="$list $k,$l,$m,$r"
done; done; done; done
[ "$DIR" = down ] && list=$(echo $list | tr ' ' '\n' | tac | tr '\n' ' ')
for c in $list; do
  k=${c%%,*}; rest=${c#*,}; l=${rest%%,*}; rest=${rest#*,}; m=${rest%%,*}; r=${rest#*,}
  f=chunk_${k}_${l}_${m}_${r}
  [ -f $f.done ] && continue
  # swap 1<->2:  s(v): 1->2, 2->1, else v.  image chunk = (s(l), s(k), s(r), s(m)); skip if image < (k,l,m,r)
  s() { case $1 in 1) echo 2;; 2) echo 1;; *) echo $1;; esac; }
  ik=$(s $l); il=$(s $k); im=$(s $r); ir=$(s $m)
  if [ $ik -lt $k ] || { [ $ik -eq $k ] && { [ $il -lt $l ] || { [ $il -eq $l ] && { [ $im -lt $m ] || { [ $im -eq $m ] && [ $ir -lt $r ]; }; }; }; }; }; then echo skipped > $f.done; continue; fi
  sed "s/^end_of_list\./0 * 1 = $k.\n0 * 2 = $l.\n1 * 2 = $m.\n2 * 1 = $r.\nend_of_list./" base.in > $f.in
  mace4 -b 3000 -f $f.in 2> $f.err | interpformat standard | isofilter > $f.tmp 2> $f.iso
  mv $f.tmp $f.out
  grep -c "interpretation(" $f.out > $f.done
done
echo ALLDONE > ALLDONE_$DIR
