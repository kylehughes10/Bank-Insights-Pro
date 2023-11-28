from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import glob

app = Flask(__name__)

# Define the directory where the reports will be saved
REPORTS_DIR = r'C:/Users/klhughes/AppData/Local/Programs/Python/Python312/Practice Python/Bank UBPR'

@app.route('/run-ubpr', methods=['POST'])
def run_ubpr():
    fdic_cert_number = request.form['fdicCertNumber']
    process = subprocess.Popen(['python', 'ubpr.py', fdic_cert_number], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        return jsonify({'error': 'Python script failed', 'details': stderr.decode()}), 500

    # Find the most recent file in REPORTS_DIR matching the pattern
    files = glob.glob(os.path.join(REPORTS_DIR, 'CDR-UBPR_RT1_*_*.txt'))
    if not files:
        return jsonify({'error': 'No files found in directory'}), 404

    # Get the most recent file
    latest_file = max(files, key=os.path.getmtime)
    print(f"Most recent file: {latest_file}")  # Debug print

    # Read the content of the most recent file
    try:
        with open(latest_file, 'r') as file:
            file_content = file.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        return jsonify({'error': 'Could not read the file'}), 500

    return jsonify({'content': file_content})

@app.route('/reports/<filename>')
def download_report(filename):
    filename = filename.replace("..", "").replace("/", "\\")
    return send_from_directory(REPORTS_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)