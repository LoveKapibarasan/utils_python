from PIL import Image
import pytesseract
import sys
import os

# Optional: Set the path to tesseract executable if not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Linux
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows

def extract_text_from_image(image_path):
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
        return ""

    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error during OCR: {e}")
        return ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ocr_script.py <image_file>")
        sys.exit(1)

    image_file = sys.argv[1]
    extracted_text = extract_text_from_image(image_file)

    print("\n--- Extracted Text ---")
    print(extracted_text)

