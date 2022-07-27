#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot
import matplotlib.patheffects as path_effects
from durationhistogram import DurationHistogram
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator, LogLocator, NullFormatter)
import plothist
import numpy
import h5py

## TODO: set tau to your resampling time in seconds

tau = 100E-12
concentration = 1

def cum_mean(data, axis=0):
    N_arr = numpy.arange(1, data.shape[axis]+1)
    cumsum = numpy.cumsum(data, axis=axis)
    if axis != 0:
        cumsum = numpy.swapaxes(cumsum, 0, axis)
    for i in range(cumsum.shape[0]):
        cumsum[i] = cumsum[i]/N_arr[i]
    if axis != 0:
        cumsum = numpy.swapaxes(cumsum, 0, axis)
    return cumsum 

def get_iter_idx_range(h5file, fi, li, path):
    iter_start = h5file.attrs['iter_start']
    iter_stop = h5file.attrs['iter_stop']
    fidx = fi-iter_start
    lidx = fidx + (li-fi)
    if fidx < 0:
        raise IndexError('Data from iteration {:d} was requested, but '
                         'data in file {:s} starts at iteration {:d}'\
                         .format(fi, path, iter_start)
                         )
    if lidx > h5file['conditional_fluxes'].shape[0]:
        raise IndexError('Data from iteration {:d} was requested, but '
                         'data in file {:s} ends at iteration {:d}'\
                         .format(li, path, iter_stop-1)
                         )
    return fidx, lidx

def load_conditional_flux(kineticsH5paths, istate, fstate, fi, li):
    cflist = []
    for path in kineticsH5paths:
        h5file = h5py.File(path, 'r+')
        cf = h5file['conditional_fluxes']
        fidx, lidx = get_iter_idx_range(h5file, fi, li, path)
        cflist.append(cf[fidx:lidx,istate, fstate])
    return numpy.vstack(cflist)

def load_total_flux(kineticsH5paths, fstate, fi, li):
    fluxlist = []
    for path in kineticsH5paths:
        h5file = h5py.File(path, 'r+')
        flux = h5file['total_fluxes']
        fidx, lidx = get_iter_idx_range(h5file, fi, li, path)
        fluxlist.append(flux[fidx:lidx, fstate])
    return numpy.vstack(fluxlist)

def load_pops(assignH5paths, istate, fi, li):
    poplist = []
    for path in assignH5paths:
        h5file = h5py.File(path, 'r+')
        pops = h5file['labeled_populations'][fi-1:li, istate].sum(axis=1)
        poplist.append(pops)
    return numpy.vstack(poplist)
            
def calc_rate_from_conditional_flux(kineticsH5paths, assignH5paths, 
                                    istate, fstate, fi, li):
    flux_arr = load_conditional_flux(kineticsH5paths, istate, fstate, 
                                          fi, li)
    pop_arr  = load_pops(assignH5paths, istate, fi, li)
    pop_list = []
    for simpop in pop_arr:
        pop_list.append(cum_mean(simpop))
    pop_arr = numpy.array(pop_list)

    flux_list = [] 
    for simflux in flux_arr:
        flux_list.append(cum_mean(simflux))
    flux_arr = numpy.array(flux_list)
    rates = flux_arr/pop_arr 
    rate_mean = rates.mean(axis=1)     
    rate_se = rates.std(axis=1, ddof=1)/numpy.sqrt(rates.shape[1])
    rate_mean = rate_mean/(tau*concentration)
    rate_se = rate_se/(tau*concentration)
    return rate_mean, rate_se 

