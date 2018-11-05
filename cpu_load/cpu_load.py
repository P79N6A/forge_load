# -*- coding: utf-8 -*-
#!/usr/bin/python                        
##################################################
# AUTHOR : Yandi LI
# CREATED_AT : 2018-03-07
# LAST_MODIFIED : 2018-10-29 12:08:18
# USAGE : python cpu_load.py
# PURPOSE : 每天3点定时启动一个小时，提高CPU利用率
##################################################
from multiprocessing import Pool
from multiprocessing import cpu_count
from datetime import datetime
import time

def f(x):
  while True:
    if datetime.now().hour != 3:
      time.sleep(60)
    else:
      x * x


if __name__ == '__main__':
  import sys
  if len(sys.argv) >= 2:
    ratio = float(sys.argv[1])
  else:
    ratio = 0.5
  processes = int(ratio * cpu_count())
  print 'utilizing %d cores\n' % processes
  pool = Pool(processes)
  pool.map(f, range(processes))
