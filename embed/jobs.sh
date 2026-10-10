#!/bin/sh
# relaunch background jobs that are not running (container restarts kill them)
P=/home/claude/pa8w
run() { # $1 tag, $2 dir, $3 log, $4 cmd
  pf=$P/.pid_$1
  if [ -f $pf ] && kill -0 $(cat $pf) 2>/dev/null; then echo "running $1"; return; fi
  cd $2 && nohup sh -c "$4" >> $3 2>&1 &
  echo $! > $pf; echo "restarted $1"
}
run fam5 $P/embed/pa8/wn family_check5.log "python3 check.py P5.json 8"
run wn36 $P/embed/pa8/rpp wn_sat3.log "python3 wn_sat.py 3:6"
run b3m7 $P/n4 b3m7.log "python3 b3m7.py"
run rp2ind9 $P/embed/pa8/impl rp2ind.log "echo d=9: \$(/home/claude/bin/mace4 -n 9 -N 9 -m 1 -f rp2ind.in 2>&1 | grep -E 'exit|MODEL' | head -1)"
