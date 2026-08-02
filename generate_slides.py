#!/usr/bin/env python3
"""
Génère les 10 slides PNG pour le carrousel LinkedIn.
Usage: python generate_slides.py
"""
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
ORANGE = "#f97316"
RED = "#ef4444"

def new_fig():
    fig, ax = plt.subplots(figsize=(10.8, 13.5), dpi=150)  # 1080x1350 = 4:5 LinkedIn
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax

def add_text(ax, x, y, text, fontsize=24, color=WHITE, weight="normal", ha="left", wrap_width=80, line_spacing=1.3):
    """Ajoute du texte avec wrap automatique."""
    import textwrap
    lines = textwrap.wrap(text, width=wrap_width)
    for i, line in enumerate(lines):
        ax.text(x, y - i * fontsize * line_spacing / 100 * 100, line,
                fontsize=fontsize, color=color, weight=weight, ha=ha, va="top")
    return y - len(lines) * fontsize * line_spacing / 100 * 100

def add_bullet_list(ax, x, y, items, fontsize=22, color=WHITE, bullet_color=ACCENT, spacing=1.5):
    for i, item in enumerate(items):
        ax.text(x, y - i * fontsize * spacing / 100 * 100, "●", fontsize=fontsize*1.2, color=bullet_color, ha="left", va="top")
        ax.text(x + 4, y - i * fontsize * spacing / 100 * 100, item, fontsize=fontsize, color=color, ha="left", va="top", wrap=True)
    return y - len(items) * fontsize * spacing / 100 * 100

def add_card(ax, x, y, w, h, title, body_items, title_color=ACCENT, body_color=WHITE):
    """Dessine une carte avec titre et liste."""
    # Fond carte
    rect = Rectangle((x, y - h), w, h, facecolor=CARD_BG, edgecolor=GRAY, linewidth=0.5, zorder=1)
    ax.add_patch(rect)
    # Titre
    ax.text(x + 3, y - 3, title, fontsize=20, color=title_color, weight="bold", ha="left", va="top")
    # Corps
    y_body = y - 10
    for item in body_items:
        ax.text(x + 3, y_body, f"• {item}", fontsize=16, color=body_color, ha="left", va="top")
        y_body -= 7
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
ax.text(50, 75, "Comptable-SLM", fontsize=56, color=WHITE, weight="bold", ha="center", va="center")
ax.text(50, 60, "Assistant IA pour la comptabilité\net l'audit algériens", fontsize=28, color=ACCENT, ha="center", va="center")
ax.text(50, 45, "RAG + SLM fine-tuné  |  100% droit algérien", fontsize=22, color=GRAY, ha="center", va="center")
ax.text(50, 25, "Link: https://comptable-slm-1.onrender.com", fontsize=20, color=ACCENT2, ha="center", va="center")
ax.text(50, 15, "#Comptabilité #Algérie #IA #SCF #Audit", fontsize=18, color=GRAY, ha="center", va="center")
save_slide(fig, "01_couverture")

# ============================================================
# SLIDE 2 : Le problème
# ============================================================
fig, ax = new_fig()
ax.text(50, 92, "Le problème", fontsize=42, color=RED, weight="bold", ha="center")
ax.text(50, 85, "Les IA actuelles ne connaissent pas la comptabilité africaine", fontsize=24, color=WHITE, ha="center")

items = [
    "Chaque pays a son propre système (SCF, TVA, charges sociales)",
    "ChatGPT / LLM génériques hallucinent sur le droit algérien",
    "Les comptables africains sont sous-équipés",
    "PDF épars, manuels obsolètes, consultants coûteux"
]
add_bullet_list(ax, 15, 75, items, fontsize=26, color=WHITE, bullet_color=RED, spacing=1.6)

ax.text(50, 15, "[X] TVA 19/9/0% -> Reponses francaises\n[X] SCF/PCN -> Confusion\n[X] CNAS/CASNOS -> Inventes",
        fontsize=20, color=GRAY, ha="center", va="bottom")
