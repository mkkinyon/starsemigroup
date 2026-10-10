import sys, pickle
from hq import *
from run6 import run_sampled
from t24 import C_stat, stats
run_sampled(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], {'stat': C_stat}, 0, maxu=3, maxy=1)
run_sampled(6, ['instQ6_0.pkl', 'instQ6_1.pkl', 'instQ6_2.pkl'], {'stat': C_stat}, 0, maxu=3, maxy=1)
for k in sorted(stats, key=str): print(stats[k], k)
