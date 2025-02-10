#!/bin/bash
#SBATCH --job-name=StackOverflowJob
#SBATCH --time=6-23:59:59  # 7 days
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --output=job_output_%j.log
#SBATCH --error=job_error_%j.log
#SBATCH --partition=single

# Load required modules
module load python/3.8  # Adjust Python version if necessary

# Define paths
WORK_DIR="/work/barcomb_lab/Mahdi/StackOverflowDumpReader"
RUN_DIR="$SLURM_TMPDIR/StackOverflowDumpReader"

# Create temporary working directory and copy files
mkdir -p "$RUN_DIR"
cp -r "$WORK_DIR"/* "$RUN_DIR"

# Copy the .env file to the working directory
cp "$WORK_DIR/.env" "$RUN_DIR/.env"

# Move to the working directory
cd "$RUN_DIR"

# Create and activate a virtual environment (if not already available)
VENV_DIR="$RUN_DIR/venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# Install dependencies
pip install --upgrade pip
pip install python-dotenv colored psycopg2-binary markdownify beautifulsoup4 html2text

# Run the script
python3 main.py \
  --input_file_path "$RUN_DIR/inputs/Posts.xml" \
  --destination_table "Posts" \
  --start_line_number 22692142 \
  --convert_to_md True
