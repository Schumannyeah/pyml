import fitz  # PyMuPDF
import pytesseract
import pandas as pd
import tabula
import io
from PIL import Image
import pyodbc


# Ensure pytesseract knows where Tesseract is located, if necessary
# pytesseract.pytesseract.tesseract_cmd = '/path/to/tesseract'

# Function to extract text from PDF using both PyMuPDF and OCR
def extract_text_from_pdf_with_ocr(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    # First, try extracting text normally
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()

    # If text is not as expected, fallback to OCR
    if "K2" not in text:  # Replace "expected_keyword" with something you expect to find
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))  # Convert page to 300 dpi image
            img_bytes = pix.tobytes("ppm")  # Convert pixmap to bytes

            # Convert bytes to PIL Image and perform OCR
            img = Image.open(io.BytesIO(img_bytes))
            ocr_text = pytesseract.image_to_string(img)
            text += ocr_text

    return text


# Function to extract tables remains unchanged
def extract_tables_from_pdf(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    return tables


# Usage
pdf_path = '../dataset/123.pdf'
text_data = extract_text_from_pdf_with_ocr(pdf_path)
print(text_data)