# -*- coding: utf-8 -*-
#!/usr/bin/python                        
##################################################
# AUTHOR : Yandi LI
# CREATED_AT : 2018-11-01
# LAST_MODIFIED : Mon 05 Nov 2018 02:49:05 PM CST
# USAGE : python test2.py
# PURPOSE : TODO
##################################################
from __future__ import division
from numba import cuda
import numpy
import math

# cuda.select_device(1)

# CUDA kernel
@cuda.jit
def my_kernel(io_array):
    pos = cuda.grid(1)
    tx = cuda.threadIdx.x 
    if pos < io_array.size:
        io_array[pos] += tx # do the computation

# Host code   
data = numpy.zeros(512)
# d_data = cuda.to_device(data)
threadsperblock = 128
blockspergrid = 2 # int(math.ceil(data.shape[0] / threadsperblock))
print(blockspergrid)
while True:
  my_kernel[blockspergrid, threadsperblock](data)
# print(data)
