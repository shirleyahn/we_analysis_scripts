#!/bin/bash
#SBATCH -p v100
#SBATCH -J crawl
#SBATCH -o crawl.%j.%N.out
#SBATCH -e crawl.%j.%N.err
#SBATCH -N 1
#SBATCH -n 40
#SBATCH -t 48:00:00
#SBATCH -A MCB22023 
#SBATCH --mail-type=all
#SBATCH --mail-user=sahn@ucdavis.edu

set -x
cd $SLURM_SUBMIT_DIR
source ~/.profile
export MY_SPECTRUM_OPTIONS="--gpu"
export PATH=$PATH:$HOME/bin
module purge
module load launcher_gpu/1.1
module load cuda/10.2
module load xl/16.1.1
module load mvapich2-gdr/2.3.4
module load gcc/7.3.0
module load amber/20
module load conda
conda activate westpa
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export WEST_SIM_ROOT=$SLURM_SUBMIT_DIR
export PYTHONPATH=/scratch/07418/s3ahn/mdtraj/lib/python3.7/site-packages:/scratch/07418/s3ahn/conda_local/envs/westpa/bin/python
source env.sh || exit 1
env | sort
SERVER_INFO=$WEST_SIM_ROOT/west_zmq_info-$SLURM_JOBID.json
w_crawl wcrawl_functions2.calculate -c wcrawl_functions2.crawler -W west.h5 --debug --first-iter=1 --last-iter=100 --work-manager=processes --n-workers=40 &> w_crawl.log &
wait
