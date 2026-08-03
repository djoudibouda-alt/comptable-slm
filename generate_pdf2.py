#!/usr/bin/env python3
"""
Génère le PDF combiné (carrousel LinkedIn) à partir des PDFs individuels.
Usage: python generate_pdf2.py
"""
from pathlib import Path
import fitz  # PyMuPDF

OUT_DIR = Path("slides")
OUT_PDF = Path("Comptable_SLM_Slides_Carousel.pdf")

slide_files = sorted(OUT_DIR.glob("*.pdf"))

doc = fitz.open()
for pdf_path in slide_files:
    src = fitz.open(pdf_path)
    doc.insert_pdf(src)
    src.close()

doc.save(OUT_PDF)
doc.close()

print(f"[OK] PDF combiné : {OUT_PDF} ({len(slide_files)} pages)")
print(f"Taille : {OUT_PDF.stat().st_size / 1024:.0f} KB")