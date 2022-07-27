iternum=600

w_pdist -W iter_${iternum}_west.h5
plothist average pdist.h5 "0::RBD COM" "1::RBD RMSD"
mv hist.pdf iter_${iternum}_pcoord_hist.pdf
plothist evolution pdist.h5 "0::RBD COM"
mv hist.pdf iter_${iternum}_com_hist.pdf
plothist evolution pdist.h5 "1::RBD RMSD"
mv hist.pdf iter_${iternum}_rmsd_hist.pdf
mv pdist.h5 iter_${iternum}_pcoord_pdist.h5
