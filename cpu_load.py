# -*- coding: utf-8 -*-
#!/usr/bin/python                        
##################################################
# AUTHOR : Yandi LI
# CREATED_AT : 2018-03-07
# LAST_MODIFIED : 2018-03-07 17:29:57
# USAGE : python cpu_load.py
# PURPOSE : TODO
##################################################
from multiprocessing import Pool
from multiprocessing import cpu_count

def f(x):
  while True:
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
