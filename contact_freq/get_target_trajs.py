import os
import sys
import re
import subprocess
import h5py
import numpy as np


MinIter = int(sys.argv[1])
MaxIter = int(sys.argv[2])
TargetBinValMin1 = 0.0 
TargetBinValMax1 = 3.5
TargetBinValMin2 = 0.0
TargetBinValMax2 = 0.0

DataIn = h5py.File("../west.h5", 'r')

FILEOUT = open("a_t415_c_k986.txt", 'w')
#FILEOUT2 = open("pcoord_2.dat", 'w')
#print("iteration ID\t segment ID\n", file=FILEOUT)
"""
for i in range(MinIter,MaxIter+1) :
   if i%100 == 0 : print("Iter ", i)
   ITER = "{0:08}".format(i)
   #num_keys = len(list(DataIn["/iterations/iter_"+ITER].keys()))
   #if num_keys == 8:
   #dset = DataIn["/iterations/iter_"+ITER+"/new_weights/index"]["prev_seg_id"]
   dset = DataIn["/iterations/iter_"+ITER+"/seg_index"]["parent_id"]
   dset1 = np.array(dset[:])
   for j in range(dset1.shape[0]):
       if dset1[j] < 0:
           print(str(i), "\t", str(j), file=FILEOUT)
FILEOUT.close()

"""
for i in range(MinIter,MaxIter+1) :
   #if i%100 == 0 : print("Iter ", i)
   ITER = "{0:08}".format(i)
   SegNum = int(DataIn["/iterations/iter_"+ITER+"/pcoord"].shape[0])
   for j in range(SegNum):
      dset = DataIn["/iterations/iter_"+ITER+"/pcoord"]
      dset1 = np.array(dset[j,1,0])
      auxdata = DataIn["/iterations/iter_"+ITER+"/auxdata/a_t415_c_k986"]
      dset2 = np.array(auxdata[j,1])
      #print(str(dset1[10]), file=FILEOUT)
      #print(str(dset2[10]), file=FILEOUT2)
      #if float(DataIn["/iterations/iter_"+ITER+"/pcoord"].value[j][0][0]) >= TargetBinVal:
      if np.all(np.logical_and(TargetBinValMin1 <= dset2, dset2 < TargetBinValMax1)): #and np.all(np.logical_and(TargetBinValMin2 <= dset2, dset2 <= TargetBinValMax2)):
         print(str(dset1), "\t", str(dset2), file=FILEOUT)
