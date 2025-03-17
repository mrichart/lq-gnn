#!/bin/bash

#usage: sbatch runDataset.slurm <output_dir> <rejection_threshold>

#SBATCH --job-name=generate_dataset
#SBATCH --ntasks=1
#SBATCH --mem=128G
#SBATCH --tmp=32G
#SBATCH --time=2-00:00:00
#SBATCH --partition=normal
#SBATCH --qos=normal
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mrichart@fing.edu.uy

out_dir=$1
rejection_threshold=$2

mkdir /scratch/mrichart/$SLURM_JOB_ID
mkdir /scratch/mrichart/$SLURM_JOB_ID/logs
mkdir /scratch/mrichart/$SLURM_JOB_ID/data
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/raw
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/raw/train
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/raw/validation
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/raw/'test'
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/raw_valid
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/raw_valid/train
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/raw_valid/validation
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/raw_valid/'test'
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/train
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/validation
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/'test'
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/train_valid
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/validation_valid
mkdir /scratch/mrichart/$SLURM_JOB_ID/data/test_valid

rsync -r --include='*.out' /clusteruy/home/mrichart/optimaix-maps/ms-gnn/uqsim-results/social_net/ /scratch/mrichart/$SLURM_JOB_ID/logs

source /clusteruy/home/mrichart/miniconda3/bin/activate base
conda activate ignnition

python generate_dataset.py --input_dir="/scratch/mrichart/$SLURM_JOB_ID/logs" --output_dir="/scratch/mrichart/$SLURM_JOB_ID/data/raw" --train_dir="/scratch/mrichart/$SLURM_JOB_ID/data/train" --validation_dir="/scratch/mrichart/$SLURM_JOB_ID/data/validation" --test_dir="/scratch/mrichart/$SLURM_JOB_ID/data/test"  --output_valid_dir="/scratch/mrichart/$SLURM_JOB_ID/data/raw_valid" --train_valid_dir="/scratch/mrichart/$SLURM_JOB_ID/data/train_valid" --validation_valid_dir="/scratch/mrichart/$SLURM_JOB_ID/data/validation_valid" --test_valid_dir="/scratch/mrichart/$SLURM_JOB_ID/data/test_valid" --input_graph_dir="/clusteruy/home/mrichart/uqsim-power-management-beta/architecture/social_network/json" --rejection_threshold=$rejection_threshold

conda deactivate

cp /scratch/mrichart/$SLURM_JOB_ID/data/train/data.json $out_dir/train/
cp /scratch/mrichart/$SLURM_JOB_ID/data/validation/data.json $out_dir/validation/
cp /scratch/mrichart/$SLURM_JOB_ID/data/test/data.json $out_dir/test/

cp /scratch/mrichart/$SLURM_JOB_ID/data/train_valid/data.json $out_dir/train_valid/
cp /scratch/mrichart/$SLURM_JOB_ID/data/validation_valid/data.json $out_dir/validation_valid/
cp /scratch/mrichart/$SLURM_JOB_ID/data/test_valid/data.json $out_dir/test_valid/

rm -rf /scratch/mrichart/$SLURM_JOB_ID/data
