#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --mem=32G
##SBATCH --gres=gpu:1
#SBATCH --time=3-00:00:00
#SBATCH --partition=besteffort
#SBATCH --qos=besteffort
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mrichart@fing.edu.uy

if [ ! -d /scratch/mrichart/$SLURM_JOB_ID ]; then
   mkdir /scratch/mrichart/$SLURM_JOB_ID
   mkdir /scratch/mrichart/$SLURM_JOB_ID/data
   mkdir /scratch/mrichart/$SLURM_JOB_ID/CheckPoint
   cp additional_functions.py train_options.yaml main.py model_description.yaml /scratch/mrichart/$SLURM_JOB_ID/
   #cp -r CheckPoint/experiment_2024_04_22_11_16_42 /scratch/mrichart/$SLURM_JOB_ID/CheckPoint/
   cp -r ../social-network/data-nano/* /scratch/mrichart/$SLURM_JOB_ID/data/
fi

cd /scratch/mrichart/$SLURM_JOB_ID

source /clusteruy/home/mrichart/miniconda3/bin/activate base
conda activate ignnition

python main.py

cp -r /scratch/mrichart/$SLURM_JOB_ID/CheckPoint/* /clusteruy/home/mrichart/optimaix-maps/ms-gnn/ignnition-models/delay-ms-p95/CheckPoint/

conda deactivate
conda deactivate

