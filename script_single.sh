#!/bin/bash -l
#SBATCH -A danielk_gpu
#SBATCH --job-name=ze
#SBATCH --time=32:00:00
#SBATCH --output="Log-ze"
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
nvidia-smi -l 5 > gpu_usage-ze.log &
PID=$!
python code/classification_single.py -t S1 -mn zephyrbeta -mh HuggingFaceH4/zephyr-7b-beta -b 5
kill $PID