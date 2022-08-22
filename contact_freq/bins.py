import numpy as np

#a=np.loadtxt('pcoord1.txt')
#hist, bin_edges = np.histogram(a, bins=100)
#a_str = np.array2string(bin_edges, precision=2, separator=',')
#print(a_str[1:-1])

a=np.loadtxt('coreb_vdw.txt')
hist, bin_edges = np.histogram(a, bins=100)
a_str = np.array2string(bin_edges, precision=2, separator=',')
print(a_str[1:-1])
