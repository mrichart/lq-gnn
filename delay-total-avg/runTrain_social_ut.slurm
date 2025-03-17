#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --mem=32G
##SBATCH --gres=gpu:1
#SBATCH --time=5-00:00:00
#SBATCH --partition=normal
##SBATCH --partition=besteffort
##SBATCH --qos=gpu
##SBATCH --qos=besteffort
#SBATCH --qos=normal
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mrichart@fing.edu.uy

if [ ! -d /scratch/mrichart/$SLURM_JOB_ID ]; then
   mkdir /scratch/mrichart/$SLURM_JOB_ID
   mkdir /scratch/mrichart/$SLURM_JOB_ID/data
   mkdir /scratch/mrichart/$SLURM_JOB_ID/CheckPoint
   cp additional_functions_social_ut_red.py /scratch/mrichart/$SLURM_JOB_ID/additional_functions.py
   cp train_options_social_ut.yaml /scratch/mrichart/$SLURM_JOB_ID/train_options.yaml
   cp model_description_big.yaml /scratch/mrichart/$SLURM_JOB_ID/model_description.yaml
   cp main.py /scratch/mrichart/$SLURM_JOB_ID/
   #cp -r CheckPoint/experiment_2024_05_29_12_04_31 /scratch/mrichart/$SLURM_JOB_ID/CheckPoint/
   cp -r ../social-network-ut/data-reduced/train_valid /scratch/mrichart/$SLURM_JOB_ID/data/
   cp -r ../social-network-ut/data-reduced/validation_valid /scratch/mrichart/$SLURM_JOB_ID/data/

fi

echo "Finish copying files"

cd /scratch/mrichart/$SLURM_JOB_ID

source /clusteruy/home/mrichart/miniconda3/bin/activate base
conda activate ignnition

echo "Start training"

python main.py

echo "Finish training"

cp -r /scratch/mrichart/$SLURM_JOB_ID/CheckPoint/* /clusteruy/home/mrichart/optimaix-maps/ms-gnn/ignnition-models/delay-total-avg/CheckPoint/

conda deactivate
conda deactivate

