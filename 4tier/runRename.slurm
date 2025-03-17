#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=4:00:00
#SBATCH --partition=besteffort
#SBATCH --qos=besteffort
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mrichart@fing.edu.uy

./renameLogs.sh
