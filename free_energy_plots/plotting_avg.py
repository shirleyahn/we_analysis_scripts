#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import h5py

hist1 = np.loadtxt('hist1.txt')
hist2 = np.loadtxt('hist2.txt')
hist3 = np.loadtxt('hist3.txt')
hist = (hist1+hist2+hist3)/3.0
for i in range(hist1.shape[0]):
    for j in range(hist1.shape[1]):
        if hist1[i][j] == np.inf:
            hist1[i][j] = 0.0
        else:
            hist1[i][j] = np.exp(-hist1[i][j])
        if hist2[i][j] == np.inf:
            hist2[i][j] = 0.0
        else:
            hist2[i][j] = np.exp(-hist2[i][j])
        if hist3[i][j] == np.inf:
            hist3[i][j] = 0.0
        else:
            hist3[i][j] = np.exp(-hist3[i][j])
        hist[i][j] = (hist1[i][j]+hist2[i][j]+hist3[i][j])/3.0
hist = hist/np.sum(hist)
for i in range(hist.shape[0]):
    for j in range(hist.shape[1]):
        if hist[i][j] >= 1.0e-8:
            hist[i][j] = -np.log(hist[i][j]) 
        else:
            hist[i][j] = np.inf

x = np.arange(0.0, 11.0, 0.2)
y = np.arange(0.0, 11.0, 0.2)
X, Y = np.meshgrid(x, y)
plt.clf()
plt.contourf(X, Y, hist.transpose()*0.001985875*300)
plt.xlabel(r'RMSD ($\AA$)', fontsize=18)
plt.ylabel(r'R$_{g}$ ($\AA$)', fontsize=18)
plt.colorbar().set_label(label='kcal/mol',size=18)
plt.axis([0, 10, 3, 11])
plt.savefig('pcoord_hist_avg.eps')
