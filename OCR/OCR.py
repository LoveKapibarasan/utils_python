from PIL import Image
import pytesseract
import sys
import os
from pdf2image import convert_from_path  # Add missing import

# Optional: Set the path to tesseract executable if not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Linux
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows




def extract_text_from_image(image_path, lang):
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
        return ""

    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang=lang)  # Add lang parameter
        return text
    except Exception as e:
        print(f"Error during OCR: {e}")
        return ""

def to_pdf(pdf_path, lang):  # Add missing function
    text = ""
    images = convert_from_path(pdf_path)
    for i, img in enumerate(images):
        page_text = pytesseract.image_to_string(img, lang=lang)
        text += page_text
        print(f"Page {i+1}:\n{page_text}")
    return text

if __name__ == "__main__":
    folder_path = input("Enter the folder path to the image file: ")
    
    lang = input("Enter the language (e.g., eng, jpn, deu, jpn+eng+deu): ").strip()  # Fix incomplete input
    if not lang:
        lang = "eng"  # Default to English if no input
        print("No language specified, defaulting to English (eng)")
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder path does not exist: {folder_path}")
        sys.exit(1)

    order = input("Enter the order of files (n: 1,2,3, l:lexicographical): ").strip().split(',')
    text = ""  # Initialize text variable

    # Sort files based on order preference
    files = os.listdir(folder_path)
    print(f"Found {len(files)} files in directory:")
    for file in files:
        print(f"  - {file}")

    # Filter for supported files
    supported_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.pdf'))]
    print(f"\nSupported files found: {len(supported_files)}")
    for file in supported_files:
        print(f"  - {file}")

    if not supported_files:
        print("No supported image or PDF files found!")
        sys.exit(1)

    if order[0].lower() == 'n':
        supported_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else 0)  # Sort supported_files instead of files
    else:  # lexicographical
        supported_files.sort()

    for file_name in supported_files:  # Use supported_files instead of files
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            print(f"Processing {file_name}...")
            file_path = os.path.join(folder_path, file_name)
            extracted_text = extract_text_from_image(file_path, lang)
            text += extracted_text
            if extracted_text:
                print(f"Extracted text from {file_name}:\n{extracted_text}\n")
            else:
                print(f"No text found in {file_name} or an error occurred.")
        elif file_name.lower().endswith('.pdf'):
            print(f"Processing PDF {file_name}...")
            confirm = input(f"Press Y to continue this pdf {file_name}...")
            if confirm.lower() != 'y':
                continue
            pdf_path = os.path.join(folder_path, file_name)
            extracted_text = to_pdf(pdf_path, lang)
            text += extracted_text
    
    # Print final combined text
    if text:
        with open("extracted_text.txt", "w", encoding="utf-8") as output_file:
            output_file.write(text)
        print("Text extracted from all files and saved to 'extracted_text.txt'.")
    else:
        print("No text extracted from any files.")