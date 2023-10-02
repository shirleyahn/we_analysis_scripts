import numpy as np
from scipy.signal import fftconvolve
import westpa.mclib as mclib

# calculate autocorrelation function C(t)
# C(t_d) = 1/(t_max)\sum_{t_0}^{t_max}A(t_0)A(t_0+t_d)
# where A(t) is the property of interest like flux or number of arrivals
# where t_max = L - t_d/delta_t where L is the total simulation length and delta_t is tau or timestep

data = np.loadtxt('arrivals.txt')  # arrivals from down state to open state for instance
data_mean = np.mean(data)
dmm = data - data_mean
acorr = fftconvolve(dmm,dmm[::-1])
acorr = acorr[len(acorr)//2:]
acorr /= acorr[0]
np.savetxt('autocorrelation_function.txt',acorr)
avg, lb_ci, ub_ci, sterr, correl_len = mclib.mcbs_ci_correl({'dataset': data}, estimator=(lambda stride, dataset: np.mean(dataset)), alpha=0.05, n_sets=1000, autocorrel_alpha=0.05, subsample=np.mean, do_correl=True, mcbs_enable=True)
print("correlation length "+str(correl_len))
print("mean "+str(avg))
print("lower CI "+str(lb_ci))
print("upper CI "+str(ub_ci))
