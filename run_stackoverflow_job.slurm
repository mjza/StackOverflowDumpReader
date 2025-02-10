#!/bin/bash
#SBATCH --job-name=StackOverflowJob
#SBATCH --time=7-00:00:00  # 7 hours
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --output=/work/barcomb_lab/Mahdi/logs/job_output_%j.log
#SBATCH --error=/work/barcomb_lab/Mahdi/logs/job_error_%j.log
#SBATCH --partition=single  # Use the correct partition

# Define paths
WORK_DIR="/work/barcomb_lab/Mahdi/StackOverflowDumpReader"
RUN_DIR="$SLURM_TMPDIR/StackOverflowDumpReader"

# Create working directory in SLURM temporary storage
mkdir -p "$RUN_DIR"
cp -r "$WORK_DIR"/* "$RUN_DIR"
cp "$WORK_DIR/.env" "$RUN_DIR/.env"

# Move to the working directory
cd "$RUN_DIR"

# Create and activate virtual environment using system Python
VENV_DIR="$RUN_DIR/venv"
if [ ! -d "$VENV_DIR" ]; then
    /usr/bin/python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# Ensure pip is available and upgrade it
python3 -m ensurepip
pip install --upgrade pip

# Install dependencies
pip install python-dotenv colored psycopg2-binary markdownify beautifulsoup4 html2text

# Run the script using system Python
python3 main.py \
  --input_file_path "$RUN_DIR/inputs/Posts.xml" \
  --destination_table "Posts" \
  --start_line_number 22692142 \
  --convert_to_md True