save_slide(fig, "02_probleme")

# ============================================================
# SLIDE 3 : La solution
# ============================================================
fig, ax = new_fig()
ax.text(50, 92, "La solution : Comptable-SLM", fontsize=42, color=GREEN, weight="bold", ha="center")

ax.text(15, 82, "Assistant IA spécialisé en comptabilité et audit algériens", fontsize=24, color=ACCENT, ha="left")

items = [
    "[OK] Reponses sourcees (pas d'hallucinations)",
    "[OK] Fonctionne hors ligne (zones sans internet)",
    "[OK] Connaît le SCF, TVA 19/9/0%, charges sociales CNAS/CASNOS",
    "[OK] SARL/EURL/SPA/SNC, IBS 19%, IRG bareme 2024",
    "[OK] 125 Q&A curees -- questions naturelles + reponses concises",
    "[OK] TF-IDF accent-insensitive (deductible = deductible)"
]
add_bullet_list(ax, 15, 72, items, fontsize=22, color=WHITE, bullet_color=GREEN, spacing=1.7)

save_slide(fig, "03_solution")

# ============================================================
# SLIDE 4 : Comment ça marche (Architecture)
# ============================================================
fig, ax = new_fig()
ax.text(50, 92, "Architecture technique", fontsize=42, color=ACCENT, weight="bold", ha="center")

# Pipeline RAG
add_card(ax, 8, 82, 42, 25, "[RAG] Pipeline RAG", [
    "Embeddings : NVIDIA Nemotron-3-Embed-1B (NIM)",
    "Vector store : ChromaDB (cosinus, persistant)",
    "7 fichiers KB → 534 chunks (section-based)",
    "TOP_K=4, seuil distance < 0.6",
    "Contexte injecté dans le prompt LLM"
], title_color=ACCENT)

# SLM Fine-tuné
add_card(ax, 52, 82, 42, 25, "[SLM] Fine-tune", [
    "Base : Llama 3.2 3B",
    "Méthode : Unsloth + QLoRA (4-bit)",
    "Dataset : 150 exemples algériens (SCF)",
    "Export : GGUF → Ollama (local)",
    "Loss : 1.89 → 0.03"
], title_color=ACCENT2)

# Flux
ax.text(50, 50, "Question → RAG (recherche loi SCF, code fiscal...)\n      → Contexte + Question → LLM\n      → Réponse précise avec sources",
        fontsize=22, color=WHITE, ha="center", va="center")

items = [
    "[Tech] NVIDIA NIM  |  [DB] ChromaDB  |  [Fast] Unsloth/QLoRA  |  [Pkg] GGUF + Ollama",
    "Differentiateur : fine-tune sur donnees africaines + hors ligne"
]
add_bullet_list(ax, 15, 30, items, fontsize=20, color=GRAY, bullet_color=ACCENT, spacing=1.5)

save_slide(fig, "04_architecture")

# ============================================================
# SLIDE 5 : Base de connaissances
# ============================================================
fig, ax = new_fig()
ax.text(50, 92, "Base de connaissances 100% algérienne", fontsize=40, color=ACCENT, weight="bold", ha="center")

kb_items = [
    ("01_scf_algerien.txt", "SCF — Loi 07-11, 7 classes, principes, plan comptable"),
    ("02_fiscalite_algerie.txt", "TVA 19/9/0%, IBS 19%, IRG barème, taxe pro, conventions"),
    ("03_normes_audit_algerie.txt", "ISA, commissaire aux comptes, audit interne, responsabilités"),
    ("04_droit_commercial_algerie.txt", "SARL/EURL/SPA/SNC, registre commerce, actes commerce"),
    ("05_charges_sociales.txt", "CNAS 7%, CASNOS 15%, congés, SMIG, assurance maladie"),
    ("06_formes_juridiques.txt", "Capital, associés, responsabilité, création, formalités"),
    ("07_procedures_pratiques.txt", "Calendrier fiscal, clôture, rapprochement, conservation"),
]

