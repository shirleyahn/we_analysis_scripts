# we_analysis_scripts

Some of the scripts have been originally prepared by Terra Sztain,
Anthony Bogetti, John Russo, and others from Prof. Lillian
Chong's group (University of Pittsburgh) and have went through
several modifications.

- simtime_walltime.py: prints out the total simulation time and
walltime for the WE simulation of interest using west.h5
- w_pdist.sh: plots average free energy landscape and evolution
of progress coordinate values - useful to keep track of progress
of your currently running WE simulation (useful tip: periodically
make copies of west.h5 in case the main one gets ruined)
- durations folder: includes scripts that extract iteration #s and
segment #s that correspond to when and which segment/walker made
the transition of interest (e.g., going from A to B), the weights
of those corresponding segments/walkers, and the duration of
those transitions. The main script to execute is plot_duration.py.
Make sure to change the TODOs in plot_duration.py. The script
will also generate a distribution plot of durations in PDF form.
- traj_concatenate folder: includes scripts that concatenate 
iterations to make a trajectory. Often times, we will end up
with a list of iteration #s and segment #s (e.g., from durations 
folder) and will want to make trajectories of each transition.
traj.sh will trace a particular iteration # and segment # so
that it obtains all of the past conformations of this particular
segment/walker. runtraj.sh is the main script to execute with a
list of iteration #s and segment #s like up_pathways.txt.
