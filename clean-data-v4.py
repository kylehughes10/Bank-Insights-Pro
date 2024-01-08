import pandas as pd
import re

def parse_ubpr_report(report_path):
    with open(report_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data_dict = {}
    date_pattern = re.compile(r"(\d{2}/\d{2}/\d{4})")

    # Updated regex to be more flexible and inclusive
    data_pattern = re.compile(r'^(?P<metric>[A-Za-z\s&\.\-\(\)]+)((\s*\-?\d+\.*\d*\s*)+)$')

    date_line_index = None
    for i, line in enumerate(lines):
        if "Earnings and Profitability" in line:
            date_line_index = i - 1
            break

    if date_line_index is not None and date_line_index < len(lines):
        line = lines[date_line_index]
        dates = date_pattern.findall(line)
        dates = sorted(set(dates), key=lambda x: pd.to_datetime(x, format='%m/%d/%Y'))

        for date in dates:
            data_dict[date] = {'FDIC Certificate #': '4239', 'Date': date}

    for line in lines:
        data_match = data_pattern.search(line)
        if data_match and dates:
            metric = data_match.group('metric').strip()
            values = data_match.group(2).split()

            num_dates = len(dates)
            num_values = len(values)
            expected_values = num_dates * 3

            if num_values < expected_values:
                print(f"Warning: Data points for metric '{metric}' are fewer than expected.")
                continue

            for i in range(num_dates):
                index = i * 3
                data_dict[dates[i]][f"{metric} BANK"] = values[index] if index < num_values else None
                data_dict[dates[i]][f"{metric} PG2"] = values[index + 1] if index + 1 < num_values else None
                data_dict[dates[i]][f"{metric} PCT"] = values[index + 2] if index + 2 < num_values else None

    return pd.DataFrame(list(data_dict.values()))

def add_sheet_to_excel(df, file_path, sheet_name):
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer: 
        df.to_excel(writer, sheet_name=sheet_name, index=False)

# Path to the provided text file
report_path = 'C:/Users/klhughes/AppData/Local/Programs/Python/Python312/Practice Python/Bank UBPR/UBPR Report.txt'
excel_file_path = 'C:/Users/klhughes/AppData/Local/Programs/Python/Python312/Practice Python/Bank UBPR/UBPR Example.xlsx'

# Parse the report and add data to Excel
new_data_df = parse_ubpr_report(report_path)
if not new_data_df.empty:
    add_sheet_to_excel(new_data_df, excel_file_path, sheet_name='Parsed UBPR Data')

new_data_df.head()  # Displaying a snippet of the parsed data

