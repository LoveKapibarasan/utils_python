import fitz

doc = fitz.open("input.pdf")
for page in doc:
    # Scale by 0.8 (80%)
    zoom = fitz.Matrix(0.8, 0.8)
    pix = page.get_pixmap(matrix=zoom)
    
    # Replace page with resized version
    page.clean_contents()
    page.insert_image(page.rect, pixmap=pix)

doc.save("resized.pdf")
