#!/usr/bin/env python3
"""
Comptable-SLM Demo — Version enrichie (TF-IDF)
Assistant IA pour la comptabilité algérienne (SCF)
"""

import json, os, socket
from pathlib import Path

import gradio as gr
import numpy as np

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


QADATA_PATH = Path(__file__).parent / "qa_dataset.json"

# ----------------------------------------------------------------
# Moteur de recherche TF-IDF
# ----------------------------------------------------------------
class QASearch:
    def __init__(self, data_path: Path):
        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.questions = [item["question"] for item in self.data]
        self.answers = [item["answer"] for item in self.data]
        self.vectorizer = None
        self.tfidf_matrix = None
        if HAVE_SKLEARN and self.questions:
            self.vectorizer = TfidfVectorizer(
                analyzer="char_wb",
                ngram_range=(2, 5),
                max_features=5000,
                sublinear_tf=True,
            )
            self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not HAVE_SKLEARN or self.vectorizer is None:
            return self._fallback_search(query, top_k)
        q_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self.tfidf_matrix).flatten()
        best_idx = scores.argmax()
        best_score = scores[best_idx]
        if best_score < 0.15:
            return []
        return [{
            "question": self.questions[best_idx],
            "answer": self.answers[best_idx],
            "score": float(best_score),
        }]

    def _fallback_search(self, query: str, top_k: int) -> list[dict]:
        q = query.lower()
        results = []
        for i, qtext in enumerate(self.questions):
            score = 0
            for word in q.split():
                if word in qtext.lower():
                    score += 1
            if score > 0:
                results.append((score / max(len(q.split()), 1), i))
        results.sort(reverse=True, key=lambda x: x[0])
        best = []
        for score, idx in results[:top_k]:
            if score > 0.3:
                best.append({
                    "question": self.questions[idx],
                    "answer": self.answers[idx],
                    "score": score,
                })
        return best


# ----------------------------------------------------------------
# Chargement
# ----------------------------------------------------------------
qa_search = QASearch(QADATA_PATH)

WELCOME = """# Comptable-SLM
### Assistant IA pour la comptabilité algérienne

Posez une question sur le SCF, la TVA, les charges sociales, l'audit, le droit des sociétés, ou les procédures pratiques.
"""

FALLBACK = (
    "Je ne connais pas encore cette question.\n\n"
    "Essayez : TVA, SARL, EURL, SCF, écritures, CASNOS, IBS, IRG, "
    "formes juridiques, audit, procédures."
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
    if len(ans) > 1200:
        ans = ans[:1200] + "..."
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
    ["Quelles sont les normes d'audit en Algérie ?"],
    ["Comment déclarer la TVA ?"],
    ["Obligations comptables du commerçant ?"],
    ["Qu'est-ce que le registre de commerce ?"],
]

demo = gr.ChatInterface(
    fn=chat,
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
