import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shutil import move  # Import move from shutil

# Path to your chromedriver executable
driver_path = r'C:/Users/klhughes/AppData/Local/Programs/Python/Python312/Practice Python/Bank UBPR/ChromeDriver/chromedriver.exe'
downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')  # Default Downloads directory
target_dir = r'C:/Users/klhughes/AppData/Local/Programs/Python/Python312/Practice Python/Bank UBPR'

# Set up Chrome options to specify the download directory
chrome_options = Options()
prefs = {"download.default_directory": downloads_dir}  # Use downloads_dir here
chrome_options.add_experimental_option("prefs", prefs)

# Initialize the webdriver with the specified options
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Open the website
driver.get('https://cdr.ffiec.gov/public/ManageFacsimiles.aspx')

# Get FDIC Certificate Number from user
fdic_cert_number = input("Enter the bank's FDIC Certificate Number: ")

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

# Function to rename and move the downloaded file
def rename_and_move_file(file_path, target_directory):
    filename = os.path.basename(file_path)
    new_filename = os.path.splitext(filename)[0] + '.txt'
    new_file_path = os.path.join(target_directory, new_filename)
    move(file_path, new_file_path)
    return new_file_path

# Wait for the download to complete
time.sleep(40) 

# Get the most recently downloaded file
downloaded_file = get_latest_downloaded_file(downloads_dir)

# Check if a file was downloaded and then process it
if downloaded_file:
    # Rename and move the file
    new_file_path = rename_and_move_file(downloaded_file, target_dir)
    os.startfile(new_file_path)  # Open the file with the default application
else:
    print("No file was downloaded.")

driver.quit()
