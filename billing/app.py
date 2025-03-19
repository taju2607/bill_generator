import os
from datetime import datetime
from reportlab.pdfgen import canvas
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Create today's folder and return the folder path
def create_today_folder():
    today_date = datetime.now().strftime("%d-%m-%Y")
    if not os.path.exists(today_date):
        os.makedirs(today_date)
    return today_date

# Create individual PDFs for the phone numbers and return the PDF paths
def create_pdfs(today_date, phone_numbers_data):
    pdf_paths = []
    for i, data in enumerate(phone_numbers_data, start=1):
        phone_number = data['Number']
        pdf_name = f"{i:03d}-{phone_number}.pdf"  # Format: 001-1234567890.pdf
        pdf_path = os.path.join(today_date, pdf_name)
        
        # Create a simple PDF
        c = canvas.Canvas(pdf_path)
        c.drawString(100, 750, f"Serial Number: {i:03d}")
        c.drawString(100, 730, f"Phone Number: {phone_number}")
        c.drawString(100, 710, f"Cost: {data['Cost']}")
        c.drawString(100, 690, f"Cash: {data['Cash']}")
        c.drawString(100, 670, f"UPI: {data['UPI']}")
        c.drawString(100, 650, f"Cart: {data['Cart']}")
        c.drawString(100, 630, f"Generated on: {today_date}")
        c.save()
        pdf_paths.append(pdf_path)
    return pdf_paths

# Create a summary PDF in the main directory
def create_summary_pdf(today_date, phone_numbers_data):
    summary_pdf_path = os.path.join(os.getcwd(), "PhoneNumbersSummary.pdf")
    c = canvas.Canvas(summary_pdf_path)
    c.drawString(100, 800, f"Summary Generated on: {today_date}")
    c.drawString(100, 780, "Phone Numbers:")
    
    y_position = 760
    for i, data in enumerate(phone_numbers_data, start=1):
        c.drawString(100, y_position, f"{i:03d}. {data['Number']}")
        y_position -= 20
        if y_position < 50:  # Handle page overflow
            c.showPage()
            y_position = 800
    c.save()
    return summary_pdf_path

# Update the Excel sheet with the new phone number data
def update_excel(phone_numbers_data):
    excel_file = "PhoneNumbersLog.xlsx"
    headers = ["S.no", "Number", "Cost", "Date", "Time", "Cash", "UPI", "Cart"]
    
    # Check if Excel file exists
    if os.path.exists(excel_file):
        df_existing = pd.read_excel(excel_file)
        last_serial = int(df_existing["S.no"].iloc[-1]) if not df_existing.empty else 0
    else:
        df_existing = pd.DataFrame(columns=headers)
        last_serial = 0
    
    # Create new data
    new_data = []
    today_date = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%H:%M:%S")
    
    for i, data in enumerate(phone_numbers_data, start=1):
        new_data.append({
            "S.no": last_serial + i,
            "Number": data["Number"],
            "Cost": data["Cost"],
            "Date": today_date,
            "Time": current_time,
            "Cash": data["Cash"],
            "UPI": data["UPI"],
            "Cart": data["Cart"],
        })
    
    # Add new data to the existing DataFrame
    df_new = pd.DataFrame(new_data)
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_excel(excel_file, index=False)
    return "Excel sheet updated."

# Flask route to handle PDF creation and Excel update
@app.route('/add_phone_numbers', methods=['POST'])
def add_phone_numbers():
    phone_numbers_data = request.json.get("phone_numbers")
    
    if not phone_numbers_data:
        return jsonify({"error": "No phone numbers provided."}), 400
    
    today_date = create_today_folder()
    
    # Create PDFs for each phone number
    pdf_paths = create_pdfs(today_date, phone_numbers_data)
    
    # Create a summary PDF
    summary_pdf_path = create_summary_pdf(today_date, phone_numbers_data)
    
    # Update the Excel sheet with phone numbers
    excel_message = update_excel(phone_numbers_data)
    
    return jsonify({
        "message": "Phone numbers processed successfully.",
        "pdf_paths": pdf_paths,
        "summary_pdf_path": summary_pdf_path,
        "excel_message": excel_message
    }), 200

if __name__ == "__main__":
    app.run(debug=False)
