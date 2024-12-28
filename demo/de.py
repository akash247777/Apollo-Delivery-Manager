from flask import Flask, render_template, request
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
document_count = 0

# Load site details from Excel file
def load_site_details():
    file_path = "data.xlsx"  # Replace with the correct path to your Excel file
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        raise FileNotFoundError("Site details Excel file not found.")

site_data = load_site_details()

@app.route('/')
def index():
    return render_template('index.html')  # A form for entering the site number

@app.route('/generate', methods=['POST'])
def generate_challan():
    global document_count
    document_count += 1

    # Get site number from the form
    site_number = request.form.get("site")
    if not site_number:
        return "No site number provided. Please try again.", 400

    # Filter site details based on site number
    site_details = site_data[site_data["Site"].astype(str) == site_number]
    if site_details.empty:
        return f"Site with number {site_number} not found. Please check and try again.", 400

    # Extract site details
    site_details = site_details.iloc[0]
    address = site_details["Address"]
    contact = site_details["Contact No"]
    site_name = site_details["Site Name"]

    # Get current date and DC number
    current_date = datetime.now().strftime("%d-%m-%Y")
    dc_no = document_count

    # Render the challan template
    return render_template(
        'challan.html',
        Site=site_number,
        address=address,
        contact=contact,
        Site_name=site_name,
        current_date=current_date,
        dc_no=dc_no
    )

if __name__ == '__main__':
    app.run(debug=True)
