import pandas as pd
from openpyxl import load_workbook
import re

def parse_ubpr_report(report_path):
    with open(report_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data_collection = []
    dates = []

    # Adjusted regular expressions to be more specific and stringent
    date_pattern = re.compile(r"(\d{2}/\d{2}/\d{4})")
    data_pattern = re.compile(r'^(?P<metric>[A-Za-z\s]+)(?P<values>(\s*\d+\.*\d*\s*){15})$')

    date_line_index = None
    for i, line in enumerate(lines):
        if "Earnings and Profitability" in line:
            date_line_index = i - 1
            break

    if date_line_index is not None and date_line_index < len(lines):
        line = lines[date_line_index]
        dates = date_pattern.findall(line)
        dates = sorted(set(dates), key=lambda x: pd.to_datetime(x, format='%m/%d/%Y'))

    for line in lines:
        data_match = data_pattern.search(line)
        if data_match and dates:
            metric = data_match.group('metric').strip()
            values = data_match.group('values').split()

            if len(values) != len(dates) * 3:
                print(f"Warning: Data points for metric {metric} do not align with the dates. Expected {len(dates) * 3}, found {len(values)}.")
                continue  # Skip this line as it doesn't match the expected structure

            for i in range(len(dates)):
                try:
                    index = i * 3
                    data_point = {
                        'FDIC Certificate #': '4239',
                        'Date': dates[i],
                        f"{metric} BANK": values[index],
                        f"{metric} PG2": values[index + 1],
                        f"{metric} PCT": values[index + 2]
                    }
                    data_collection.append(data_point)
                except IndexError:
                    print(f"Error processing data for {metric} on {dates[i]}. Expected index {index} not found in values.")

    return pd.DataFrame(data_collection)

def add_sheet_to_excel(df, file_path, sheet_name):
    """Adds a new sheet to an existing Excel file with the given DataFrame."""
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer: 
        df.to_excel(writer, sheet_name=sheet_name)

def main():
    report_path = 'C:/Users/klhughes/AppData/Local/Programs/Python/Python312/Practice Python/Bank UBPR/UBPR Report.txt'
    excel_file_path = 'C:/Users/klhughes/AppData/Local/Programs/Python/Python312/Practice Python/Bank UBPR/UBPR Example.xlsx'
    
    new_data_df = parse_ubpr_report(report_path)
    print("Data extracted to DataFrame:")
    print(new_data_df)
    
    if not new_data_df.empty:
        add_sheet_to_excel(new_data_df, excel_file_path, sheet_name='Parsed UBPR Data')
        print(f"Attempted to add new sheet to {excel_file_path}")
    else:
        print("No data to write to Excel.")

if __name__ == "__main__":
    main()
