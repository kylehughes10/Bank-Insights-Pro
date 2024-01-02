import pandas as pd
import re

# Define patterns for parsing
FDIC_CERT_PATTERN = r'FDIC Certificate # (\d+)'
DATE_PATTERN = r'\b\d{2}/\d{2}/\d{4}\b'
PEER_GROUP_PATTERN = r'The current peer group for this bank is: (\d+)'
METRIC_PATTERN_REFINED = r'\n\s+(.*?)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+)\s+'

def read_ubpr_report(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def extract_fdic_cert(report_content):
    # Extract the FDIC Certification number using a regular expression
    match = re.search(FDIC_CERT_PATTERN, report_content)
    return match.group(1) if match else None

def extract_dates(report_content):
    # Extract all dates from the report
    return re.findall(DATE_PATTERN, report_content)

def extract_peer_group(report_content):
    # Extract the peer group
    match = re.search(PEER_GROUP_PATTERN, report_content, re.MULTILINE)
    return match.group(1) if match else None

def extract_metrics_refined(report_section):
    # Extract metrics, values, peer group values, and percentiles
    metrics = re.findall(METRIC_PATTERN_REFINED, report_section)
    structured_metrics = []
    for metric in metrics:
        name, bank_value, peer_group_value, percentile = metric
        structured_metrics.append({
            'Metric': name.strip(),
            'Bank Value': bank_value,
            'Peer Group Value': peer_group_value,
            'Percentile': percentile
        })
    return structured_metrics

def structure_data_refined(fdic_cert, dates, peer_group, metrics):
    # Create a dictionary to hold the structured data for the most recent date
    data = {
        'FDIC Certification #': fdic_cert,
        'Date': dates[3],  # Assuming the 4th date is the most recent based on the pattern observed
        'Peer Group': peer_group
    }
    # Add metrics to the data dictionary
    for metric in metrics:
        data[f'{metric["Metric"]}'] = metric['Bank Value']
        data[f'{metric["Metric"]} PG {peer_group}'] = metric['Peer Group Value']
        data[f'{metric["Metric"]} PCT'] = metric['Percentile']
    # Convert the dictionary to a DataFrame
    return pd.DataFrame([data])

def write_to_excel(data, excel_path):
    # Load the existing Excel file
    with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a') as writer:
        # Write the structured data to a new sheet
        data.to_excel(writer, sheet_name='Structured UBPR Data', index=False)

# Main process
if __name__ == "__main__":
    ubpr_report_path = "C:/Users/kyleh/OneDrive/Documents/YouTube/UBPR/ubpr-report-generator/public/UBPR Report.txt"
    excel_path = "C:/Users/kyleh/OneDrive/Documents/YouTube/UBPR/ubpr-report-generator/public/UBPR Example.xlsx"

    report_content = read_ubpr_report(ubpr_report_path)
    fdic_cert = extract_fdic_cert(report_content)
    dates = extract_dates(report_content)
    peer_group = extract_peer_group(report_content)
    metrics = extract_metrics_refined(report_content)
    structured_data = structure_data_refined(fdic_cert, dates, peer_group, metrics)
    write_to_excel(structured_data, excel_path)