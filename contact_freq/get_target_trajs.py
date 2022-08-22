import sys
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

for i in range(MinIter,MaxIter+1) :
   #if i%100 == 0 : print("Iter ", i)
   ITER = "{0:08}".format(i)
   SegNum = int(DataIn["/iterations/iter_"+ITER+"/pcoord"].shape[0])
   for j in range(SegNum):
      dset = DataIn["/iterations/iter_"+ITER+"/pcoord"]
      dset1 = np.array(dset[j,1,0])
      auxdata = DataIn["/iterations/iter_"+ITER+"/auxdata/a_t415_c_k986"]
      dset2 = np.array(auxdata[j,1])
      if np.all(np.logical_and(TargetBinValMin1 <= dset2, dset2 < TargetBinValMax1)):
         print(str(dset1), "\t", str(dset2), file=FILEOUT)
