#!/usr/bin/env python3
"""
Génère les slides PDF/PNG pour carrousel LinkedIn — version minimaliste 100% Algérie.
Usage: python generate_slides.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path

OUT_DIR = Path("slides")
OUT_DIR.mkdir(exist_ok=True)

# Couleurs
DARK_BG = "#0f172a"      # slate-900
CARD_BG = "#1e293b"      # slate-800
ACCENT = "#38bdf8"       # sky-400
ACCENT2 = "#22d3ee"      # cyan-400
WHITE = "#f8fafc"
GRAY = "#94a3b8"
GREEN = "#22c55e"

def new_fig():
    fig, ax = plt.subplots(figsize=(10.8, 13.5), dpi=150)  # 1080x1350 = 4:5 LinkedIn
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax

def add_bullet_list(ax, x, y, items, fontsize=24, color=WHITE, bullet_color=ACCENT, spacing=1.6):
    for i, item in enumerate(items):
        ax.text(x, y - i * fontsize * spacing / 100 * 100, "●", fontsize=fontsize*1.2, color=bullet_color, ha="left", va="top")
        ax.text(x + 4, y - i * fontsize * spacing / 100 * 100, item, fontsize=fontsize, color=color, ha="left", va="top", wrap=True)
    return y - len(items) * fontsize * spacing / 100 * 100

def add_card(ax, x, y, w, h, title, body_items, title_color=ACCENT):
    rect = Rectangle((x, y - h), w, h, facecolor=CARD_BG, edgecolor=GRAY, linewidth=0.5, zorder=1)
    ax.add_patch(rect)
    ax.text(x + 3, y - 3, title, fontsize=22, color=title_color, weight="bold", ha="left", va="top")
    y_body = y - 12
    for item in body_items:
        ax.text(x + 3, y_body, f"• {item}", fontsize=18, color=WHITE, ha="left", va="top")
        y_body -= 8
    return y - h

def save_slide(fig, name):
    path = OUT_DIR / f"{name}.png"
    fig.savefig(path, facecolor=DARK_BG, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print(f"[OK] {path}")

# ============================================================
# SLIDE 1 : Couverture
# ============================================================
fig, ax = new_fig()
ax.text(50, 75, "Prototype SLM Droit comptable\net fiscal Algerien", fontsize=52, color=WHITE, weight="bold", ha="center", va="center")
ax.text(50, 58, "Comptable-SLM — RAG + SLM fine-tune", fontsize=26, color=ACCENT, ha="center", va="center")
ax.text(50, 48, "100% droit algerien  |  125 Q&A curees  |  37/37 tests", fontsize=22, color=GRAY, ha="center", va="center")
ax.text(50, 32, "https://comptable-slm-1.onrender.com", fontsize=22, color=ACCENT2, weight="bold", ha="center", va="center")
ax.text(50, 22, "#Comptabilite #Algerie #IA #SCF #Audit #SLM #RAG", fontsize=18, color=GRAY, ha="center", va="center")
save_slide(fig, "01_couverture")

# ============================================================
# SLIDE 2 : Le probleme
# ============================================================
fig, ax = new_fig()
ax.text(50, 92, "Le probleme : Les LLM hallucinent\nsur le droit algerien", fontsize=42, color="#ef4444", weight="bold", ha="center")

items = [
    "TVA 19/9/0% -> reponses francaises",
    "SCF (loi 07-11) vs ancien PCN -> confusion",
    "Comptes TVA 4455/4456/4457 -> inconnus",
    "CNAS 7% / CASNOS 15% -> melanges ou inventes",
    "IBS 19% uniforme, IRG bareme 2024 -> baremes etrangers",
    "SARL/EURL/SPA, commissaire aux comptes -> regles francaises",
]
add_bullet_list(ax, 15, 80, items, fontsize=24, bullet_color="#ef4444", spacing=1.5)

ax.text(50, 15, "ChatGPT, Claude... ne connaissent pas le droit comptable algerien",
        fontsize=20, color=GRAY, ha="center", va="bottom")
save_slide(fig, "02_probleme")

# ============================================================
# SLIDE 3 : La solution
# ============================================================
fig, ax = new_fig()
ax.text(50, 92, "La solution : Comptable-SLM", fontsize=44, color=GREEN, weight="bold", ha="center")
ax.text(50, 84, "RAG + SLM fine-tune 100% droit algerien", fontsize=26, color=ACCENT, ha="center")

# RAG card
add_card(ax, 8, 78, 42, 30, "[RAG] Pipeline RAG", [
    "Embeddings : NVIDIA Nemotron-3-Embed-1B (NIM)",
    "Vector store : ChromaDB (cosinus, persistant)",
    "7 fichiers KB -> 534 chunks (section-based)",
    "TOP_K=4, seuil distance < 0.6",
    "Contexte injecte dans le prompt LLM",
], title_color=ACCENT)

# SLM card
add_card(ax, 52, 78, 42, 30, "[SLM] Modele local", [
    "Base : Llama 3.2 3B",
    "Fine-tune : Unsloth + QLoRA (4-bit)",
    "Dataset : 150 exemples algeriens (SCF)",
    "Export : GGUF -> Ollama (offline)",
    "Loss : 1.89 -> 0.03",
], title_color=ACCENT2)

# Flux
ax.text(50, 38, "Question -> RAG (recherche loi SCF, code fiscal...)\n      -> Contexte + Question -> LLM\n      -> Reponse precise avec sources",
        fontsize=22, color=WHITE, ha="center", va="center")

items = [
    "TF-IDF word-level accent-insensitive (deductible = deductible)",
    "Reponses sourcees  |  Fallback intelligent (pas d'hallucination)",
]
add_bullet_list(ax, 15, 25, items, fontsize=20, bullet_color=ACCENT, spacing=1.5)
save_slide(fig, "03_solution")

# ============================================================
# SLIDE 4 : Ce qu'il maitrise (6 domaines)
# ============================================================
fig, ax = new_fig()
ax.text(50, 92, "Ce qu'il maitrise — 6 domaines cles", fontsize=42, color=ACCENT, weight="bold", ha="center")

domains = [
    ("[TVA] TVA", ["Taux 19/9/0%", "Comptes 4455/4456/4457", "Declaration", "Ecritures achat/vente"]),
    ("[IBS] IBS / IRG", ["IBS 19% uniforme", "Calcul + acomptes", "IRG bareme 2024", "Retenue source compte 4431"]),
    ("[SOC] Charges sociales", ["CNAS 7%", "CASNOS 15%", "Allocations familiales", "Conges payes 30j"]),
    ("[LAW] Formes juridiques", ["SARL/EURL/SPA/SNC", "Capital 100k DA", "Registre commerce"]),
    ("[SCALE] Audit", ["Normes ISA", "Commissaire aux comptes", "Obligations"]),
    ("[WRITE] Ecritures / Procedures", ["Achat/vente TVA", "Amortissement", "Provision", "Calendrier fiscal", "Cloture exercice"]),
]

y = 82
for title, items in domains:
    add_card(ax, 8, y, 84, 10, title, items[:3] + (["..."] if len(items) > 3 else []), title_color=ACCENT2)
    y -= 11

ax.text(50, 10, "Tests : 37/37 reponses pertinentes",
        fontsize=20, color=GREEN, weight="bold", ha="center", va="bottom")
save_slide(fig, "04_domaines")

# ============================================================
# SLIDE 5 : Resultats tests
# ============================================================
fig, ax = new_fig()
ax.text(50, 92, "Resultats : 37/37 tests reussis", fontsize=44, color=GREEN, weight="bold", ha="center")

test_items = [
    ("[OK] TVA", ["taux 19/9/0%", "deductible", "collectee", "declaration", "comptes 4455/6/7"]),
    ("[OK] IBS / IRG", ["IBS 19%", "calcul", "bareme IRG 2024", "compte 4431"]),
    ("[OK] Charges sociales", ["CNAS 7%", "CASNOS 15%", "allocations", "conges payes"]),
    ("[OK] Formes juridiques", ["SARL vs EURL", "capital 100k", "CAC"]),
    ("[OK] Audit", ["normes ISA", "CAC obligations", "registre commerce"]),
    ("[OK] Ecritures", ["achat TVA 19%", "amortissement", "provision"]),
    ("[OK] Procedures", ["calendrier fiscal", "cloture", "rapprochement bancaire"]),
]

y = 80
for title, items in test_items:
    add_card(ax, 8, y, 84, 8, title, items, title_color=GREEN)
    y -= 9.5

ax.text(50, 12, "Matching robuste : TF-IDF word-level, accents normalises, bonus titre, seuil 0.15",
        fontsize=18, color=GRAY, ha="center", va="bottom")
save_slide(fig, "05_resultats")

# ============================================================
# SLIDE 6 : Demo en ligne
# ============================================================
fig, ax = new_fig()
ax.text(50, 92, "Demo en ligne — Lien permanent", fontsize=44, color=ACCENT, weight="bold", ha="center")

ax.text(50, 78, "https://comptable-slm-1.onrender.com", fontsize=36, color=ACCENT2, weight="bold", ha="center")

add_card(ax, 15, 68, 70, 30, "Interface Gradio ChatInterface", [
    "Questions libres en francais",
    "12 exemples pre-charges",
    "Reponses instantanees (< 1s)",
    "Sources citees automatiquement",
    "Fallback intelligent si pas de reponse",
    "Theme « soft » agreable",
], title_color=ACCENT)

ax.text(50, 30, "Heberge sur Render (Free tier)\nLien permanent — partageable sur LinkedIn",
        fontsize=22, color=GRAY, ha="center", va="center")

ax.text(50, 18, 'Testez : "Quels sont les taux de TVA en Algerie ?"\nou "Difference entre SARL et EURL ?"',
        fontsize=22, color=ACCENT2, ha="center", va="bottom")
save_slide(fig, "06_demo")

# ============================================================
# SLIDE 7 : Cloture
# ============================================================
fig, ax = new_fig()
ax.text(50, 80, '"L IA doit servir les professionnels\nalgeriens, pas l inverse."', fontsize=40, color=WHITE, weight="bold", ha="center", style="italic")

ax.text(50, 65, "— Expert-comptable & Auditeur legal (15+ ans) | Dev IA", fontsize=22, color=GRAY, ha="center")

ax.text(50, 50, "Public cible :", fontsize=26, color=ACCENT, weight="bold", ha="center")
ax.text(50, 43, "Experts-comptables, Commissaires aux comptes, Comptables agrees,\nEtudiants, Cabinets d'audit algeriens",
        fontsize=22, color=WHITE, ha="center")

ax.text(50, 30, "Code : github.com/djoudibouda-alt/comptable-slm", fontsize=22, color=GRAY, ha="center")
ax.text(50, 24, "Demo : https://comptable-slm-1.onrender.com", fontsize=22, color=ACCENT2, weight="bold", ha="center")

ax.text(50, 12, "#Comptabilite #Algerie #IA #SCF #Audit #TVA #IBS #IRG #CNAS #CASNOS #SLM #RAG",
        fontsize=18, color=GRAY, ha="center", va="bottom")
save_slide(fig, "07_cloture")

print(f"\n[Done] 7 slides generees dans {OUT_DIR}/")