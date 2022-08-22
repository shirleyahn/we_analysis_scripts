import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pylab as pylab
from matplotlib.ticker import AutoMinorLocator
params = {'font.family': 'sans-serif',
          'font.sans-serif': 'Helvetica',
         'legend.fontsize': '36',
         'figure.figsize': (24,12),
         'axes.labelsize': '36',
         'axes.titlesize': '36',
         'xtick.labelsize': '36',
         'ytick.labelsize': '36'}
pylab.rcParams.update(params)

dist1 = np.loadtxt('a_t415_c_k986.txt')
#dist2 = np.loadtxt('a_r457_b_d364.txt')
dist3 = np.loadtxt('a_k462_b_d198.txt')
dist4 = np.loadtxt('a_d427_c_k986.txt')
dist5 = np.loadtxt('a_r408_c_d405.txt')
dist6 = np.loadtxt('a_r466_b_e132.txt')
#dist7 = np.loadtxt('a_d428_c_r454.txt')

fig = plt.figure(figsize=(24,12))
ax = fig.add_subplot(111)
numBins = 160
n1, bins1, patches1 = plt.hist(dist1[:,0], numBins, label='A T415 - C K986', color='fuchsia',alpha=0.8, rwidth=0.9, weights=np.ones(len(dist1))/len(dist1), density=False, range=(50.0, 90.0))
#n2, bins2, patches2 = plt.hist(dist2[:,0], numBins, label='A R457 - B D364', color='darkviolet',alpha=0.8, rwidth=0.9, weights=np.ones(len(dist2))/len(dist2), density=False, range=(50.0, 90.0))
n3, bins3, patches3 = plt.hist(dist3[:,0], numBins, label='A K462 - B D198', color='darkorchid',alpha=0.8, rwidth=0.9, weights=np.ones(len(dist3))/len(dist3), density=False, range=(50.0, 90.0))
n4, bins4, patches4 = plt.hist(dist4[:,0], numBins, label='A D427 - C K986', color='mediumpurple',alpha=0.8, rwidth=0.9, weights=np.ones(len(dist4))/len(dist4), density=False, range=(50.0, 90.0))
n5, bins5, patches5 = plt.hist(dist5[:,0], numBins, label='A R408 - C D405', color='cornflowerblue',alpha=0.8, rwidth=0.9, weights=np.ones(len(dist5))/len(dist5), density=False, range=(50.0, 90.0))
n6, bins6, patches6 = plt.hist(dist6[:,0], numBins, label='A R466 - B E132', color='deepskyblue',alpha=0.8, rwidth=0.9, weights=np.ones(len(dist6))/len(dist6), density=False, range=(50.0, 90.0))
#n7, bins7, patches7 = plt.hist(dist7[:,0], numBins, label='A D428 - C R454', color='aqua',alpha=0.8, rwidth=0.9, weights=np.ones(len(dist7))/len(dist7), density=False, range=(50.0, 90.0))
ax.set_xlabel('RBD-core distance ($\AA$)',labelpad=20)
ax.set_ylabel('Contact frequency',labelpad=20)
plt.legend(loc=1)
plt.ylim([0, 0.3])
fig.savefig('contact_freq.png', bbox_inches='tight')
