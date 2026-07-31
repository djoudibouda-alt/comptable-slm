#!/usr/bin/env python3
"""
Comptable-SLM Demo — Moteur Q&A curé (TF-IDF accent-insensitive)
Assistant IA pour la comptabilité algérienne (SCF)
"""

import json, os, socket, unicodedata
from pathlib import Path

import gradio as gr
import numpy as np

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


def strip_accents(s):
    """Normalise les accents : é->e, è->e, etc."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


QADATA_PATH = Path(__file__).parent / "qa_dataset.json"

# ----------------------------------------------------------------
# Moteur de recherche Q&A (accent-insensitive)
# ----------------------------------------------------------------
class QASearch:
    def __init__(self, data_path: Path):
        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.questions = [item["question"] for item in self.data]
        self.answers = [item["answer"] for item in self.data]

        # Corpus normalisé sans accents
        self.search_texts = [
            strip_accents(f"{item['question']} {item.get('tags', '')}")
            for item in self.data
        ]
        self.questions_flat = [strip_accents(q).lower() for q in self.questions]

        self.vectorizer = None
        self.tfidf_matrix = None
        if HAVE_SKLEARN and self.search_texts:
            self.vectorizer = TfidfVectorizer(
                analyzer="word",
                ngram_range=(1, 3),
                max_features=10000,
                sublinear_tf=True,
                max_df=0.85,
                min_df=1,
            )
            self.tfidf_matrix = self.vectorizer.fit_transform(self.search_texts)

    def search(self, query: str) -> list[dict]:
        if not HAVE_SKLEARN or self.vectorizer is None:
            return []
        q_flat = strip_accents(query.lower())
        q_vec = self.vectorizer.transform([q_flat])
        scores = cosine_similarity(q_vec, self.tfidf_matrix).flatten()

        query_words = [w for w in q_flat.split() if len(w) > 3]
        boosted = []
        for i, score in enumerate(scores):
            bonus = 1.0
            for w in query_words:
                if w in self.questions_flat[i]:
                    bonus += 0.3
            boosted.append(score * bonus)

        best_idx = max(range(len(boosted)), key=lambda i: boosted[i])
        best_score = boosted[best_idx]

        has_match = any(w in self.questions_flat[best_idx] for w in query_words) if query_words else True
        if best_score < 0.15 or not has_match:
            return []

        return [{
            "question": self.questions[best_idx],
            "answer": self.answers[best_idx],
            "score": float(best_score),
        }]


# ----------------------------------------------------------------
# Initialisation
# ----------------------------------------------------------------
qa_search = QASearch(QADATA_PATH)

WELCOME = """# Comptable-SLM
### Assistant IA pour la comptabilité algérienne

Posez une question sur le SCF, la TVA, l'IBS, l'IRG, les charges sociales, l'audit, le droit des sociétés ou les écritures comptables.
"""

FALLBACK = (
    "Je n'ai pas trouvé de réponse à votre question.\n\n"
    "**Questions possibles :**\n"
    "- TVA : taux, comptes (4455/4456/4457), déclaration, écritures\n"
    "- IBS : taux 19%, calcul, acomptes\n"
    "- IRG : barème mensuel, retenue à la source\n"
    "- SARL / EURL : capital, création, différence\n"
    "- CASNOS / CNAS : taux, déclaration\n"
    "- SCF : classes, principes, documents comptables\n"
    "- Audit : normes, commissaire aux comptes\n"
    "- Écritures : achat, vente, TVA, amortissement, provision"
)


def find_answer(message: str) -> str:
    q = message.strip()
    if not q:
        return "Posez une question sur la comptabilité algérienne."

    results = qa_search.search(q)
    if not results:
        return FALLBACK

    best = results[0]
    ans = best["answer"].strip()
    if len(ans) > 2000:
        ans = ans[:2000] + "\n\n*... (texte tronqué)*"

    return ans


def chat(message: str, history: list):
    if not message or not message.strip():
        return "Posez une question sur la comptabilité algérienne."
    try:
        return find_answer(message)
    except Exception as e:
        return f"Erreur : {str(e)}"


EXAMPLES = [
    ["Quels sont les taux de TVA en Algérie ?"],
    ["Différence entre SARL et EURL ?"],
    ["Qu'est-ce que le SCF ?"],
    ["Comptabiliser un achat avec TVA 19%"],
    ["C'est quoi la CASNOS ?"],
    ["Qu'est-ce que l'IBS ?"],
    ["Comment fonctionne l'IRG ?"],
    ["Formes juridiques en Algérie ?"],
    ["Quels sont les comptes TVA dans le SCF ?"],
    ["Comment déclarer la TVA ?"],
    ["Qu'est-ce que le registre de commerce ?"],
    ["Amortissement comptable écriture"],
    ["Quel est le SMIG en Algérie ?"],
    ["Calendrier fiscal 2024"],
    ["Allocations familiales CNAS"],
]

demo = gr.ChatInterface(
    fn=chat,
    type="messages",
    title="Comptable-SLM",
    description=WELCOME,
    examples=[[e[0]] for e in EXAMPLES],
    theme="soft",
)

if __name__ == "__main__":
    if os.environ.get("RENDER") or os.environ.get("SPACE_ID"):
        demo.launch(server_name="0.0.0.0")
    else:
        port = 7860
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(("0.0.0.0", port))
                s.close()
                break
            except OSError:
                port += 1
        demo.launch(share=True, server_name="0.0.0.0", server_port=port)
