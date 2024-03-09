#!/bin/bash -l
#SBATCH -A danielk_gpu
#SBATCH --job-name=mistral16
#SBATCH --time=32:00:00
#SBATCH --output="Log-mistral16"
#SBATCH --partition=a100
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --mem=100G
#SBATCH --gres=gpu:1
#SBATCH --mail-type=end,fail
#SBATCH --mail-user=xye23@jhu.edu
#SBATCH --export=ALL

module load gcc/9.3.0
module load cuda/12.1.0
module load anaconda
source activate test
nvidia-smi -l 5 > gpu_usage-mistral16.log &
PID=$!
python code/t1.py -s S1 -mn mistral -mh mistralai/Mistral-7B-v0.1 -b 4
kill $PID