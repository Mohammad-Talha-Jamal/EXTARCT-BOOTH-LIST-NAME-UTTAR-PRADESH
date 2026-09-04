import time
import csv
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

try:
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    USE_MANAGER = True
except ImportError:
    USE_MANAGER = False
    print("Install webdriver-manager: pip install webdriver-manager")

# ----------------------------------------------------------------------
# MANUAL OVERRIDES
# ----------------------------------------------------------------------
DISTRICT_MAPPING = {
    "Bagpat": "Baghpat",
    "Gautam Budh Nagar": "Gautam Buddha Nagar",
    "Gautam Budh Nagar": "Gautam Buddha Nagar",
    "Lakhimpur Kheri": "Kheri",
    "Allahabad": "Prayagraj",
    "Faizabad": "Ayodhya",
}

CONSTITUENCY_NAME_MAPPING = {
    247: "Vishwanathganj",
}

def setup_edge_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    if USE_MANAGER:
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    else:
        driver = webdriver.Edge(options=options)
    driver.minimize_window()
    return driver

def select_dropdown_by_text(driver, element_name, visible_text, timeout=20):
    select_elem = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.NAME, element_name))
    )
    for option in select_elem.find_elements(By.TAG_NAME, "option"):
        if option.text.strip() == visible_text:
            option.click()
            time.sleep(0.5)
            return True
    # Case-insensitive fallback
    for option in select_elem.find_elements(By.TAG_NAME, "option"):
        if option.text.strip().lower() == visible_text.lower():
            option.click()
            time.sleep(0.5)
            return True
    raise Exception(f"Option '{visible_text}' not found in {element_name}")

def select_assembly_constituency(driver, const_number, const_name):
    full_name = f"{const_number} - {const_name}"
    # Use the hidden <select> – this is reliable
    hidden_select = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "constituency"))
    )
    select = Select(hidden_select)
    try:
        select.select_by_visible_text(full_name)
    except:
        # If exact match fails, try to select by partial text (e.g., "1 - Behat" might have extra spaces)
        for opt in select.options:
            if opt.text.strip() == full_name:
                opt.click()
                break
        else:
            raise Exception(f"Option '{full_name}' not found in hidden select")
    time.sleep(1)
    # Manually trigger change event to load the table
    driver.execute_script("arguments[0].dispatchEvent(new Event('change', {bubbles: true}));", hidden_select)
    wait_for_spinner_to_disappear(driver)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr"))
    )
    time.sleep(0.5)

def wait_for_spinner_to_disappear(driver, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "globalSpinnerDiv"))
        )
    except:
        pass
    time.sleep(0.5)

def click_next_and_wait(driver):
    wait_for_spinner_to_disappear(driver)
    try:
        next_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'control-btn') and normalize-space()='>']")
        if not next_btn.is_enabled():
            return False
    except:
        try:
            next_btn = driver.find_element(By.XPATH, "//button[contains(text(), '>')]")
            if not next_btn.is_enabled():
                return False
        except:
            return False

    rows_before = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    first_row_text = rows_before[0].text if rows_before else ""

    for attempt in range(3):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
            time.sleep(0.3)
            next_btn.click()
            break
        except ElementClickInterceptedException:
            wait_for_spinner_to_disappear(driver)
            time.sleep(1)
    else:
        return False

    try:
        WebDriverWait(driver, 15).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "tbody tr")[0].text != first_row_text
        )
        return True
    except:
        try:
            next_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'control-btn') and normalize-space()='>']")
            return next_btn.is_enabled()
        except:
            return False

def extract_all_parts(driver):
    all_parts = []
    page_num = 1
    while True:
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:
                part_text = cells[1].text.strip()
                if part_text:
                    all_parts.append(part_text)
        print(f"      Page {page_num}: {len(rows)} parts")
        if not click_next_and_wait(driver):
            break
        page_num += 1
    return all_parts

