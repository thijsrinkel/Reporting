import streamlit as st
import fitz  # PyMuPDF for PDF handling
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(values, pdf_output_path):
    """Generate a PDF with filled details."""
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    
    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 800, "Survey Installation and Calibration Report")
    
    # Project Details
    c.setFont("Helvetica", 12)
    c.drawString(100, 780, f"Project Name: EPCI Energy Island for MOG2 Project")
    c.drawString(100, 760, f"Caisson Number: {values['caisson_number']}")
    c.drawString(100, 740, f"Date: {values['date']}")
    c.drawString(100, 720, f"Location: {values['location']}")
    c.drawString(100, 700, f"Operator: {values['operator']}")
    
    # Report Sections
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 670, "Scope of Document")
    c.setFont("Helvetica", 12)
    c.drawString(100, 650, "This document presents a summary of the survey operations, installations,")
    c.drawString(100, 635, "and calibrations acquired for Caisson XX as part of the EPCI Energy Island Project.")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 600, "Survey System Setup")
    c.setFont("Helvetica", 12)
    c.drawString(100, 580, "- Equipment installed on Caisson XX")
    c.drawString(100, 565, "- Software used during installation and calibrations")
    c.drawString(100, 550, "- Survey System Calibrations and Verifications")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 520, "Position Verifications")
    c.setFont("Helvetica", 12)
    c.drawString(100, 500, "After installation and calibration, a position verification was performed to")
    c.drawString(100, 485, "ensure correct functionality and accuracy of the CCSC Survey Systems.")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 450, "CCSC Survey Systems Health Check")
    c.setFont("Helvetica", 12)
    c.drawString(100, 430, "A system integrity check was performed to validate correct DGNSS antenna offsets.")
    
    c.save()
    
    with open(pdf_output_path, "wb") as f:
        f.write(pdf_buffer.getvalue())
    return pdf_output_path

def merge_pdfs(main_pdf, annex_pdfs, output_pdf):
    """Merge the main report PDF with annex PDFs."""
    merger = fitz.open()
    merger.insert_pdf(fitz.open(main_pdf))
    for annex in annex_pdfs:
        merger.insert_pdf(fitz.open(annex))
    merger.save(output_pdf)
    merger.close()
    return output_pdf

# Streamlit UI
st.title("Caisson Report Generator")
st.write("Fill in the details and upload annexes to generate the final report.")

# Dynamic form fields
st.sidebar.header("Enter Report Details")
values = {
    "caisson_number": st.sidebar.text_input("Caisson Number"),
    "date": st.sidebar.text_input("Date"),
    "location": st.sidebar.text_input("Location"),
    "operator": st.sidebar.text_input("Operator"),
}

# Upload annex PDFs
annex_files = st.file_uploader("Upload Annex PDFs", type=["pdf"], accept_multiple_files=True)

# Generate button
if st.button("Generate Report"):
    pdf_report = "final_report.pdf"
    generate_pdf(values, pdf_report)
    
    annex_paths = []
    for annex in annex_files:
        annex_path = f"annex_{annex.name}"
        with open(annex_path, "wb") as f:
            f.write(annex.read())
        annex_paths.append(annex_path)
    
    final_pdf = "complete_report.pdf"
    merge_pdfs(pdf_report, annex_paths, final_pdf)
    
    st.success("Report Generated Successfully!")
    with open(final_pdf, "rb") as f:
        st.download_button("Download Final Report", f, file_name="Caisson_Report.pdf")
