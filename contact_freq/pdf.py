import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pylab as pylab

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

fig = plt.figure(figsize=(24,12))
ax = fig.add_subplot(111)
numBins = 160
n1, bins1, patches1 = plt.hist(dist1[:,0], numBins, label='A T415 - C K986', color='fuchsia',alpha=0.8, rwidth=0.9, weights=np.ones(len(dist1))/len(dist1), density=False, range=(50.0, 90.0))
ax.set_xlabel('RBD-core distance ($\AA$)',labelpad=20)
ax.set_ylabel('Contact frequency',labelpad=20)
plt.legend(loc=1)
plt.ylim([0, 0.3])
fig.savefig('contact_freq.png', bbox_inches='tight')
