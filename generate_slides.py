#!/usr/bin/env python3
"""
Génère les slides PDF/PNG pour carrousel LinkedIn — design professionnel minimaliste.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path

OUT_DIR = Path("slides")
OUT_DIR.mkdir(exist_ok=True)

# Couleurs
DARK = "#0f172a"         # slate-900
CARD = "#1e293b"         # slate-800
ACCENT = "#38bdf8"       # sky-400
ACCENT2 = "#22d3ee"      # cyan-400
WHITE = "#f8fafc"
MUTED = "#94a3b8"
GREEN = "#22c55e"
RED = "#ef4444"

def new_fig():
    fig, ax = plt.subplots(figsize=(10.8, 13.5), dpi=150)
    fig.patch.set_facecolor(DARK)
    ax.set_facecolor(DARK)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax

def card(ax, x, y, w, h, title, bullets, title_color=ACCENT, radius=0):
    """Dessine une carte arrondie."""
    rect = Rectangle((x, y - h), w, h, facecolor=CARD, edgecolor="#334155", linewidth=1, zorder=1)
    if radius:
        rect.set_path_effects([])
    ax.add_patch(rect)
    # Titre
    ax.text(x + 24, y - 20, title, fontsize=26, color=title_color, weight="bold", ha="left", va="top")
    # Bullets
    y_b = y - 52
    for b in bullets:
        ax.text(x + 24, y_b, "▸ " + b, fontsize=20, color=WHITE, ha="left", va="top")
        y_b -= 28
    return y - h

def section_title(ax, x, y, text, color=ACCENT):
    ax.text(x, y, text, fontsize=22, color=color, weight="bold", ha="left", va="top")
    return y - 30

def save(fig, name):
    fig.savefig(OUT_DIR / f"{name}.png", facecolor=DARK, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print(f"[OK] {name}.png")

# ============================================================
# SLIDE 1 : COUVERTURE
# ============================================================
fig, ax = new_fig()
ax.text(50, 72, "Prototype SLM", fontsize=58, color=WHITE, weight="bold", ha="center")
ax.text(50, 60, "Droit comptable & fiscal\nAlgérien", fontsize=40, color=ACCENT, ha="center", linespacing=1.3)
ax.text(50, 44, "Comptable-SLM", fontsize=24, color=MUTED, ha="center")
ax.text(50, 38, "RAG + SLM fine-tuné  |  100% droit algérien", fontsize=22, color=MUTED, ha="center")
ax.text(50, 28, "https://comptable-slm-1.onrender.com", fontsize=24, color=ACCENT2, weight="bold", ha="center")
ax.text(50, 18, "#Comptabilité #Algérie #IA #SCF #Audit #SLM #RAG", fontsize=18, color=MUTED, ha="center")
save(fig, "01_couverture")

# ============================================================
# SLIDE 2 : PROBLÈME
# ============================================================
fig, ax = new_fig()
ax.text(50, 90, "Le problème", fontsize=48, color=RED, weight="bold", ha="center")
ax.text(50, 82, "Les LLM généralistes hallucinent sur le droit algérien", fontsize=24, color=MUTED, ha="center")

problems = [
    ("TVA 19/9/0%", "→ Réponses françaises"),
    ("SCF (loi 07-11) vs PCN", "→ Confusion"),
    ("Comptes TVA 4455/4456/4457", "→ Inconnus"),
    ("CNAS 7% / CASNOS 15%", "→ Mélangés ou inventés"),
    ("IBS 19% / IRG barème 2024", "→ Barèmes étrangers"),
    ("SARL / EURL / SPA", "→ Règles françaises"),
]

y = 72
for topic, issue in problems:
    card(ax, 10, y, 80, 28, topic, [issue], title_color=RED, radius=8)
    y -= 30

ax.text(50, 8, "ChatGPT, Claude... ne connaissent pas le droit comptable algérien",
        fontsize=20, color=MUTED, ha="center", va="bottom")
save(fig, "02_probleme")

# ============================================================
# SLIDE 3 : SOLUTION (RAG + SLM)
# ============================================================
fig, ax = new_fig()
ax.text(50, 90, "La solution : Comptable-SLM", fontsize=46, color=GREEN, weight="bold", ha="center")
ax.text(50, 84, "RAG + SLM fine-tuné — 100% droit algérien", fontsize=24, color=ACCENT, ha="center")

# RAG
card(ax, 10, 78, 38, 38, "[RAG] Pipeline RAG", [
    "Embeddings : Nemotron-3-Embed-1B (NIM)",
    "Vector store : ChromaDB (cosinus, persistant)",
    "7 fichiers KB → 534 chunks (section-based)",
    "TOP_K=4, seuil < 0.6",
    "Contexte injecté dans le prompt LLM",
], title_color=ACCENT)

# SLM
card(ax, 52, 78, 38, 38, "[SLM] Modèle local", [
    "Base : Llama 3.2 3B",
    "Fine-tune : Unsloth + QLoRA (4-bit)",
    "Dataset : 150 ex. algériens (SCF)",
    "Export : GGUF → Ollama (offline)",
    "Loss : 1.89 → 0.03",
], title_color=ACCENT2)

# Flux
ax.text(50, 36, "Question → RAG (loi SCF, code fiscal...)", fontsize=22, color=WHITE, ha="center")
ax.text(50, 31, "→ Contexte + Question → LLM", fontsize=22, color=WHITE, ha="center")
ax.text(50, 26, "→ Réponse précise avec sources", fontsize=22, color=WHITE, ha="center")

ax.text(50, 16, "TF-IDF word-level accent-insensitive  |  Réponses sourcées  |  Fallback intelligent",
        fontsize=18, color=MUTED, ha="center")
save(fig, "03_solution")

# ============================================================
# SLIDE 4 : 6 DOMAINES MAÎTRISÉS
# ============================================================
fig, ax = new_fig()
ax.text(50, 90, "Ce qu'il maîtrise — 6 domaines clés", fontsize=44, color=ACCENT, weight="bold", ha="center")

domains = [
    ("TVA", ["Taux 19/9/0%", "Comptes 4455/4456/4457", "Déclaration", "Écritures achat/vente"], ACCENT),
    ("IBS / IRG", ["IBS 19% uniforme", "Calcul + acomptes", "IRG barème 2024", "Retenue source 4431"], ACCENT2),
    ("Charges sociales", ["CNAS 7%", "CASNOS 15%", "Allocations familiales", "Congés payés 30j"], GREEN),
    ("Formes juridiques", ["SARL / EURL / SPA / SNC", "Capital 100k DA", "Registre commerce"], "#f97316"),
    ("Audit", ["Normes ISA", "Commissaire aux comptes", "Obligations CAC"], "#a855f7"),
    ("Écritures / Procédures", ["Achat/vente TVA", "Amortissement / Provision", "Calendrier fiscal", "Clôture / Rapprochement"], "#ec4899"),
]

y = 82
for title, items, color in domains:
    card(ax, 10, y, 80, 16, title, items[:3], title_color=color)
    y -= 18

ax.text(50, 6, "Tests : 37/37 réponses pertinentes", fontsize=22, color=GREEN, weight="bold", ha="center")
save(fig, "04_domaines")

# ============================================================
# SLIDE 5 : RÉSULTATS TESTS
# ============================================================
fig, ax = new_fig()
ax.text(50, 90, "Résultats : 37/37 tests ✅", fontsize=44, color=GREEN, weight="bold", ha="center")

results = [
    ("TVA", ["taux 19/9/0%", "déductible", "collectée", "déclaration", "comptes 4455/6/7"]),
    ("IBS / IRG", ["IBS 19%", "calcul + acomptes", "barème IRG 2024", "compte 4431"]),
    ("Charges sociales", ["CNAS 7%", "CASNOS 15%", "allocations", "congés payés"]),
    ("Formes juridiques", ["SARL vs EURL", "capital 100k", "CAC"]),
    ("Audit", ["normes ISA", "CAC obligations", "registre commerce"]),
    ("Écritures", ["achat TVA 19%", "amortissement", "provision"]),
    ("Procédures", ["calendrier fiscal", "clôture", "rapprochement bancaire"]),
]

y = 80
for title, items in results:
    card(ax, 10, y, 80, 9, title, items, title_color=GREEN)
    y -= 10.5

ax.text(50, 8, "Matching : TF-IDF word-level  +  accents normalisés  +  bonus titre  +  seuil 0.15",
        fontsize=17, color=MUTED, ha="center")
save(fig, "05_resultats")

# ============================================================
# SLIDE 6 : DÉMO EN LIGNE
# ============================================================
fig, ax = new_fig()
ax.text(50, 90, "Démo en ligne — Lien permanent", fontsize=44, color=ACCENT, weight="bold", ha="center")

ax.text(50, 80, "https://comptable-slm-1.onrender.com", fontsize=34, color=ACCENT2, weight="bold", ha="center")

card(ax, 10, 70, 80, 36, "[UI] Interface Gradio ChatInterface", [
    "▸ Questions libres en français",
    "▸ 12 exemples pré-chargés",
    "▸ Réponses instantanées (< 1s)",
    "▸ Sources citées automatiquement",
    "▸ Fallback intelligent (pas d'hallucination)",
    "▸ Thème « soft » agréable",
], title_color=ACCENT)

ax.text(50, 28, "Hébergé sur Render (Free tier)  —  Lien permanent partageable",
        fontsize=20, color=MUTED, ha="center")

ax.text(50, 16, 'Testez : "Quels sont les taux de TVA en Algérie ?"  ou  "Différence SARL / EURL ?"',
        fontsize=20, color=ACCENT2, ha="center")
save(fig, "06_demo")

# ============================================================
# SLIDE 7 : CLÔTURE
# ============================================================
fig, ax = new_fig()

ax.text(50, 80, '"L\'IA doit servir les professionnels\nalgériens, pas l\'inverse."', fontsize=38, color=WHITE, weight="bold", ha="center", linespacing=1.4)

ax.text(50, 64, "— Expert-comptable & Auditeur légal (15+ ans)  |  Développeur IA", fontsize=20, color=MUTED, ha="center")

ax.text(50, 54, "Public cible", fontsize=28, color=ACCENT, weight="bold", ha="center")
ax.text(50, 48, "Experts-comptables  •  Commissaires aux comptes  •  Comptables agréés\nÉtudiants  •  Cabinets d'audit algériens", fontsize=20, color=WHITE, ha="center", linespacing=1.5)

ax.text(50, 36, "Démo : https://comptable-slm-1.onrender.com", fontsize=22, color=ACCENT2, weight="bold", ha="center")
ax.text(50, 30, "Code  : github.com/djoudibouda-alt/comptable-slm", fontsize=20, color=MUTED, ha="center")

ax.text(50, 16, "#Comptabilité #Algérie #IA #SCF #Audit #TVA #IBS #IRG #CNAS #CASNOS #SLM #RAG",
        fontsize=18, color=MUTED, ha="center", va="bottom")
save(fig, "07_cloture")

print("\n[Done] 7 slides générées")