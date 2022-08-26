import h5py

file1 = h5py.File("ca_coords.h5","r")
file2 = h5py.File("west.h5","a")

for i in range(1,100):
    f1string = 'iterations/iter_'+str(i).zfill(8)+'/auxdata/ca_coords'
    f2string = 'iterations/iter_'+str(i).zfill(8)+'/auxdata/ca_coords'
    print(f2string)
    copy_arr = file1[f1string]
    file2.create_dataset(f2string, data=copy_arr)

file1.close()
file2.close()
