# -*- coding: utf-8 -*-
#!/usr/bin/python                        
##################################################
# AUTHOR : Yandi LI
# CREATED_AT : 2018-11-01
# LAST_MODIFIED : 2018-11-06 21:05:10
# USAGE : python test2.py
# PURPOSE : TODO
##################################################
from __future__ import division
import math
import threading
import time
from collections import deque
import GPUtil
from numba import cuda
import numpy

cuda.select_device(0)

class Monitor(threading.Thread):

  def __init__(self):
    super(Monitor, self).__init__()
    self.setDaemon(True)
    self._queue = deque([0] * 5, 5)
    self.avg_load = 0
    self.max_load = 0

  def update(self, ):
    load = self.get_current_load()
    self._queue.append(load)
    self.avg_load = sum(self._queue)/len(self._queue)
    self.max_load = max(self._queue)

  def run(self):
    while True:
      self.update()
      time.sleep(1)

  @staticmethod
  def get_current_load():
    gpu = GPUtil.getGPUs()[0]
    load = gpu.load * 100
    return load


class Worker(object):

  def __init__(self, target=50):
    data = numpy.zeros(512)
    self._device_data = cuda.to_device(data)
    self.threadsperblock = 128
    self.blockspergrid = int(math.ceil(data.shape[0] / self.threadsperblock)) 
    self.target = target
    self.multiplier = 1000

  def __str__(self):
    return "threadsperblock: {}, blockspergrid: {}".format(self.threadsperblock, self.blockspergrid)


  @staticmethod
  @cuda.jit
  def my_kernel(io_array):
    """ CUDA kernel 
    """
    pos = cuda.grid(1)
    tx = cuda.threadIdx.x 
    if pos < io_array.size:
      io_array[pos] += tx # do the computation


  def run_awhile(self, sec=10):
    start = time.time()
    while time.time() - start < sec:
      self.my_kernel[self.multiplier * self.blockspergrid, self.threadsperblock](self._device_data)


  def idle_awhile(self, sec=5):
    time.sleep(sec)


  @classmethod
  def main(cls, target=50):
    worker = Worker(target)
    print(worker)
    monitor = Monitor()
    monitor.start()
    print("Monitor started: %s" % monitor.is_alive())
    time.sleep(5)
    print("Initial average load", monitor.avg_load)

    while True:
      if monitor.max_load > worker.target:
        print("Idle for 5s with load %s" % monitor.max_load)
        worker.idle_awhile(5)
        continue

      print("Run for 10s with load %s" % monitor.avg_load)
      worker.run_awhile(10)
      # if monitor.max_load > worker.target:
      #   continue



if __name__ == "__main__":
  Worker.main(target=50)