y = 82
for i, (fname, desc) in enumerate(kb_items):
    col = i % 2
    row = i // 2
    x = 8 + col * 46
    y_pos = y - row * 22
    add_card(ax, x, y_pos, 42, 18, fname.replace(".txt", "").replace("_", " ").title(), [desc], 
             title_color=ACCENT if i < 3 else ACCENT2)

ax.text(50, 10, "7 fichiers  •  534 chunks  •  Section-based chunking (##/### headers)",
        fontsize=18, color=GRAY, ha="center", va="bottom")
save_slide(fig, "05_knowledgebase")

# ============================================================
# SLIDE 6 : 125 Q&A curées
# ============================================================
fig, ax = new_fig()
ax.text(50, 92, "125 Q&A curées — Questions naturelles", fontsize=40, color=ACCENT, weight="bold", ha="center")

categories = [
    ("[TVA] TVA", ["Taux 19/9/0%", "Comptes 4455/4456/4457", "Declaration", "Ecritures achat/vente", "TVA deductible/collectee", "A decaisser"]),
    ("[IBS] IBS / IRG", ["IBS 19% uniforme", "Calcul + acomptes", "IRG bareme 2024", "Retenue source 4431"]),
    ("[SOC] SARL / EURL / SPA", ["Differences", "Capital 100k DA", "Creation formalites", "Commissaire aux comptes"]),
    ("[SOC] CNAS / CASNOS", ["Taux 7% / 15%", "Regimes declaration", "Allocations familiales", "Difference salariat/inde"]),
    ("[LAW] Audit / Droit", ["Normes ISA", "CAC obligations", "Registre commerce", "Actes de commerce"]),
    ("[WRITE] Ecritures / Procedures", ["Achat/vente TVA", "Amortissement", "Provision", "Calendrier fiscal", "Cloture exercice"]),
]

y = 80
for cat_name, items in categories:
    add_card(ax, 8, y, 84, 10, cat_name, items[:3] + (["..."] if len(items) > 3 else []), title_color=ACCENT2)
    y -= 11

ax.text(50, 10, "Chaque Q&A : question naturelle + réponse concise + tags de matching",
        fontsize=18, color=GRAY, ha="center", va="bottom")
save_slide(fig, "06_qa_curated")

# ============================================================
# SLIDE 7 : Résultats tests
# ============================================================
fig, ax = new_fig()
ax.text(50, 92, "Resultats : 37/37 tests [OK]", fontsize=42, color=GREEN, weight="bold", ha="center")

test_items = [
    ("[OK] TVA", ["taux", "deductible", "collectee", "declaration", "comptes 4455/6/7"]),
    ("[OK] IBS / IRG", ["taux 19%", "calcul", "bareme 2024", "compte 4431"]),
    ("[OK] SARL/EURL", ["difference", "capital", "creation", "CAC"]),
    ("[OK] CNAS/CASNOS", ["taux", "regimes", "allocations", "difference"]),
    ("[OK] Audit", ["normes ISA", "CAC", "registre commerce"]),
    ("[OK] Ecritures", ["achat TVA 19%", "amortissement", "provision"]),
    ("[OK] Procedures", ["calendrier fiscal", "cloture", "rapprochement bancaire"]),
]

y = 80
for title, items in test_items:
    add_card(ax, 8, y, 84, 8, title, items, title_color=GREEN)
    y -= 9.5

ax.text(50, 12, "Matching robuste : accents normalisés, TF-IDF word-level, bonus titre, seuil 0.15",
        fontsize=18, color=GRAY, ha="center", va="bottom")
save_slide(fig, "07_resultats")

# ============================================================
# SLIDE 8 : Démo en ligne
# ============================================================
fig, ax = new_fig()
ax.text(50, 92, "Demo en ligne -- Lien permanent", fontsize=42, color=ACCENT, weight="bold", ha="center")

ax.text(50, 78, "https://comptable-slm-1.onrender.com", fontsize=36, color=ACCENT2, weight="bold", ha="center")

