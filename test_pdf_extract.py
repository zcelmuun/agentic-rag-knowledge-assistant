import pymupdf as fitz

doc = fitz.open("data/guidebook_pdfs/guidebook_eng.pdf")

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    print(f"--- Page {page_num + 1} ---")
    print(text[:300])
    print()