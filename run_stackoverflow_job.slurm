#!/bin/bash
#SBATCH --job-name=StackOverflowJob
#SBATCH --time=7-00:00:00  # 7 days
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --output=job_output_%j.log
#SBATCH --error=job_error_%j.log
#SBATCH --partition=single

# Load required modules
module load python/3.8  # Adjust if necessary

# Create and activate a virtual environment
VENV_DIR="/work/barcomb_lab/Mahdi/StackOverflowDumpReader/venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# Install dependencies if not already installed
pip install --upgrade pip
pip install python-dotenv colored psycopg2-binary markdownify beautifulsoup4 html2text

# Run the script
python3 /work/barcomb_lab/Mahdi/StackOverflowDumpReader/main.py \
  --input_file_path "/work/barcomb_lab/Mahdi/StackOverflowDumpReader/inputs/Posts.xml" \
  --destination_table "Posts" \
  --start_line_number 22692142 \
  --convert_to_md True
