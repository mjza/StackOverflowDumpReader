#!/bin/bash
#SBATCH --job-name=StackOverflowDump
#SBATCH --output=/work/barcomb_lab/Mahdi/StackOverflowDumpReader/logs/job_output_%j.log
#SBATCH --error=/work/barcomb_lab/Mahdi/StackOverflowDumpReader/logs/job_error_%j.log
#SBATCH --time=7-00:00:00  # 7 days
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G  # Adjust memory as needed
#SBATCH --partition=cpu2023

####### Set environment variables ###############
module load python/3.12.5

# Set up virtual environment
VENV_DIR="/work/barcomb_lab/Mahdi/StackOverflowDumpReader/senv"
if [ ! -d "$VENV_DIR" ]; then
    python -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install -r /work/barcomb_lab/Mahdi/StackOverflowDumpReader/requirements.txt
else
    source "$VENV_DIR/bin/activate"
fi

####### Run your script #########################
python /work/barcomb_lab/Mahdi/StackOverflowDumpReader/main.py \
  --input_file_path /work/barcomb_lab/Mahdi/StackOverflowDumpReader/inputs/Posts.xml \
  --destination_table Posts \
  --start_line_number 22692142 \
  --convert_to_md True
# change start_line_number accordingly 