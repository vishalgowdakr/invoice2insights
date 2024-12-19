import pdfplumber


def extract_text_from_pdf(pdf_path):
    """
    Extract all text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str: Extracted text from the PDF
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Extract text from each page and concatenate
            full_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n\n"  # Add newlines between pages

            return full_text.strip()

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""
