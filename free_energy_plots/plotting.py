#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import h5py

def pull_data(n_iter, iter_group):
    pcoord1 = iter_group['pcoord'][:,:,0]
    pcoord2 = iter_group['pcoord'][:,:,1]
    data = np.dstack((pcoord1, pcoord2))
    return data

def avg_2d(hist, midpoints, binbounds):
    #plt.title('Free energy')
    for i in range(hist.shape[0]):
        for j in range(hist.shape[1]):
            if hist[i][j] == np.inf:
                hist[i][j] = 0.0
            else:
                hist[i][j] = np.exp(-hist[i][j])
    hist = hist/np.sum(hist)
    np.savetxt('hist.txt',hist)
    for i in range(hist.shape[0]):
        for j in range(hist.shape[1]):
            if hist[i][j] >= 1.0e-8:
                hist[i][j] = -np.log(hist[i][j])
            else:
                hist[i][j] = np.inf
    x = np.arange(0.0, 10.2, 0.2)
    y = np.arange(0.0, 10.2, 0.2)
    X, Y = np.meshgrid(x, y)
    plt.clf()
    #levels = np.linspace(0.0, 12.0, 12)
    plt.contourf(X, Y, hist.transpose()*0.001985875*300) #levels=levels)
    plt.xlabel(r'RMSD ($\AA$)') 
    plt.ylabel(r'R$_{g}$ ($\AA$)')
    plt.colorbar(label='kcal/mol')
    plt.axis([0, 9, 3, 10])
