#!/usr/bin/env python3
"""
Génère un PDF multipage avec PIL directement (plus fiable).
"""
from PIL import Image
from pathlib import Path

OUT_DIR = Path("slides")
OUT_PDF = Path("Comptable_SLM_Slides.pdf")

slide_files = sorted(OUT_DIR.glob("*.png"))

# Charger toutes les images en RGB
images = []
for img_path in slide_files:
    img = Image.open(img_path).convert("RGB")
    images.append(img)

# Sauvegarder en PDF multipage
images[0].save(
    OUT_PDF,
    save_all=True,
    append_images=images[1:],
    resolution=150,
    quality=95
)

print(f"[OK] PDF genere : {OUT_PDF} ({len(images)} pages)")
print(f"Taille : {OUT_PDF.stat().st_size / 1024:.0f} KB")