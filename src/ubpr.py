import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # Added import for WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options to specify the download directory
chrome_options = Options()
prefs = {"download.default_directory": os.path.join(os.path.expanduser('~'), 'Downloads')}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize the webdriver with the specified options
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

# Open the website
driver.get('https://cdr.ffiec.gov/public/ManageFacsimiles.aspx')

# Accept input from stdin for the CERT numbers
fdic_cert_numbers = input().strip().split(' ')

for fdic_cert_number in fdic_cert_numbers:
    # Select the report type (Uniform Bank Performance Report)
    report_type_dropdown = wait.until(EC.presence_of_element_located((By.ID, 'reportTypeDropDownList')))
    report_type_dropdown.send_keys('Uniform Bank Performance Report')

    # Select the identifier type (FDIC Certificate Number)
    identifier_type_dropdown = wait.until(EC.presence_of_element_located((By.ID, 'selectAsrUbprUniqueIdentifierType')))
    identifier_type_dropdown.send_keys('FDIC Certificate Number')

    # Enter the FDIC Certificate Numbers
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

    # Wait for the download to complete and rename/move as needed
    time.sleep(35)  # Sleep times may need adjustment depending on download speed

    # Make sure to clear the CERT input for the next number
    fdic_cert_input.clear()

driver.quit()
