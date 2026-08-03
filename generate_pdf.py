#!/usr/bin/env python3
"""
Convertit les slides PNG en un seul PDF pour LinkedIn.
"""
import img2pdf
from pathlib import Path

SLIDES_DIR = Path("slides")
OUT_PDF = Path("Comptable_SLM_Slides.pdf")

slide_files = sorted(SLIDES_DIR.glob("*.png"))

with open(OUT_PDF, "wb") as f:
    f.write(img2pdf.convert([str(p) for p in slide_files]))

print(f"[OK] PDF généré : {OUT_PDF} ({len(slide_files)} pages)")
print(f"Taille : {OUT_PDF.stat().st_size / 1024:.0f} KB")