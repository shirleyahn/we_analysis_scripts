import h5py
import numpy as np

simtime = 0.1 # in ns
f = h5py.File('west.h5','r')
total_simtime = np.sum(f['summary']['n_particles'])*0.1/1000
total_walltime = np.sum(f['summary']['walltime'])/60.0/60.0/24.0 # in seconds
print('total simtime = '+str(total_simtime)+' microseconds')
print('total walltime = '+str(total_walltime)+' days')
