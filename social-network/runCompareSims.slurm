#!/bin/bash

#usage: sbatch runCompareSims.slurm

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=10G
#SBATCH --time=1:00:00
#SBATCH --tmp=4G
#SBATCH --partition=besteffort
#SBATCH --qos=besteffort
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=mrichart@fing.edu.uy
#SBATCH --array=1-10

cd /clusteruy/home/mrichart/optimaix-maps/lqn-models/4tier

source /clusteruy/home/mrichart/miniconda3/bin/activate base
conda activate ignnition 

python 'compareLQN_sim.py' '--input_dir' '/clusteruy/home/mrichart/optimaix-maps/ms-gnn/ignnition-models/4tier/data-reduced/test_valid'

conda deactivate