add_card(ax, 15, 68, 70, 30, "Interface Gradio ChatInterface", [
    "• Questions libres en français",
    "• 12 exemples pré-chargés",
    "• Réponses instantanées (< 1s)",
    "• Sources citées automatiquement",
    "• Fallback intelligent si pas de réponse",
    "• Thème « soft » agréable"
], title_color=ACCENT)

ax.text(50, 30, "Hébergé sur Render (Free tier)\nLien permanent — partageable sur LinkedIn",
        fontsize=22, color=GRAY, ha="center", va="center")

ax.text(50, 15, "[Tip] Testez : \"Quels sont les taux de TVA en Algerie ? \"\n    ou \"Difference entre SARL et EURL ? \"",
        fontsize=20, color=ACCENT2, ha="center", va="bottom")
save_slide(fig, "08_demo")

# ============================================================
# SLIDE 9 : Roadmap & Vision
# ============================================================
fig, ax = new_fig()
ax.text(50, 92, "Roadmap & Vision panafricaine", fontsize=40, color=ACCENT, weight="bold", ha="center")

# 3 mois
add_card(ax, 8, 82, 42, 35, "[3M] 3 mois", [
    "Dataset 1 000+ exemples",
    "Support OHADA (16 pays)",
    "Interface web complète",
    "Beta test 20 cabinets algériens",
    "Optimisation RAG (reranking)",
    "Export GGUF validé"
], title_color=ACCENT)

# 6 mois
add_card(ax, 52, 82, 42, 35, "[6M] 6 mois", [
    "Maroc, Tunisie, Sénégal, CI",
    "Application mobile",
    "Intégration logiciels compta",
    "Extraction factures (Docling+Qwen)",
    "Analyseur Grand Livre (audit)",
    "Modèle multilingue (fr/ar)"
], title_color=ACCENT2)

# Vision
ax.text(50, 38, "[Target] Vision : L'assistant IA panafricain\nde reference pour la comptabilite",
        fontsize=26, color=WHITE, weight="bold", ha="center")

items = [
    "54 pays africains, chacun son système",
    "Zone OHADA = 16 pays cadre unifié",
    "TAM : 500 000+ comptables Afrique francophone"
]
add_bullet_list(ax, 15, 30, items, fontsize=20, color=GRAY, bullet_color=ACCENT, spacing=1.5)

save_slide(fig, "09_roadmap")

# ============================================================
# SLIDE 10 : Call to Action
# ============================================================
fig, ax = new_fig()
ax.text(50, 85, "Rejoignez l'aventure ! [Rocket]", fontsize=48, color=ACCENT, weight="bold", ha="center")

ax.text(50, 72, "Link: https://comptable-slm-1.onrender.com", fontsize=28, color=ACCENT2, weight="bold", ha="center")
ax.text(50, 65, "Code: github.com/djoudibouda-alt/comptable-slm", fontsize=24, color=GRAY, ha="center")

add_card(ax, 15, 55, 70, 30, "Pourquoi Google Africa Applied AI Lab ?", [
    "[Handshake] Acces anticipe Gemini / Gemma",
    "[Brain] Mentorat technique Google Research",
    "[Money] Reseau VCs africains (4DX, Norrsken, Novastar)",
    "[Globe] Passage Algerie -> OHADA -> Panafrique",
    "[Chart] 15+ ans expertise comptable + dev IA solo"
], title_color=GREEN)

ax.text(50, 18, "\"L'IA doit servir les professionnels africains, pas l'inverse.\"",
        fontsize=24, color=WHITE, weight="bold", ha="center", style="italic")

ax.text(50, 8, "#Comptabilité #Algérie #IA #SCF #Audit #GoogleAI #AfricaTech #Innovation",
        fontsize=18, color=GRAY, ha="center", va="bottom")
save_slide(fig, "10_cta")

print(f"\n[Done] 10 slides generees dans {OUT_DIR}/")