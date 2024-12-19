import pytesseract
from PIL import Image


def extract_text_from_image(image_path):
    """
    Extract text from an image using Tesseract OCR.

    Args:
        image_path (str): Path to the input image file

    Returns:
        str: Extracted text from the image
    """
    try:
        # Open the image
        image = Image.open(image_path)

        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(image)

        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None
