#!/usr/bin/env python3
"""
Génère le dataset Q&A complet à partir de la base de connaissances.
"""
import json, re
from pathlib import Path

KB_DIR = Path("knowledge_base")
OUTPUT = "qa_dataset.json"

def extract_qa_from_file(filepath):
    """Extrait des paires Q&A à partir des sections du fichier knowledge base."""
    text = filepath.read_text(encoding="utf-8")
    filename = filepath.stem
    qa_pairs = []

    # Découpage par sections ##
    sections = re.split(r"\n## ", text)
    for i, section in enumerate(sections):
        if i == 0:
            # Titre principal
            title = section.strip().split("\n")[0].lstrip("# ")
            content = section
        else:
            title = section.split("\n")[0].strip()
            content = "## " + section

        if len(content) < 100:
            continue

        content_clean = re.sub(r"#+\s*", "", content).strip()
        content_short = content_clean[:500]

        # Générer questions à partir du titre
        title_lower = title.lower()

        qa_pairs.append({
            "question": f"Qu'est-ce que {title} ?",
            "answer": content_short,
            "source": filename,
            "section": title
        })

        qa_pairs.append({
            "question": f"Expliquez {title}",
            "answer": content_short,
            "source": filename,
            "section": title
        })

        # Extraire les mots-clés du titre pour générer plus de questions
        keywords = re.findall(r"\b[A-Z][a-zéèêëàâäùûüôöîïç]{3,}\b", title)
        for kw in keywords[:3]:
            if kw not in ("Avec", "Pour", "Dans", "Sur", "Par", "Les", "Des"):
                qa_pairs.append({
                    "question": f"Parlez-moi de {kw}",
                    "answer": content_short,
                    "source": filename,
                    "section": title
                })

    return qa_pairs


def main():
    all_qa = []
    for f in sorted(KB_DIR.glob("*.txt")):
        print(f"Extraction: {f.name}")
        try:
            qa = extract_qa_from_file(f)
            all_qa.extend(qa)
            print(f"  -> {len(qa)} questions")
        except Exception as e:
            print(f"  Erreur: {e}")

    # Supprimer les doublons
    seen = set()
    unique_qa = []
    for qa in all_qa:
        key = (qa["question"], qa["answer"][:100])
        if key not in seen:
            seen.add(key)
            unique_qa.append(qa)

    print(f"\nTotal: {len(unique_qa)} paires Q&A uniques")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(unique_qa, f, ensure_ascii=False, indent=2)
    print(f"Sauvegardé dans: {OUTPUT}")

if __name__ == "__main__":
    main()
