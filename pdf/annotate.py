import fitz  # PyMuPDF

pdf_path = "input.pdf"
doc = fitz.open(pdf_path)

# Example: highlight text on page 0
page = doc[0]
text = "important keyword"
text_instances = page.search_for(text)

for inst in text_instances:
    highlight = page.add_highlight_annot(inst)
    highlight.update()

# Example: add sticky note
page.add_text_annot((100, 150), "This is a note")

doc.save("annotated.pdf")
