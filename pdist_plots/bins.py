import numpy as np
import h5py
import os

pcoord_dim_num = 1
auxdata_name = 'rbdc_elec'
end_iter = 271

fwest = h5py.File('../west.h5','r')

if os.path.exists("pcoord"+str(pcoord_dim_num)+".txt"):
    os.remove("pcoord"+str(pcoord_dim_num)+".txt")
if os.path.exists(str(auxdata_name)+".txt"):
    os.remove(str(auxdata_name)+".txt")

for i in range(1,end_iter):
    fstring = 'iterations/iter_'+str(i).zfill(8)+'/pcoord'
    pcoord_data = fwest[fstring]
    dset = np.array(pcoord_data[:,:,pcoord_dim_num-1])
    with open("pcoord"+str(pcoord_dim_num)+".txt", "ab") as f:
        np.savetxt(f, dset)
    fstring = 'iterations/iter_'+str(i).zfill(8)+'/auxdata/'+str(auxdata_name)
    auxdata = fwest[fstring]
    with open(str(auxdata_name)+".txt", "ab") as f:
        np.savetxt(f, auxdata)

a=np.loadtxt("pcoord"+str(pcoord_dim_num)+".txt")
hist, bin_edges = np.histogram(a, bins=100)
bin_edges[0] -= 0.01
bin_edges[-1] += 0.01
a_str = np.array2string(bin_edges, formatter={'float_kind':lambda x: "%.2f" % x}, separator=',', max_line_width=100000000)
print("w_pdist -W ../west.h5 --construct-dataset plotting.pull_data -o TEST_pdist.h5 -b [", end="")
print(a_str, end="")
print(",", end="")
a=np.loadtxt(str(auxdata_name)+".txt")
hist, bin_edges = np.histogram(a, bins=100)
bin_edges[0] -= 0.01
bin_edges[-1] += 0.01 
a_str = np.array2string(bin_edges, formatter={'float_kind':lambda x: "%.2f" % x}, separator=',', max_line_width=100000000)
print(a_str, end="")
print("]", end="")
