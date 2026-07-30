#!/usr/bin/env python3
"""
Comptable-SLM Demo — Assistant IA pour la comptabilité algérienne.

Usage:
    python comptable_demo.py

Prérequis:
    pip install gradio python-dotenv
    Fichier .env avec NVIDIA_API_KEY ou Ollama local
"""

import os
import sys
import gradio as gr
from pathlib import Path

# Ajouter le dossier du projet au PATH
sys.path.insert(0, str(Path(__file__).parent))
from rag_pipeline import RAGPipeline

# Exemples de questions pour la démo
EXAMPLES = [
    "Quels sont les taux de TVA en Algérie ?",
    "Quelle est la différence entre SARL et EURL ?",
    "Comment comptabiliser un achat avec TVA 19% ?",
    "Qu'est-ce que le SCF ?",
    "Quels sont les taux de charges sociales CNAS et CASNOS ?",
    "Qu'est-ce que l'IBS en Algérie ?",
    "Comment fonctionne la retenue à la source IRG ?",
    "Quelles sont les obligations comptables d'une EURL ?",
]

WELCOME = """# 🇩🇿 Comptable-SLM
### Assistant IA pour la comptabilité et l'audit algériens

Posez une question sur le SCF, la fiscalité algérienne, les charges sociales, 
le droit des sociétés, ou les écritures comptables.

**Exemples de questions** : cliquez sur un exemple ci-dessous ⬇️
"""


def init_pipeline():
    try:
        p = RAGPipeline()
        return p
    except Exception as e:
        print(f"Erreur d'initialisation : {e}")
        return None


def answer_question(question, history):
    if not question.strip():
        return history

    p = init_pipeline()
    if p is None:
        history.append((question, "❌ Erreur : impossible d'initialiser le pipeline. Vérifiez votre .env"))
        return history

    try:
        result = p.query(question)
        answer = result["answer"]
        sources = result.get("sources", [])

        # Ajouter les sources
        if sources:
            answer += "\n\n📚 **Sources :**\n"
            seen = set()
            for s in sources:
                source = s.get("source", "Inconnu")
                if source not in seen:
                    seen.add(source)
                    title = s.get("title", "")
                    answer += f"- `{source}` — {title}\n"

        history.append((question, answer))
    except Exception as e:
        history.append((question, f"❌ Erreur : {str(e)}"))

    return history


def create_interface():
    with gr.Blocks(
        title="Comptable-SLM Demo",
        theme=gr.themes.Soft(primary_hue="blue", secondary_hue="emerald"),
        css=".gradio-container { max-width: 900px !important; margin: auto; } footer { display: none !important; }"
    ) as demo:
        gr.Markdown(WELCOME)

        chatbot = gr.Chatbot(
            label="Comptable-SLM",
            height=450,
            bubble_full_width=False,
            avatar_images=(None, "🧾"),
        )

        with gr.Row():
            msg = gr.Textbox(
                label="Votre question",
                placeholder="Ex: Quels sont les taux de TVA en Algérie ?",
                scale=4,
                container=True,
            )
            send_btn = gr.Button("Envoyer", variant="primary", scale=1)

        gr.Examples(
            examples=EXAMPLES,
            inputs=msg,
            label="💡 Questions suggérées",
        )

        with gr.Row():
            clear_btn = gr.Button("🔄 Nouvelle conversation", variant="secondary", size="sm")
            gr.Markdown(
                "**💡 Pro tip** : Configurez `USE_LOCAL_LLM=true` dans `.env` "
                "pour utiliser Ollama (hors ligne)"
            )

        # Gestion des événements
        def user_and_respond(text, history):
            if not text.strip():
                return "", history
            p = init_pipeline()
            if p is None:
                history.append((text, "Erreur : impossible d'initialiser le pipeline. Verifiez votre .env"))
                return "", history
            try:
                result = p.query(text)
                answer = result["answer"]
                sources = result.get("sources", [])
                if sources:
                    answer += "\n\nSources :\n"
                    seen = set()
                    for s in sources:
                        src = s.get("source", "Inconnu")
                        if src not in seen:
                            seen.add(src)
                            answer += f"- {src} — {s.get('title', '')}\n"
                history.append((text, answer))
            except Exception as e:
                history.append((text, f"Erreur : {str(e)}"))
            return "", history

        msg.submit(user_and_respond, [msg, chatbot], [msg, chatbot])
        send_btn.click(user_and_respond, [msg, chatbot], [msg, chatbot])
        clear_btn.click(lambda: ("", []), None, [msg, chatbot], queue=False)

    return demo


if __name__ == "__main__":
    print("=" * 50)
    print("  Comptable-SLM Demo")
    print("  Assistant IA - Comptabilité Algérienne")
    print("=" * 50)
    print("\nDémarrage de l'interface...")
    print("Ouvrez http://127.0.0.1:7860 dans votre navigateur\n")

    demo = create_interface()
    demo.launch(share=True, server_name="0.0.0.0")