def main():
    excel_path = "Book1.xlsx"
    if not os.path.exists(excel_path):
        print(f"Excel file not found: {excel_path}")
        return

    try:
        df = pd.read_excel(excel_path, sheet_name=0)
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return

    df.columns = df.columns.str.strip()
    required_cols = ["CONSTITUENCY NUMBER", "CONSTITUENCY NAME", "DISTRICT"]
    if not all(col in df.columns for col in required_cols):
        print(f"Excel columns missing. Expected: {required_cols}")
        return

    # Apply constituency name corrections
    df["CONSTITUENCY NAME"] = df.apply(
        lambda row: CONSTITUENCY_NAME_MAPPING.get(row["CONSTITUENCY NUMBER"], row["CONSTITUENCY NAME"]),
        axis=1
    )

    driver = setup_edge_driver()
    driver.get("https://voters.eci.gov.in/download-eroll")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "stateCode"))
    )
    time.sleep(2)

    # Set global filters
    select_dropdown_by_text(driver, "stateCode", "Uttar Pradesh")
    print("✓ State: Uttar Pradesh")
    select_dropdown_by_text(driver, "revyear", "2026")
    print("✓ Year: 2026")
    select_dropdown_by_text(driver, "roleType", "SIR FinalRoll - 2026")
    print("✓ Roll Type: SIR FinalRoll - 2026")

    # Extract live district names for mapping
    district_select = driver.find_element(By.NAME, "district")
    live_districts = [opt.text.strip() for opt in district_select.find_elements(By.TAG_NAME, "option") if opt.get_attribute("value")]

    def get_live_district(excel_district):
        mapped = DISTRICT_MAPPING.get(excel_district, excel_district)
        if mapped in live_districts:
            return mapped
        for live in live_districts:
            if live.lower() == mapped.lower():
                return live
        return None

    processed_count = 0
    skipped_count = 0

    for index, row in df.iterrows():
        const_number = int(row["CONSTITUENCY NUMBER"])
        const_name = row["CONSTITUENCY NAME"].strip().replace("<br>", "").strip()
        district_excel = row["DISTRICT"].strip()
        district_live = get_live_district(district_excel)

        safe_name = f"{const_number} - {const_name}".replace("/", "-").replace("\\", "-").replace(":", "-").replace("*", "").replace("?", "").replace('"', "'")
        filename = f"{safe_name}.csv"

        if os.path.exists(filename):
            print(f"\n⏭️ Skipping already processed: {const_number} - {const_name}")
            skipped_count += 1
            continue

        if not district_live:
            print(f"\n⚠️ District '{district_excel}' not found in live list. Skipping constituency {const_number} - {const_name}")
            continue

        print(f"\n{'='*60}")
        print(f"📂 District: {district_live} | Constituency: {const_number} - {const_name}")

        # Refresh page for a clean state
        driver.get("https://voters.eci.gov.in/download-eroll")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "stateCode"))
        )
        time.sleep(2)

        # Re-apply global filters
        select_dropdown_by_text(driver, "stateCode", "Uttar Pradesh")
        select_dropdown_by_text(driver, "revyear", "2026")
        select_dropdown_by_text(driver, "roleType", "SIR FinalRoll - 2026")

        # Select district
        try:
            select_dropdown_by_text(driver, "district", district_live, timeout=15)
            time.sleep(3)  # Ensure hidden select populates
        except Exception as e:
            print(f"   ⚠️ Failed to select district '{district_live}': {e}")
            continue

        # Select AC using hidden select (retry once)
        success = False
        for attempt in range(2):
            try:
                select_assembly_constituency(driver, const_number, const_name)
                success = True
                break
            except Exception as e:
                print(f"      Attempt {attempt+1} failed: {e}")
                time.sleep(3)
                # Re-select district to refresh the hidden select
                try:
                    select_dropdown_by_text(driver, "district", district_live, timeout=10)
                    time.sleep(2)
                except:
                    pass
        if not success:
            print("      ❌ Skipping due to repeated failures.")
            continue

        print("      ✅ Table loaded.")
        parts = extract_all_parts(driver)
        print(f"      Total parts extracted: {len(parts)}")

        if len(parts) == 0:
            print("      ⚠️ No parts found. CSV not saved.")
            continue

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Part No and Part Name"])
            for part in parts:
                writer.writerow([part])
        print(f"      💾 Saved to {filename}")
        processed_count += 1

        time.sleep(1)

    print(f"\n✅ Processing complete! Newly processed: {processed_count}, Skipped: {skipped_count}")
    driver.quit()

if __name__ == "__main__":
    main()
