#!/bin/bash

#SBATCH -J "gpu testing"        #JOB NAME
#SBATCH --nodes=1            #NUMBER OF NODES
#SBATCH --ntasks-per-node=1  #NUMBER OF TASKS PER NODE
#SBATCH --cpus-per-task=5
#SBATCH -p testing
#SBATCH -G 1
#SBATCH -o output2.txt
#SBATCH -e output2.txt

echo "Test on Devana HPC cluster"

module load CUDA/12.1.1
module load Python/3.11.3-GCCcore-12.3.0

module list

source ~/.predict_SchNet/bin/activate

cd ~/predict_SchNet/test

./test.sh  ~/.predict_SchNet/bin/activate

