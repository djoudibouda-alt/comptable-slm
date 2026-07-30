#!/usr/bin/env python3
"""
Comptable-SLM Demo — Moteur de recherche sectionnée (TF-IDF word-level)
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
# Règles de priorité : mots-clés → réponses rédigées
# ----------------------------------------------------------------
HARDCODED = {
    "tva": (
        "**Taux de TVA en Algérie :**\n\n"
        "- **19%** - Taux normal (ventes de biens, prestations de services)\n"
        "- **9%** - Taux réduit (produits alimentaires, transports, édition)\n"
        "- **0%** - Exonérations (exportations, biens d'équipement)\n\n"
        "Source : Code des impôts algérien"
    ),
    "sarl": (
        "**SARL vs EURL**\n\n"
        "**SARL :** 2 à 50 associés, capital minimum 100 000 DA\n"
        "**EURL :** 1 associé unique, même régime que SARL\n\n"
        "Source : Code de commerce algérien"
    ),
    "scf": (
        "**SCF — Système Comptable et Financier**\n\n"
        "Loi n° 07-11 du 25 novembre 2007\n\n"
        "**7 classes de comptes :**\n"
        "1. Financement permanent\n"
        "2. Actif immobilisé\n"
        "3. Stocks\n"
        "4. Tiers\n"
        "5. Trésorerie\n"
        "6. Charges\n"
        "7. Produits"
    ),
    "ecriture": (
        "**Écriture type : Achat avec TVA 19%**\n\n"
        "Achat 100 000 DA + TVA 19 000 DA\n\n"
        "  Débit 60 (Achats)            100 000\n"
        "  Débit 4456 (TVA déduct.)      19 000\n"
        "  Crédit 401 (Fournisseur)             119 000\n\n"
        "Source : SCF algérien"
    ),
    "casnos": (
        "**CASNOS — Non-Salariés**\n\n"
        "Taux : 15% du revenu déclaré\n"
        "- 7,5% Retraite\n"
        "- 7,5% Assurances sociales\n\n"
        "Régimes : Réel, IFU, Simplifié"
    ),
    "ibs": (
        "**IBS — Impôt sur les Bénéfices des Sociétés**\n\n"
        "Taux : 19% du résultat fiscal (uniforme)\n\n"
        "Source : Code des impôts"
    ),
    "irg": (
        "**IRG — Retenue à la source**\n\n"
        "Barème mensuel 2024 :\n"
        "- **0%** : jusqu'à 30 000 DA\n"
        "- **23%** : 30 001 à 120 000 DA\n"
        "- **27%** : 120 001 à 300 000 DA\n"
        "- **35%** : plus de 300 000 DA\n\n"
        "Compte SCF : 4431 — IRG retenu à la source"
    ),
    "droit": (
        "**Formes juridiques en Algérie**\n\n"
        "- **SARL** : 2 à 50 associés, responsabilité limitée\n"
        "- **EURL** : 1 associé, responsabilité limitée\n"
        "- **SNC** : 2+ associés, responsabilité illimitée\n"
        "- **SPA** : 7+ actionnaires, capital minimum 1 000 000 DA (non-cotée)\n\n"
        "Source : Code de commerce"
    ),
}

# Ordre de check : (mot-clé à chercher, clé dans HARDCODED)
KEYWORD_MAP = [
    ("tva", "tva"),
    ("sarl", "sarl"),
    ("eurl", "sarl"),
    ("scf", "scf"),
    ("ecritur", "ecriture"),
    ("comptabilis", "ecriture"),
    ("achat", "ecriture"),
    ("casnos", "casnos"),
    ("ibs", "ibs"),
    ("irg", "irg"),
    ("societe", "droit"),
    ("spa", "droit"),
    ("snc", "droit"),
    ("forme juridique", "droit"),
]

# ----------------------------------------------------------------
# Moteur de recherche sectionnée (TF-IDF word-level)
# ----------------------------------------------------------------
class SectionSearch:
    def __init__(self, data_path: Path):
        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.corpus = [item["search_text"] for item in self.data]
        self.vectorizer = None
        self.tfidf_matrix = None
        if HAVE_SKLEARN and self.corpus:
            self.vectorizer = TfidfVectorizer(
                analyzer="word",
                ngram_range=(1, 3),
                max_features=10000,
                sublinear_tf=True,
                stop_words=None,
                max_df=0.85,
                min_df=1,
            )
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not HAVE_SKLEARN or self.vectorizer is None:
            return self._fallback_search(query, top_k)
        q_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self.tfidf_matrix).flatten()

        # Mots significatifs de la requête (longueur > 3)
        query_words = [w.lower() for w in query.split() if len(w) > 3]

        # Appliquer un bonus si les mots de la requête apparaissent dans le titre
        boosted = []
        for i, score in enumerate(scores):
            bonus = 1.0
            title_lower = self.data[i]["title"].lower()
            for w in query_words:
                if w in title_lower:
                    bonus += 0.3
            boosted.append(score * bonus)

        best_idx = max(range(len(boosted)), key=lambda i: boosted[i])
        best_score = boosted[best_idx]

        THRESHOLD = 0.10
        if best_score < THRESHOLD:
            return []

        # Vérifier la pertinence : mot significatif dans titre OU début de réponse
        title_lower = self.data[best_idx]["title"].lower()
        answer_start = self.data[best_idx]["answer"].lower()[:300]
        has_relevance = (
            any(w in title_lower for w in query_words)
            or any(w in answer_start for w in query_words)
        ) if query_words else True
        if not has_relevance:
            return []

        return [{
            "title": self.data[best_idx]["title"],
            "answer": self.data[best_idx]["answer"],
            "source": self.data[best_idx]["source"],
            "score": float(best_score),
        }]

    def _fallback_search(self, query: str, top_k: int) -> list[dict]:
        q = query.lower()
        results = []
        for i, text in enumerate(self.corpus):
            score = sum(1 for w in q.split() if w in text.lower())
            if score > 0:
                results.append((score / max(len(q.split()), 1), i))
        results.sort(reverse=True, key=lambda x: x[0])
        for score, idx in results[:top_k]:
            if score > 0.3:
                return [{
                    "title": self.data[idx]["title"],
                    "answer": self.data[idx]["answer"],
                    "source": self.data[idx]["source"],
                    "score": score,
                }]
        return []


# ----------------------------------------------------------------
# Initialisation
# ----------------------------------------------------------------
section_search = SectionSearch(QADATA_PATH)

WELCOME = """# Comptable-SLM
### Assistant IA pour la comptabilité algérienne

