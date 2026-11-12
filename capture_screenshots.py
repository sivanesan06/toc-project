"""
capture_screenshots.py
Automated screenshot capture tool using Selenium and Headless Chrome.
Captures all nine required application views directly from the running Streamlit app.
"""

import os
import sys
import time
import subprocess
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_for_server(url: str = "http://localhost:8501", timeout_sec: int = 20) -> bool:
    """Polls the server until it responds with HTTP 200."""
    start_time = time.time()
    while time.time() - start_time < timeout_sec:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def capture_all_views():
    screenshot_dir = os.path.abspath("outputs/screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)

    # 1. Start Streamlit in Background
    python_exe = sys.executable
    cmd = [
        python_exe, "-m", "streamlit", "run", "app.py",
        "--server.headless", "true",
        "--server.port", "8501",
        "--browser.gatherUsageStats", "false"
    ]
    print("Starting Streamlit application...")
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        if not wait_for_server("http://localhost:8501"):
            print("ERROR: Streamlit server failed to start within timeout.")
            return

        print("Streamlit is online. Initializing Headless Chrome...")

        # 2. Configure Selenium Headless Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1440,1050")

        # Chrome path if standard
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if os.path.exists(chrome_path):
            chrome_options.binary_location = chrome_path

        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1440, 1050)

        wait = WebDriverWait(driver, 15)

        # Helper to click a sidebar radio option
        def select_sidebar_nav(label_contains: str):
            driver.get("http://localhost:8501")
            time.sleep(2.5)
            # Find radio button labels in sidebar
            labels = driver.find_elements(By.CSS_SELECTOR, "section[data-testid='stSidebar'] label")
            for lbl in labels:
                if label_contains in lbl.text:
                    driver.execute_script("arguments[0].click();", lbl)
                    time.sleep(2.5)
                    return True
            return False

        # 1. Homepage / Dashboard
        print("Capturing 01_homepage.png...")
        driver.get("http://localhost:8501")
        time.sleep(3)
        driver.save_screenshot(os.path.join(screenshot_dir, "01_homepage.png"))

        # 2. Document Upload & Preview
        print("Capturing 02_document_upload.png...")
        select_sidebar_nav("2. 📁 Document Upload")
        driver.save_screenshot(os.path.join(screenshot_dir, "02_document_upload.png"))

        # 3. Five-Pattern Search Results
        print("Capturing 03_five_pattern_search.png...")
        select_sidebar_nav("3. 🔍 Regular Expression")
        driver.save_screenshot(os.path.join(screenshot_dir, "03_five_pattern_search.png"))

        # 4. Occurrence Statistics (Select Pattern 1)
        print("Capturing 04_occurrence_statistics.png...")
        select_sidebar_nav("3. 🔍 Regular Expression")
        # Find dropdown
        try:
            selectboxes = driver.find_elements(By.CSS_SELECTOR, "div[data-baseweb='select']")
            if selectboxes:
                driver.execute_script("arguments[0].click();", selectboxes[0])
                time.sleep(1)
                options = driver.find_elements(By.CSS_SELECTOR, "li[role='option']")
                for opt in options:
                    if "Pattern 1" in opt.text:
                        driver.execute_script("arguments[0].click();", opt)
                        time.sleep(2)
                        break
        except Exception as e:
            print("Dropdown select notice:", e)
        driver.save_screenshot(os.path.join(screenshot_dir, "04_occurrence_statistics.png"))

        # 5. DFA State Transition Diagram
        print("Capturing 05_dfa_transition_diagram.png...")
        select_sidebar_nav("4. ⚙️ DFA Design")
        driver.save_screenshot(os.path.join(screenshot_dir, "05_dfa_transition_diagram.png"))

        # 6. DFA Transition Table (Tab 2)
        print("Capturing 06_dfa_transition_table.png...")
        select_sidebar_nav("4. ⚙️ DFA Design")
        tabs = driver.find_elements(By.CSS_SELECTOR, "button[data-baseweb='tab']")
        if len(tabs) >= 2:
            driver.execute_script("arguments[0].click();", tabs[1])
            time.sleep(1.5)
        driver.save_screenshot(os.path.join(screenshot_dir, "06_dfa_transition_table.png"))

        # 7. DFA Simulation Results (Tab 3)
        print("Capturing 07_dfa_simulation_results.png...")
        select_sidebar_nav("4. ⚙️ DFA Design")
        tabs = driver.find_elements(By.CSS_SELECTOR, "button[data-baseweb='tab']")
        if len(tabs) >= 3:
            driver.execute_script("arguments[0].click();", tabs[2])
            time.sleep(1.5)
        driver.save_screenshot(os.path.join(screenshot_dir, "07_dfa_simulation_results.png"))

        # 8. RE vs DFA Execution Comparison
        print("Capturing 08_re_vs_dfa_comparison.png...")
        select_sidebar_nav("5. ⚖️ RE vs DFA")
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "08_re_vs_dfa_comparison.png"))

        # 9. Test Cases & Observations
        print("Capturing 09_test_cases_and_observations.png...")
        select_sidebar_nav("6. 🧪 Test Cases")
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "09_test_cases_and_observations.png"))

        print("All screenshots successfully captured!")
        driver.quit()

    finally:
        print("Terminating Streamlit server...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    capture_all_views()

