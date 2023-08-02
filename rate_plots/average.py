import numpy as np
import os

os.chdir('run1')
nsegs1 = np.loadtxt('nsegs_1.txt')
rate1_1 = np.loadtxt('rate_evolution_F_U_1.txt')
rate2_1 = np.loadtxt('rate_evolution_U_F_1.txt')i
# first column: iter_start (Integer) Iteration at which the averaging window begins (inclusive).
# second column: iter_stop (Integer) Iteration at which the averaging window ends (exclusive).
# thid column: expected (Floating-point) Expected (mean) value of the observable as evaluated within this window, in units of inverse tau.
# fourth column: ci_lbound (Floating-point) Lower bound of the confidence interval of the observable within this window, in units of inverse tau.
# (fourth column is substracted by expected value for plotting error bars)
# fifth column: ci_ubound (Floating-point) Upper bound of the confidence interval of the observable within this window, in units of inverse tau.
# (fifth column is substracted by expected value for plotting error bars)
rate1_1[:,3] = rate1_1[:,2]-rate1_1[:,3] 
rate1_1[:,4] = rate1_1[:,4]-rate1_1[:,2]
rate2_1[:,3] = rate2_1[:,2]-rate2_1[:,3]
rate2_1[:,4] = rate2_1[:,4]-rate2_1[:,2]

os.chdir('../run2')
nsegs2 = np.loadtxt('nsegs_2.txt')
rate1_2 = np.loadtxt('rate_evolution_F_U_2.txt')
rate2_2 = np.loadtxt('rate_evolution_U_F_2.txt')
rate1_2[:,3] = rate1_2[:,2]-rate1_2[:,3]
rate1_2[:,4] = rate1_2[:,4]-rate1_2[:,2]
rate2_2[:,3] = rate2_2[:,2]-rate2_2[:,3]
rate2_2[:,4] = rate2_2[:,4]-rate2_2[:,2]

os.chdir('../run3')
nsegs3 = np.loadtxt('nsegs_3.txt')
rate1_3 = np.loadtxt('rate_evolution_F_U_3.txt')
rate2_3 = np.loadtxt('rate_evolution_U_F_3.txt')
rate1_3[:,3] = rate1_3[:,2]-rate1_3[:,3]
rate1_3[:,4] = rate1_3[:,4]-rate1_3[:,2]
rate2_3[:,3] = rate2_3[:,2]-rate2_3[:,3]
rate2_3[:,4] = rate2_3[:,4]-rate2_3[:,2]

min_length = np.min((nsegs1.shape[0], nsegs2.shape[0], nsegs3.shape[0]))
nsegs_avg = (nsegs1[:min_length]+nsegs2[:min_length]+nsegs3[:min_length])/3
min_length = np.min((rate1_1.shape[0], rate1_2.shape[0], rate1_3.shape[0]))
rate1_avg = (rate1_1[:min_length]+rate1_2[:min_length]+rate1_3[:min_length])/3
rate2_avg = (rate2_1[:min_length]+rate2_2[:min_length]+rate2_3[:min_length])/3

# sixth column plots 95% confidence interval
for i in range(rate1_avg.shape[0]):
    rate1_avg[i,5] = 1.96*np.std([rate1_1[i,2], rate1_2[i,2], rate1_3[i,2]])/np.sqrt(3)
    rate2_avg[i,5] = 1.96*np.std([rate2_1[i,2], rate2_2[i,2], rate2_3[i,2]])/np.sqrt(3)

os.chdir('..')
np.savetxt('nsegs_1.txt', nsegs_avg)
np.savetxt('rate_evolution_F_U_1.txt', rate1_avg)
np.savetxt('rate_evolution_U_F_1.txt', rate2_avg)
