#!/bin/bash
#SBATCH --job-name=StackOverflowJob
#SBATCH --time=7-00:00:00  # 7 days
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --output=/work/barcomb_lab/Mahdi/StackOverflowDumpReader/logs/job_output_%j.log
#SBATCH --error=/work/barcomb_lab/Mahdi/StackOverflowDumpReader/logs/job_error_%j.log
#SBATCH --partition=single

# Load required modules (if any)
module load python/3.11

# Set up virtual environment
VENV_DIR="/work/barcomb_lab/Mahdi/StackOverflowDumpReader/venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install -r /work/barcomb_lab/Mahdi/StackOverflowDumpReader/requirements.txt
else
    source "$VENV_DIR/bin/activate"
fi

# Ensure .env is in place
cp /work/barcomb_lab/Mahdi/StackOverflowDumpReader/.env $VENV_DIR/
export $(cat $VENV_DIR/.env | xargs)

# Run Python script
python3 /work/barcomb_lab/Mahdi/StackOverflowDumpReader/main.py \
  --input_file_path "/work/barcomb_lab/Mahdi/StackOverflowDumpReader/inputs/Posts.xml" \
  --destination_table "Posts" \
  --start_line_number 22692142 \
  --convert_to_md True
