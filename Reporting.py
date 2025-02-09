import streamlit as st
import fitz  # PyMuPDF for PDF handling
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(values, pdf_output_path):
    """Generate a PDF with filled details."""
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    c.drawString(100, 800, "Caisson Report")
    c.drawString(100, 780, f"Date: {values['date']}")
    c.drawString(100, 760, f"Location: {values['location']}")
    c.drawString(100, 740, f"Operator: {values['operator']}")
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

# Dynamic form fields (Example fields)
st.sidebar.header("Enter Report Details")
values = {
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