def calc_rate_from_total_flux(kineticsH5paths, fstate, 
                              fi, li, durationbinwidth=1):
    durationhistogram = DurationHistogram() 
    durationhistogram.from_list(kineticsH5paths, fstate, firstiter=fi, lastiter=li, 
                                     correction=True, 
                                     binwidth=durationbinwidth)
    flux_arr = load_total_flux(kineticsH5paths, fstate, fi, li)
    summed_flux_arr = numpy.cumsum(flux_arr, axis=1)
    cumulative_integral = numpy.zeros(flux_arr.shape[1]) 
    for i in range(flux_arr.shape[1]):
        val = durationhistogram.integrate(
                                durationhistogram.hist,
                                durationhistogram.edges,
                                ub = i+0.5)
        cumulative_integral[i] = val 
    for i in range(flux_arr.shape[1]):
        correction_factor = numpy.trapz(cumulative_integral[:i+1])
        #if i % 100 == 0: print(correction_factor)
        if correction_factor != 0: summed_flux_arr[:,i] /= correction_factor
    rates = summed_flux_arr 
    rate_mean = rates.mean(axis=1)     
    rate_se = rates.std(axis=1, ddof=1)/numpy.sqrt(rates.shape[1])
    rate_mean = rate_mean/(tau*concentration)
    rate_se = rate_se/(tau*concentration)
    rate_mean_minus_rate_se = rate_mean-rate_se
    rate_mean_plus_rate_se = rate_mean+rate_se
    logle = numpy.log(rate_mean_minus_rate_se, out=numpy.zeros_like(rate_mean_minus_rate_se), where=(rate_mean_minus_rate_se>0))/numpy.log(10)
    logub = numpy.log(rate_mean_plus_rate_se, out=numpy.zeros_like(rate_mean_plus_rate_se), where=(rate_mean_plus_rate_se>0))/numpy.log(10)
    logmean = numpy.log(rate_mean, out=numpy.zeros_like(rate_mean), where=(rate_mean>0))/numpy.log(10)
    xs = numpy.arange(1, li, 1)
    return rate_mean, rate_se 

def main():
    ## TODO: set first iteration (fi), last iteration (li) 
    fi = 1
    li = 600

    istate = 0
    fstate = 1
    directpath = ['direct.h5']
    assignpath = ['assign.h5']
    alex_rates, alex_sem = calc_rate_from_total_flux(directpath, fstate, fi, li)
    f, ax = pyplot.subplots(1,1)
    f.set_size_inches(8,6)
    lb = 0
    binwidth = 20
    halfwidth = binwidth/2
    durations, weights = plothist.from_list(directpath, fstate, fi, li, correction=True, binwidth=10)
    ub = numpy.ceil(durations.max()) 
    edges = numpy.arange(lb, li+binwidth, binwidth, dtype=float)
    #print(edges)
    hist, _ = numpy.histogram(durations, weights=weights, bins=edges, density=True)
    print(li-halfwidth, lb-halfwidth, -1*binwidth)
    print(numpy.arange(li-halfwidth, lb-halfwidth, -1*binwidth, dtype=float))
    factors = 1/numpy.arange(li-halfwidth, lb-halfwidth, -1*binwidth, dtype=float)
    hist = hist*factors
    #print(hist)
    hmax=numpy.max(hist)
    #print(hmax)
    w=numpy.where(hist>hmax*0.99)
    #print(w)
    diff =((numpy.repeat(edges, 1))[2] - (numpy.repeat(edges, 1))[1])/2   
    thex=(numpy.repeat(edges, 1))[w] + diff
    #print(thex)
    ax.semilogy(numpy.repeat(edges*0.1, 2), plothist.convert_to_step(hist), linewidth=0, color='k')
    ax.fill_between(numpy.repeat(edges*0.1, 2), 0, plothist.convert_to_step(hist), facecolor='red', alpha=0.6)
    ax.axvline(x=thex*0.1,  c='grey', linewidth=2, alpha=0.85)

    ## TODO: set appropriate labels and file name
    ax.set_title('Distribution of transition times to the up state', size=16)
    ax.set_xlabel('Transition times (ns)', size=16)
    ax.set_ylabel('Probability', size=16)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    pyplot.savefig('spike_durations.pdf')
if __name__ == "__main__":
    main()


