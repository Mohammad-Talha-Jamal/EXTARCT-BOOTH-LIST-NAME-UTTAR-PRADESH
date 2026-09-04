# Clone repo (if using git)
git clone https://github.com/yourusername/eci-voter-roll-extractor.git
cd eci-voter-roll-extractor

# Setup
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt

# Run
python extract_all_up_resume_fixed.py