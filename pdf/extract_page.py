import sys
import fitz  # PyMuPDF

def main():
    if len(sys.argv) != 5:
        print("Usage: python pdf_extract_range_fitz.py input.pdf start_page end_page output.pdf", file=sys.stderr)
        sys.exit(1)

    input_path, start_str, end_str, output_path = sys.argv[1:5]

    try:
        start = int(start_str)
        end = int(end_str)
    except ValueError:
        print("start_page and end_page must be integers (1-based).", file=sys.stderr)
        sys.exit(2)

    if start < 1 or end < 1 or end < start:
        print("Invalid range: ensure 1 <= start_page <= end_page.", file=sys.stderr)
        sys.exit(3)

    try:
        src = fitz.open(input_path)
    except Exception as e:
        print(f"Failed to open input PDF: {e}", file=sys.stderr)
        sys.exit(4)

    num_pages = len(src)
    if end > num_pages:
        print(f"end_page ({end}) exceeds document length ({num_pages} pages).", file=sys.stderr)
        src.close()
        sys.exit(5)

    out = fitz.open()
    # convert to 0-based inclusive indices
    out.insert_pdf(src, from_page=start - 1, to_page=end - 1)

    try:
        out.save(output_path)
    except Exception as e:
        print(f"Failed to save output PDF: {e}", file=sys.stderr)
        out.close()
        src.close()
        sys.exit(6)

    out.close()
    src.close()
    print(f"Extracted pages {start}-{end} of {num_pages} to: {output_path}")

if __name__ == "__main__":
    main()