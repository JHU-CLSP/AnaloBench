#!/bin/bash -l
#SBATCH -A danielk_gpu
#SBATCH --job-name=tulu70
#SBATCH --time=32:00:00
#SBATCH --output="Log-tulu70"
#SBATCH --partition=a100
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --mem=150G
#SBATCH --gres=gpu:4
#SBATCH --mail-type=end,fail
#SBATCH --mail-user=xye23@jhu.edu
#SBATCH --export=ALL

module load gcc/9.3.0
module load cuda/12.1.0
module load anaconda
source activate test
nvidia-smi -l 5 > gpu_usage-tulu70.log &
PID=$!
python code/classification_multi.py -t S1 -mn tulu70 -mh allenai/tulu-2-70b -b 5
kill $PID