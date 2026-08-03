#!/usr/bin/env python3
"""
Slide tutoriel : Comment utiliser Comptable-SLM
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path

OUT_DIR = Path("slides")
OUT_DIR.mkdir(exist_ok=True)

DARK = "#0f172a"
CARD = "#1e293b"
ACCENT = "#38bdf8"
ACCENT2 = "#22d3ee"
WHITE = "#f8fafc"
MUTED = "#94a3b8"
GREEN = "#22c55e"

def new_fig():
    fig, ax = plt.subplots(figsize=(10.8, 13.5), dpi=150)
    fig.patch.set_facecolor(DARK)
    ax.set_facecolor(DARK)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax

def card(ax, x, y, w, h, title, bullets, title_color=ACCENT):
    rect = Rectangle((x, y - h), w, h, facecolor=CARD, edgecolor="#334155", linewidth=1, zorder=1)
    ax.add_patch(rect)
    ax.text(x + 24, y - 20, title, fontsize=26, color=title_color, weight="bold", ha="left", va="top")
    y_b = y - 52
    for b in bullets:
        ax.text(x + 24, y_b, "▸ " + b, fontsize=20, color=WHITE, ha="left", va="top")
        y_b -= 28
    return y - h

def step(ax, x, y, w, h, num, title, desc, color=ACCENT):
    rect = Rectangle((x, y - h), w, h, facecolor=CARD, edgecolor="#334155", linewidth=1, zorder=1)
    ax.add_patch(rect)
    # Numéro
    ax.text(x + 18, y - 18, str(num), fontsize=36, color=color, weight="bold", ha="center", va="top")
    # Titre
    ax.text(x + 50, y - 16, title, fontsize=24, color=WHITE, weight="bold", ha="left", va="top")
    # Description
    ax.text(x + 50, y - 42, desc, fontsize=18, color=MUTED, ha="left", va="top", wrap=True)
    return y - h

def save(fig, name):
    fig.savefig(OUT_DIR / f"{name}.png", facecolor=DARK, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    print(f"[OK] {name}.png")

# ============================================================
# SLIDE TUTORIEL
# ============================================================
fig, ax = new_fig()

ax.text(50, 94, "Comment utiliser Comptable-SLM", fontsize=44, color=ACCENT, weight="bold", ha="center")
ax.text(50, 88, "Guide rapide pour experts-comptables, auditeurs et comptables", fontsize=20, color=MUTED, ha="center")

# Étape 1
step(ax, 10, 80, 80, 22, "1", "Accéder à la démo",
     "Ouvrez https://comptable-slm-1.onrender.com dans votre navigateur\nAucune installation, aucun compte requis — fonctionne immédiatement")

# Étape 2
step(ax, 10, 56, 80, 22, "2", "Poser votre question",
     "Tapez votre question en français naturel dans la zone de chat\nExemples : « Taux TVA Algérie », « Écriture achat TVA 19% », « Différence SARL EURL »")

# Étape 3
step(ax, 10, 32, 80, 22, "3", "Lire la réponse",
     "La réponse s'affiche instantanément avec la source (fichier + section)\nLes montants, comptes, taux et barèmes sont à jour (SCF, loi 07-11, code fiscal 2024)")

# Conseils
card(ax, 10, 8, 80, 24, "[TIPS] Bonnes pratiques", [
    "Utilisez des termes précis : « TVA déductible » > « TVA »",
    "Précisez le contexte : « déclaration TVA mensuelle » > « déclaration »",
    "Si pas de réponse : reformulez ou essayez un synonyme",
    "Les réponses citent leur source — vérifiez si besoin",
], title_color=ACCENT2)

save(fig, "08_tutoriel")
print("\n[OK] Slide tutoriel générée")