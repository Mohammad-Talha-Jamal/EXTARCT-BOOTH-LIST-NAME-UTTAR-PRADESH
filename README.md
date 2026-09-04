# ECI Voter Roll Extractor (Uttar Pradesh)

Automated extraction of part-wise voter roll data from the **Election Commission of India** website  
(`https://voters.eci.gov.in/download-eroll`) for all Assembly Constituencies in Uttar Pradesh (2026 Final Roll).

## Features
- Reads a list of constituencies from an Excel file.
- Extracts all part numbers and part names for each constituency.
- Saves each constituency’s parts to a separate CSV file.
- Handles pagination, dynamic dropdowns, and spinners.
- Skips already extracted files (resume capability).
- Includes manual overrides for district name mismatches and constituency name corrections.

## Requirements
- Windows OS (or any OS with Edge browser installed)
- Python 3.7+
- Microsoft Edge (Chromium-based)

## Installation

```bash
git clone https://github.com/yourusername/eci-voter-roll-extractor.git
cd eci-voter-roll-extractor
pip install -r requirements.txt