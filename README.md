# ECI Booth List Extractor (Uttar Pradesh)

Automated extraction of part-wise Booth List data from the **Election Commission of India** website  
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

 📦 Installation

Follow these steps to get the tool running on your machine.

# Prerequisites
- Windows operating system (7, 10, or 11)
- Microsoft Edge (Chromium‑based) installed – [Download here](https://www.microsoft.com/edge)
- Python 3.7 or higher – [Download here](https://python.org) (make sure to check *“Add Python to PATH”* during installation)



# Step 1: Clone the repository

Open PowerShell and run:

```bash

git clone https://github.com/Mohammad-Talha-Jamal/EXTARCT-BOOTH-LIST-NAME-UTTAR-PRADESH.git
cd EXTARCT-BOOTH-LIST-NAME-UTTAR-PRADESH
pip install -r requirements.txt

```
> No Git? Download the ZIP from the GitHub page and extract it, then use `cd` to navigate into the extracted folder.



# Step 2: (Optional) Create a virtual environment

This keeps dependencies isolated. Run:
```
python -m venv venv
.\venv\Scripts\Activate
```

You’ll see `(venv)` appear at the start of your prompt.



# Step 3: Install required packages
```
pip install -r requirements.txt
```

If a `requirements.txt` file is not present, install the dependencies manually:

```
pip install pandas openpyxl selenium webdriver-manager

```


# Step 4: Prepare your input file

Place your `Book1.xlsx` file in the same folder as the script.  
The Excel file must contain these three columns (exact names):

| Column Name | Description |
|-|-|
| `CONSTITUENCY NUMBER` | Integer (e.g., `247`) |
| `CONSTITUENCY NAME` | Name (e.g., `Vishwanathganj`) |
| `DISTRICT` | District name (e.g., `Prayagraj`) |

> 💡 A sample `Book1.xlsx` is already provided in the repo – you can edit it with your own data.



# Step 5: Run the script
```
python extract_all_up_booth_list.py
```

> ⚠️ The script will open a minimized Edge browser and begin extracting data automatically. Do not interact with the browser while it runs.



# Step 6: Output

- Each constituency’s part list is saved as a separate CSV file:
  
  {const_number} - {const_name}.csv
  
- The script skips already processed files – so you can safely restart it if interrupted.



# ❗ Troubleshooting

| Problem | Solution |
||-|
| “pip is not recognized” | Reinstall Python and ensure *“Add to PATH”* is checked. |
| “ExecutionPolicy” restriction | Run PowerShell as Administrator: <br> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| WebDriver not found | The script auto‑downloads EdgeDriver via `webdriver‑manager`. Ensure you have an active internet connection. |
| ModuleNotFoundError | Run `pip install -r requirements.txt` again. |
| Browser pops up instead of minimized | That’s normal – the script minimizes it automatically after launch. |



# 📌 Quick one‑liner (if you already have everything set up)
```
git clone https://github.com/Mohammad-Talha-Jamal/EXTARCT-BOOTH-LIST-NAME-UTTAR-PRADESH.git ; cd EXTARCT-BOOTH-LIST-NAME-UTTAR-PRADESH ; pip install -r requirements.txt ; python extract_all_up_booth_list.py

```


