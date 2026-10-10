#!/bin/sh
# relaunch background jobs that are not running (container restarts kill them)
P=/home/claude/pa8w
run() { pf=$P/.pid_$1; if [ -f $pf ] && kill -0 $(cat $pf) 2>/dev/null; then echo "running $1"; return; fi; cd $2 && nohup sh -c "$4" >> $3 2>&1 & echo $! > $pf; echo "restarted $1"; }
run redw2 $P/embed/pa8/red red_w2_l2.log "python3 redsearch.py ../rpp/w2inst4.pkl a,c,b,x,y 2"
run redrp2 $P/embed/pa8/red red_rp2_l2.log "python3 redsearch.py rp2inst4.pkl a,c,b,x1,x2,y 2"
