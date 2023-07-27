import numpy as np
import h5py
import os

simulation_time = 0.020 # in ns

os.chdir('run1')

f = h5py.File('ANALYSIS/DEFAULT/assign.h5','r')
dset=f['nsegs']
dset=np.array(dset)
print(np.sum(dset)*simulation_time)
print(dset.shape)

np.savetxt('nsegs_1.txt',np.cumsum(dset)*simulation_time)

f = h5py.File('ANALYSIS/DEFAULT/direct.h5','r')
dset=f['rate_evolution']
dset=np.array(dset[:,0,1])
np.savetxt('rate_evolution_F_U_1.txt',dset)

dset=f['rate_evolution']
dset=np.array(dset[:,1,0])
np.savetxt('rate_evolution_U_F_1.txt',dset)

os.chdir('../run2')

f = h5py.File('ANALYSIS/DEFAULT/assign.h5','r')
dset=f['nsegs']
dset=np.array(dset)
print(np.sum(dset)*simulation_time)
print(dset.shape)

np.savetxt('nsegs_2.txt',np.cumsum(dset)*simulation_time)

f = h5py.File('ANALYSIS/DEFAULT/direct.h5','r')
dset=f['rate_evolution']
dset=np.array(dset[:,0,1])
np.savetxt('rate_evolution_F_U_2.txt',dset)

dset=f['rate_evolution']
dset=np.array(dset[:,1,0])
np.savetxt('rate_evolution_U_F_2.txt',dset)

os.chdir('../run3')

f = h5py.File('ANALYSIS/DEFAULT/assign.h5','r')
dset=f['nsegs']
dset=np.array(dset)
print(np.sum(dset)*simulation_time)
print(dset.shape)

np.savetxt('nsegs_3.txt',np.cumsum(dset)*simulation_time)

f = h5py.File('ANALYSIS/DEFAULT/direct.h5','r')
dset=f['rate_evolution']
dset=np.array(dset[:,0,1])
np.savetxt('rate_evolution_F_U_3.txt',dset)

dset=f['rate_evolution']
dset=np.array(dset[:,1,0])
np.savetxt('rate_evolution_U_F_3.txt',dset)
