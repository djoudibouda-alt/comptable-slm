#!/usr/bin/env python3
"""
Génère un index sectionné de la base de connaissances.
Chaque section ## devient une entrée avec son contenu complet.
"""
import json, re
from pathlib import Path

KB_DIR = Path("knowledge_base")
OUTPUT = "qa_dataset.json"

def extract_sections(filepath):
    """Extrait toutes les sections ## d'un fichier knowledge_base."""
    text = filepath.read_text(encoding="utf-8")
    filename = filepath.stem

    # Ligne de titre principal (premier #)
    lines = text.split("\n")
    main_title = ""
    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            main_title = line.lstrip("# ").strip()
            break

    # Découpage par sections ##
    sections = re.split(r"\n(?=## )", text)
    entries = []

    for i, sec in enumerate(sections):
        sec = sec.strip()
        if not sec or len(sec) < 100:
            continue

        lines_sec = sec.split("\n")
        title = ""
        for line in lines_sec:
            if line.startswith("## "):
                title = line.lstrip("## ").strip()
                break

        if not title:
            title = main_title

        # Nettoyer le contenu (enlever les en-têtes markdown pour le search)
        content = sec
        content_clean = re.sub(r"#{1,3}\s*", "", content).strip()
        content_clean = re.sub(r"-{3,}", "", content_clean).strip()

        # Texte de recherche = titre + contenu (résumé pour l'index)
        # On prend les 800 premiers caractères pour l'indexation
        search_text = f"{title} {content_clean[:800]}"

        entries.append({
            "title": title,
            "search_text": search_text,
            "answer": content_clean,
            "source": filename,
        })

    return entries


def main():
    all_entries = []
    for f in sorted(KB_DIR.glob("*.txt")):
        print(f"Extraction: {f.name}")
        entries = extract_sections(f)
        all_entries.extend(entries)
        print(f"  -> {len(entries)} sections")

    print(f"\nTotal: {len(all_entries)} sections indexées")

    # Sauvegarder
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)
    print(f"Sauvegardé dans: {OUTPUT}")

if __name__ == "__main__":
    main()
