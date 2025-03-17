#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --mem=32G
##SBATCH --gres=gpu:1
#SBATCH --time=5-00:00:00
##SBATCH --partition=normal
#SBATCH --partition=besteffort
##SBATCH --qos=gpu
#SBATCH --qos=besteffort
##SBATCH --qos=normal
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mrichart@fing.edu.uy

model=$1
ckpt=$2
dir_data=$3

if [ ! -d /scratch/mrichart/$SLURM_JOB_ID ]; then
   mkdir /scratch/mrichart/$SLURM_JOB_ID
   mkdir /scratch/mrichart/$SLURM_JOB_ID/data
   mkdir /scratch/mrichart/$SLURM_JOB_ID/CheckPoint
   cp additional_functions_$model'_red'.py /scratch/mrichart/$SLURM_JOB_ID/additional_functions.py
   cp train_options_$model'_test.yaml' /scratch/mrichart/$SLURM_JOB_ID/train_options.yaml
   cp model_description_big.yaml /scratch/mrichart/$SLURM_JOB_ID/model_description.yaml
   cp mainEvaluate.py /scratch/mrichart/$SLURM_JOB_ID/
   cp -r CheckPoint/$ckpt /scratch/mrichart/$SLURM_JOB_ID/CheckPoint/
   cp -r $dir_data/test_valid_shuffle /scratch/mrichart/$SLURM_JOB_ID/data/test_valid

fi

echo "Finish copying files"

cd /scratch/mrichart/$SLURM_JOB_ID

source /clusteruy/home/mrichart/miniconda3/bin/activate base
conda activate ignnition

echo "Start evaluation"

python mainEvaluate.py

echo "Finish evaluation"

conda deactivate
conda deactivate


