# Logic:
# 1. Extract Data from PDF:
# Use a Python library like PyMuPDF, PyPDF2, or pdfplumber to extract text from the PDF.
# For extracting tables, you can use tabula-py or camelot-py.
# For images and figures, you can use PyMuPDF or pdf2image.
#
# 2. Process Extracted Data:
# Process the extracted text to identify the required information.
# If there are tables, convert them into a suitable format (e.g., DataFrame using pandas).
# For images, save them to disk and store the file paths in the database.
#
# 3. Store Data in MSSQL:
# Use pyodbc or SQLAlchemy to connect to your MSSQL database.
# Create the necessary tables if they don't exist.
# Insert the extracted and processed data into the MSSQL tables.

import fitz  # PyMuPDF
import pandas as pd
import tabula
import pyodbc

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Function to extract tables from PDF
def extract_tables_from_pdf(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    return tables

# Example usage
pdf_path = '../dataset/123.pdf'
text_data = extract_text_from_pdf(pdf_path)
# Print extracted text and tables
print(text_data)

# tables_data = extract_tables_from_pdf(pdf_path)
# for table in tables_data:
#     print(table)