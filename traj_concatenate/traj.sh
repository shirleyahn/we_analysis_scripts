#!/bin/bash


# --------------------------------
# Amber Trajectory Tool for WESTPA
# --------------------------------
# 
# Written by Anthony Bogetti on 28.08.18
# 
# This script will stitch together a trajectory file from your Amber-WESTPA
# simulation that can be viewed in VMD or another molecular dynmaics 
# visualization software.  Run this script with the command ./amberTraj.sh
# from the same directory where the west.h5 file from your WESTPA simulation
# is located.  The results of this analysis will be stored in a new folder
# called trajAnalysis as the file trace.nc.  Load trace.nc into VMD to 
# visualize the trajectory.  As a note, you will need to have your computer
# configured to run w_succ from the WESTPA software package and cpptraj from 
# the Amber software package.  Though, if the simulation has completed successfully,
# these commands will most likely be ready to run.


# The variables defined below are the name of the new analysis directory that
# will be created and the name of an intermediate file in the process of 
# stitching together the trajectory file.
dir=trajAnalysis
file=path.txt
TOP=/mnt/NFS/original/CONFIG/closed_strip.prmtop
siter=ITER
sseg=SEG
#export CPPTRAJ=$AMBERHOME/bin/cpptraj.MPI

# The analysis directory is then made and the parameter file for the system is
# copied into it.  All analysis will take place within this directory.
#if [ -d "$dir" ]; then
  #rm -r $dir
#fi
mkdir $dir

# The topology file for the system is copied into the trajectory
# analysis directory.
cp $TOP $dir

# The input file for cpptraj is prepared.
if [ -f "$dir/cpptraj.in" ]; then
  rm "$dir/cpptraj.in"
fi

# w_trace is run, generating a history of the successful trajectory specified
# above.  This will create a list of all of the iterations and segments that
# need to be stitched together to create a smooth, viewable, successful trajectory.
w_trace -W plots/iter_600_west.h5 $siter:$sseg

# Output files from w_trace are moved into the trajAnalysis directory.
mv $(echo 'traj_'$siter'_'$sseg'_trace.txt') $dir
mv trajs.h5 $dir
cd $dir

# initial state of the system, which doesn't have an iter:seg ID)
cat $(echo 'traj_'$siter'_'$sseg'_trace.txt') | tail -n +9 > path.txt

# users, however, the following should work just fine.

while read file; do
	iter=$(echo $file | awk '{print $1}')
	seg=$(echo $file | awk '{print $2}')
        #if [ $iter -lt 252 ];
        #then
	    #filestring='../../TRSNS_TRJ/'$(printf "%06d" $iter)'/'$(printf "%06d" $seg)'/''seg.nc'
        #else 
        filestring='../traj_segs/'$(printf "%06d" $iter)'/'$(printf "%06d" $seg)'/''seg.nc'
        #fi
	echo "trajin $filestring" >> cpptraj.in	
done < "path.txt"

# These two lines will specify the name of the file where the stitched trajectory
# is written to and a line to commence the cpptraj run
printf "trajout trace_$siter""_$sseg"".dcd\nrun" >> cpptraj.in 

# Now, cpptraj is called using the parameter file and the cpptraj.in file
# that was created above as input.  The text displayed to the terminal is written
# to the file traj.log.
cpptraj.cuda -p $TOP -i cpptraj.in > traj.log

echo Trajectory file creation is complete.
echo To view your trajectory, load the parameter file into VMD followed by the trace.nc file, both located in the trajAnalysis directory.

# The intermediary files are removed to clean up the analysis directory.
rm trajs.h5
cd ..
