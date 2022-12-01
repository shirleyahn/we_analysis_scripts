import numpy as np
import h5py

walker_sim_time = 0.020 # in ns

f = h5py.File('ANALYSIS/DEFAULT/assign.h5','r')
dset=f['nsegs']
dset=np.array(dset)
np.savetxt('nsegs.txt',np.cumsum(dset)*walker_sim_time) # this is to get the molecular time from WE sim

f = h5py.File('ANALYSIS/DEFAULT/direct.h5','r')
dset=f['rate_evolution']
dset=np.array(dset[:,0,1]) # rate evolution going from state 0 (Folded) to state 1 (Unfolded)
np.savetxt('rate_evolution_F_U.txt',dset)
