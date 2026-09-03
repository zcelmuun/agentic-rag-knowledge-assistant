import pymupdf as fitz

pdf_files = {
    "english": "data/guidebook_pdfs/guidebook_eng.pdf",
    "korean": "data/guidebook_pdfs/guidebook_kor.pdf",
    "chinese": "data/guidebook_pdfs/guidebook_chn.pdf",
}

for language, filepath in pdf_files.items():
    doc = fitz.open(filepath)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    output_path = f"data/{language}_full_text.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"Saved {language}: {len(full_text)} characters -> {output_path}")