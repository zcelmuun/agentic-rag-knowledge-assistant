import pymupdf as fitz
import re
import json

pdf_files = {
    "english": "data/guidebook_pdfs/guidebook_eng.pdf",
    "korean": "data/guidebook_pdfs/guidebook_kor.pdf",
    "chinese": "data/guidebook_pdfs/guidebook_chn.pdf",
}

contents_marker_patterns = {
    "english": re.compile(r"Contents"),
    "korean": re.compile(r"목\s*차"),
    "chinese": re.compile(r"目\s*录"),
}

section_pattern = re.compile(r"\n\s*(\d{1,2})\s*\n\s*([^\n]+)\n")

MIN_CHUNK_LENGTH = 50

all_chunks = []

for language, filepath in pdf_files.items():
    doc = fitz.open(filepath)

    full_text = ""
    for page in doc:
        full_text += page.get_text()

    marker_pattern = contents_marker_patterns[language]
    marker_match = marker_pattern.search(full_text)

    if marker_match is None:
        print(f"WARNING: Could not find Contents marker for {language}")
        continue

    search_text = full_text[marker_match.start():]

    matches = list(section_pattern.finditer(search_text))

    for i, match in enumerate(matches):
        section_number = match.group(1)
        section_title = match.group(2).strip()
        start_pos = match.end()

        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(search_text)

        section_text = search_text[start_pos:end_pos].strip()

        if len(section_text) < MIN_CHUNK_LENGTH:
            continue

        chunk = {
            "language": language,
            "source_file": filepath,
            "section_number": section_number,
            "section_title": section_title,
            "text": section_text,
        }
        all_chunks.append(chunk)

print(f"Total chunks created: {len(all_chunks)}")
print()
for chunk in all_chunks:
    print(f"[{chunk['language']}] Section {chunk['section_number']}: {chunk['section_title']} ({len(chunk['text'])} chars)")

with open("data/chunks.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print()
print("Saved all chunks to data/chunks.json")