import fitz

doc = fitz.open('Salon Frenyz(April).pdf')
text = ""
for page in doc:
    text += page.get_text()

with open('pdf_content_pymupdf.txt', 'w') as f:
    f.write(text)
