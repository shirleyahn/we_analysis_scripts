#!/usr/bin/env python
# 
# wcrawl_functions.py
#
# Written 15.09.29; updated 18.04.10 by Alex DeGrave
from __future__ import print_function, division; __metaclass__ = type
import logging
import numpy
import h5py
import os
import sys
import io
import tarfile
from westpa.core import h5io
from westpa.core.segment import Segment
from westpa.cli.tools.w_crawl import WESTPACrawler
from itertools import combinations, product
import mdtraj as md
import glob as glob

log = logging.getLogger(__name__)
log.setLevel("DEBUG")

class IterationProcessor(object):
    '''
    This class performs analysis on each iteration.  It should contain a method
    ``process_iteration``, which may be called as 
    ``process_iteration(self, n_iter, iter_group)``, where ``n_iter`` refers to
    the weighted ensemble iteration index, and ``iter_group`` is the HDF5 group 
    for the given iteration. The method should return an array or other values, 
    which the ``process_iter_result`` method of the ``Crawler`` class recieves 
    as the argument ``result``. 
    '''
    #TODO: define all of the properties below
    # Store the location of the PDB file to be used as the topology 
    base_sim_path = '/scratch/07418/s3ahn/original'

    # Store the location of the PDB file to be used as the topology
    child_topology_filename = f'{base_sim_path}/CONFIG/closed_strip.pdb'
    parent_topology_filename = f'{base_sim_path}/CONFIG/closed.pdb'

    # Define the pattern used for finding each segment's traj files
    child_traj_pattern = f'{base_sim_path}' + '/traj_segs/{n_iter:06d}/{seg_id:06d}/seg.nc'
    parent_traj_pattern = f'{base_sim_path}' + '/traj_segs/{parent_iter:06d}/{parent_id:06d}/seg.nc'

    iter_pattern = 'iterations/iter_{n_iter:08d}'

    nframes = 2 

    def __init__(self):
        '''
        Initialize the IterationProcessor class
        '''
        #log.debug(f"Loading topology from {self.topology_filename}")
        self.child_topology = md.load_topology(self.child_topology_filename)
        self.parent_topology = md.load_topology(self.parent_topology_filename)

    def process_iteration(self, n_iter, iter_group):
        '''
        The main analysis function that w_crawl calls for each iteration.
        This should be changed based on your analysis. This method could
        contain all the code for your analysis, or it could call an outside
        function. 

        ----------
        Parameters
        ----------
        n_iter: (int) The index of the weighted ensemble iteration for which
          analysis should be performed.
        iter_group: (H5py group) The hdf5 group corresponding to iteration
          n_iter, from the the main WESTPA data file (typically west.h5)

        -------
        Returns
        -------
        result: (numpy.ndarray) In general this could be an object, which is
          later processed by Crawler.process_iter_result. The array has shape 
          (n_segments, n_timepoints, 1), where dimension 0 indexes the segment, 
          dimension 1 indexes the frame number, and dimension 2 indexes the property of interest.
        '''
        # Find the number of segments in the iteration at hand
        print("starting",n_iter)
        nsegs = iter_group['seg_index'].shape[0]
        parent_iter = n_iter-1

        # The dimensionality of the data you wish to store
        data_dims = 1
        
        # Create an array to hold your data
        iteration_data_array = numpy.zeros((nsegs, self.nframes, data_dims))

        # Iterate over each segment
        for iseg in range(nsegs):
            pathy = self.iter_pattern.format(n_iter=n_iter)
            with h5py.File("west.h5","r") as f:
                parent_seg = int(f[pathy]['seg_index']['parent_id'][iseg])
            if parent_seg < 0:
                parent_seg = parent_seg*-1
            for _idx, traj_pattern in enumerate([self.parent_traj_pattern, self.child_traj_pattern]):
                try:
                    traj_path = traj_pattern.format(n_iter=n_iter, seg_id=iseg)
                except KeyError:
                    traj_path = traj_pattern.format(parent_iter=parent_iter, parent_id=parent_seg)

                try:
                    group_1 = list(range(1969, 1977))
                    group_2 = list(range(2016, 2022))
                    pairs = list(product(group_1, group_2))
                    dist = numpy.amin(md.compute_contacts(md.formats.NetCDFTrajectoryFile(traj_path).read_as_traj(self.child_topology), contacts=pairs, scheme='closest')[0])*10.0
                # If this traj doesn't exist, handle it gracefully and put NaNs in the coords
                except OSError:
                    dist = numpy.full(shape=(data_dims), fill_value=numpy.nan)
                
                iteration_data_array[iseg, _idx] = dist

        return iteration_data_array


class Crawler(WESTPACrawler):
    '''
    In this example, w_crawl works as follows:

    We supply the ``Crawler`` class, which handles writing data. The 
    Crawler specifies 3 methods: initialize, finalize, and process_iter_result.

    ``initialize`` is called only once--when w_crawl starts up. The job of 
    initialize is to create the output file (and HDF5 file).

    Like ``initialize``, ``finalize`` is also called only once--when w_crawl
    finishes calculations for all iterations. The job of ``finalize`` is to
    gracefully close the output file, preventing data corruption.

    The method ``process_iter_result`` is called once per weighted ensemble
    iteration. It takes the weighted ensemble iteration (n_iter) and the result
    of the calculations for an iteration (result) as arguments, and stores the
    data in the output file.

    The actual calculations are performed by the IterationProcessor class 
    defined above. In particular, the IterationProcessor.process_iteration 
    method performs the calculations; the return value of this method is passed
    to Crawler.process_iter_result.
    '''

    def initialize(self, iter_start, iter_stop):
        '''
        Create an HDF5 file for saving the data.  Change the file path to
        a location that is available to you. 
        '''
        #TODO: define crawl_property
        self.crawl_property = 'b_n17_b_n165_min'
        self.output_file = h5io.WESTPAH5File(str(self.crawl_property)+'.h5', 'w')
        h5io.stamp_iter_range(self.output_file, iter_start, iter_stop)

    def finalize(self):
        self.output_file.close()

    def process_iter_result(self, n_iter, result):
        '''
        Save the result of the calculation in the output file.

        ----------
        Parameters
        ----------
        n_iter: (int) The index of the weighted ensemble iteration to which
          the data in ``result`` corresponds.
        result: (numpy.ndarray) In general this could be an arbitrary object
          returned by IterationProcessor.process_iteration; here it is a numpy
          array of the center of geometry.
        '''
        # Initialize/create the group for the specific iteration
        iter_group = self.output_file.require_iter_group(n_iter)

        iteration_data_array = result
        
        # Save datasets
        dataset = iter_group.create_dataset('auxdata/'+str(self.crawl_property), 
                                            data=iteration_data_array, 
                                            scaleoffset=6, 
                                            compression=4,
                                            chunks=h5io.calc_chunksize(
                                                    iteration_data_array.shape,
                                                    iteration_data_array.dtype
                                                                       )
                                            )

# Entry point for w_crawl
iteration_processor = IterationProcessor()

def calculate(n_iter, iter_group):
    '''Picklable shim for iteration_processor.process_iteration()'''
    global iteration_processor 
    return iteration_processor.process_iteration(n_iter, iter_group)

crawler = Crawler()
