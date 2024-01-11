import pandas as pd
import matplotlib.pyplot as plt
import os
from reportlab.platypus import Image, SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import webbrowser

# Define paths for the input Excel file and output PDF file
excel_file_path = 'C:/Users/kyleh/OneDrive/Documents/YouTube/Bank-Insights-Pro-main/Bank-Insights-Pro-main/UBPR Example.xlsx'
pdf_file_path = 'Bank_Executive_Report.pdf'

# Load the data from the Excel file
try:
    ubpr_df = pd.read_excel(excel_file_path, sheet_name='Parsed UBPR Data')
except Exception as e:
    print("Error loading Excel file:", e)
    exit(1)

# Ensure 'Date' column is in the correct format and exists
if 'Date' not in ubpr_df.columns:
    print("Error: 'Date' column not found in the DataFrame.")
    exit(1)

ubpr_df['Date'] = pd.to_datetime(ubpr_df['Date'])

# Extract the bank's FDIC Certificate number (assumed to be in the first row of the first column)
fdic_certificate_number = ubpr_df.iloc[0, 0]

# Function to sanitize metric names for use in filenames and titles
def sanitize_name(name):
    return name.replace('/', '_').replace('\t', '_').replace('\\', '_').replace(' ', '_')

# Function to plot metrics and save figures in batches
def plot_metrics_in_batches(df, metrics, batch_size=20):
    os.makedirs('plots', exist_ok=True)  # Ensure the plots directory exists
    for i in range(0, len(metrics), batch_size):
        batch_metrics = metrics[i:i + batch_size]
        for metric in batch_metrics:
            sanitized_metric = sanitize_name(metric)
            save_path = f"plots/{fdic_certificate_number}_{sanitized_metric}.png"
            if metric not in df.columns:
                print(f"Metric not found: {metric}")
                continue
            plt.figure()
            df.plot(x='Date', y=metric, kind='line', title=sanitized_metric)
            plt.savefig(save_path)
            plt.close()
        print(f"Processed batch {i // batch_size + 1}")

plot_metrics_in_batches(ubpr_df, ubpr_df.columns[2:])  # Skipping 'FDIC Certificate #' and 'Date'

# Function to generate insights for a given metric
def generate_insight(metric):
    # Implement your analysis logic here
    return f"Insight for {metric}"

# PDF Report Generation
doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
styles = getSampleStyleSheet()
elements = []

# Add Cover Page
elements.append(Paragraph("Bank Executive Financial Report", styles['Title']))
elements.append(PageBreak())

# Add Disclaimer
disclaimer_text = "The executive bank report is a comprehensive analysis derived from the Uniform Bank Performance Report (UBPR), trended over time to provide a detailed view of a bank's performance. It meticulously compares a bank's key financial indicators with those of its peer groups, offering a clear perspective on where the bank stands in the competitive landscape. This report focuses exclusively on statistical observations based on UBPR data, without including any recommendations. Its purpose is to deliver a factual, data-driven understanding of a bank's financial health, growth, and stability, enabling informed assessments for stakeholders and industry analysts."
elements.append(Paragraph(disclaimer_text, styles['BodyText']))
elements.append(PageBreak())

# Add Table of Contents
elements.append(Paragraph("Table of Contents", styles['Heading1']))
# Add table of contents entries here
elements.append(PageBreak())

# Analysis Sections
for metric in ubpr_df.columns[2:]:  # Start from the third column to skip 'FDIC Certificate #' and 'Date'
    sanitized_metric = sanitize_name(metric)
    plot_path = f"plots/{fdic_certificate_number}_{sanitized_metric}.png"
    elements.append(Paragraph(f"{metric} Analysis", styles['Heading2']))
    elements.append(Spacer(1, 12))
    elements.append(Image(plot_path))
    elements.append(Spacer(1, 12))
    insight_text = generate_insight(metric)
    elements.append(Paragraph(insight_text, styles['BodyText']))
    elements.append(PageBreak())

# Build PDF
doc.build(elements)

# Function to open the PDF file after creation
def open_pdf(file_path):
    if os.path.exists(file_path):
        webbrowser.open(file_path)
    else:
        print("Error: File does not exist.")

# Open the PDF file
open_pdf(pdf_file_path)
