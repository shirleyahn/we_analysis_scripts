#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

def pull_data(n_iter, iter_group):
    auxdata = iter_group['auxdata']['rbdc_elec'][:,:]
    pcoord = iter_group['pcoord'][:,:,0]
    data = np.dstack((pcoord, auxdata))
    return data

def avg_2d(hist, midpoints, binbounds):
    #plt.title('TEST')
    plt.xlabel('RBD COM')
    plt.ylabel('RBD C Electrostatic Energy')
