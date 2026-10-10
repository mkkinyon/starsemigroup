#!/bin/sh
# test each word equation (from words4.txt classes) with prover9 in regular *-semigroup form, 90s
H="a*c*a = a. c*a*c = c. c*b*c = c. b*c*b = b. e*c = c*e. e*a*e = e*c*e. f*a = a*f. e*b*e = f*b*f."
i=0
while read line; do
  set -- $(echo "$line" | sed 's/ = / /g')
  first=$1; shift
  for w in "$@"; do
    i=$((i+1))
    lhs=$(echo $first | sed 's/x/e/g; s/y/f/g; s/\(.\)/\1*/g; s/\*$//')
    rhs=$(echo $w | sed 's/x/e/g; s/y/f/g; s/\(.\)/\1*/g; s/\*$//')
    { echo "assign(max_seconds, 90)."; sed '/^end_of_list/d' rss_base.txt; echo "$H"; echo "end_of_list."; echo "formulas(goals)."; echo "$lhs = $rhs."; echo "end_of_list."; } > bw_$i.in
    prover9 -f bw_$i.in > bw_$i.out 2>&1
    echo "$first = $w : $(grep -m1 -E 'THEOREM PROVED|SEARCH FAILED|Fatal' bw_$i.out) $(grep 'Given=' bw_$i.out | tail -1 | cut -d. -f1)"
  done
done < words4.txt