Posez une question sur le SCF, la TVA, les charges sociales, l'audit, le droit des sociétés ou les procédures pratiques.
"""

FALLBACK = (
    "Je n'ai pas trouvé de réponse dans ma base de connaissances.\n\n"
    "Essayez : TVA, SARL, EURL, SCF, écritures comptables, CASNOS, IBS, IRG, "
    "formes juridiques, audit, déclaration fiscale, registre de commerce."
)


def find_answer(message: str) -> str:
    q = message.strip()
    if not q:
        return "Posez une question sur la comptabilité algérienne."

    # 1. Vérifier les réponses rédigées par mot-clé
    q_lower = q.lower()
    for kw, key in KEYWORD_MAP:
        if kw in q_lower:
            return HARDCODED[key]

    # 2. Chercher dans les sections de la base de connaissances
    results = section_search.search(q)
    if not results:
        return FALLBACK

    best = results[0]
    ans = best["answer"].strip()
    if len(ans) > 1500:
        ans = ans[:1500] + "\n\n*... (texte tronqué)*"

    source_name = best["source"].replace("_", " ").title()
    return f"{ans}\n\n— *Source : {source_name}*"


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
    ["Comment déclarer la TVA ?"],
    ["Obligations comptables du commerçant ?"],
    ["Qu'est-ce que le registre de commerce ?"],
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
