#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import h5py
import sys

def pull_data(n_iter, iter_group):
    auxdata = iter_group['auxdata']['corea_vdw'][:,:]
    pcoord = iter_group['pcoord'][:,:,0]
    with open("corea_vdw.txt", "ab") as f:
        np.savetxt(f, auxdata)
    #with open("pcoord1.txt", "ab") as f:
        #np.savetxt(f, pcoord)
    data = np.dstack((pcoord, auxdata))
    return data

def avg_2d(hist, midpoints, binbounds):
    #plt.title('TEST')
    plt.xlabel('RBD COM')
    plt.ylabel('Core A van der Waals Energy')
