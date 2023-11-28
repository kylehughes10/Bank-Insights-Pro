import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

# Path to your chromedriver executable
driver_path = r'C:/Users/klhughes/AppData/Local/Programs/Python/Python312/Practice Python/Bank UBPR/ChromeDriver/chromedriver.exe'
downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')  # Default Downloads directory

# Set up Chrome options to specify the download directory
chrome_options = Options()
prefs = {"download.default_directory": downloads_dir}  # Use downloads_dir here
chrome_options.add_experimental_option("prefs", prefs)

# Initialize the webdriver with the specified options
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Open the website
driver.get('https://cdr.ffiec.gov/public/ManageFacsimiles.aspx')

# Check if the FDIC Certificate Number is passed as a command-line argument
if len(sys.argv) < 2:
    print("FDIC Certificate Number not provided as a command-line argument.")
    sys.exit(1)  # Exit if no argument is provided

# The FDIC Certificate Number is the first argument passed to the script
fdic_cert_number = sys.argv[1]


# Select the report type (Uniform Bank Performance Report)
report_type_dropdown = wait.until(EC.presence_of_element_located((By.ID, 'reportTypeDropDownList')))
report_type_dropdown.send_keys('Uniform Bank Performance Report')

# Select the identifier type (FDIC Certificate Number)
identifier_type_dropdown = wait.until(EC.presence_of_element_located((By.ID, 'selectAsrUbprUniqueIdentifierType')))
identifier_type_dropdown.send_keys('FDIC Certificate Number')

# Enter the FDIC Certificate Number
fdic_cert_input = wait.until(EC.presence_of_element_located((By.ID, 'txtUbprEsrUniqueIdentifier')))
fdic_cert_input.send_keys(fdic_cert_number)

# Click the 'Generate' button
generate_button = wait.until(EC.element_to_be_clickable((By.ID, 'btnGenerateByIdentifierEsrUbpr')))
generate_button.click()

# Ensure the standard radio button is selected
standard_radio_button = wait.until(EC.element_to_be_clickable((By.ID, 'RFStandard')))
standard_radio_button.click()

# Click the 'Generate Report' button
generate_report_button = wait.until(EC.element_to_be_clickable((By.ID, 'btnGenerateReportSrf')))
generate_report_button.click()

# Handle the popup window
original_window = driver.current_window_handle
# Wait for the new window or tab
wait.until(EC.number_of_windows_to_be(2))

# Loop through until we find a new window handle
for window_handle in driver.window_handles:
    if window_handle != original_window:
        driver.switch_to.window(window_handle)
        break

# Check the 'all pages' checkbox
all_pages_checkbox = wait.until(EC.element_to_be_clickable((By.ID, 'tc-chk-all')))
all_pages_checkbox.click()

# Click the 'Download' button
download_button = wait.until(EC.element_to_be_clickable((By.ID, 'btnDownloadReport')))
download_button.click()

# Rename and move the downloaded file
time.sleep(35) 

# Path to the directory where downloads are saved
download_dir = r'C:/Users/klhughes/AppData/Local/Programs/Python/Python312/Practice Python/Bank UBPR'

# Function to find the latest downloaded file
def get_latest_downloaded_file(directory):
    files = sorted(
        [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')],
        key=lambda x: os.path.getmtime(x),
        reverse=True
    )
    return files[0] if files else None

# Wait for the download to complete
time.sleep(40) 

# Get the most recently downloaded file
downloaded_file = get_latest_downloaded_file(downloads_dir)

driver.quit()
