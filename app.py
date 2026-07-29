#!/usr/bin/env python3
"""
Comptable-SLM Demo — Version autonome
Assistant IA pour la comptabilite algerienne
"""

import gradio as gr

ANSWERS = {
    "tva": (
        "**Taux de TVA en Algérie :**\n\n"
        "- **19%** - Taux normal (ventes de biens, prestations de services)\n"
        "- **9%** - Taux reduit (produits alimentaires, transports, edition)\n"
        "- **0%** - Exonerations (exportations, biens d'equipement)\n\n"
        "Reference : Code des impots algerien"
    ),
    "sarl": (
        "**SARL vs EURL**\n\n"
        "**SARL :** 2 a 50 associes, capital 100 000 DA\n"
        "**EURL :** 1 seul associe, meme regime que SARL\n\n"
        "Source : Code de commerce algerien"
    ),
    "scf": (
        "**SCF - Systeme Comptable et Financier**\n\n"
        "Loi n 07-11 du 25 novembre 2007\n\n"
        "7 classes :\n"
        "1. Financement permanent\n"
        "2. Actif immobilise\n"
        "3. Stocks\n"
        "4. Tiers\n"
        "5. Tresorerie\n"
        "6. Charges\n"
        "7. Produits"
    ),
    "ecriture": (
        "**Achat avec TVA 19%**\n"
        "Achat 100 000 DA + TVA 19 000 DA\n\n"
        "  Debit 60 (Achats)          100 000\n"
        "  Debit 4456 (TVA deduct.)    19 000\n"
        "  Credit 401 (Fournisseur)           119 000\n\n"
        "Reference : SCF algerien"
    ),
    "casnos": (
        "**CASNOS - Non-Salaries**\n\n"
        "Taux : 15% du revenu declare\n"
        "- 7,5% Retraite\n"
        "- 7,5% Assurances sociales\n\n"
        "Regimes : Reel, IFU, Simplifie"
    ),
    "ibs": (
        "**IBS - Impot sur les Benefices**\n\n"
        "Taux normal : 26%\n"
        "Taux reduit : 19% (production)\n\n"
        "Source : Code des impots"
    ),
    "irg": (
        "**IRG - Retenue a la source**\n\n"
        "Bareme mensuel :\n"
        "- 0% : jusqu'a 30 000 DA\n"
        "- 23% : 30 001 a 120 000 DA\n"
        "- 27% : 120 001 a 300 000 DA\n"
        "- 35% : plus de 300 000 DA\n\n"
        "Compte : 4431 IRG retenu a la source"
    ),
    "droit": (
        "**Formes juridiques en Algerie**\n\n"
        "- **SARL** : 2 a 50 associes\n"
        "- **EURL** : 1 associe\n"
        "- **SNC** : responsabilite illimitee\n"
        "- **SPA** : 7+ actionnaires\n\n"
        "Source : Code de commerce"
    ),
}


def find_answer(message):
    q = message.lower().strip()
    if not q:
        return "Posez une question sur la comptabilite algerienne."
    for kw, key in [
        ("tva", "tva"), ("sarl", "sarl"), ("eurl", "sarl"),
        ("scf", "scf"), ("ecritur", "ecriture"), ("comptabilis", "ecriture"),
        ("achat", "ecriture"), ("casnos", "casnos"), ("ibs", "ibs"),
        ("irg", "irg"), ("societe", "droit"), ("spa", "droit"),
        ("snc", "droit"), ("forme juridique", "droit"),
    ]:
        if kw in q:
            return ANSWERS[key]
    return (
        "Je ne connais pas encore cette question.\n\n"
        "Essayez : TVA, SARL, EURL, SCF, ecritures, CASNOS, IBS, IRG, "
        "formes juridiques."
    )


WELCOME = """# Comptable-SLM
### Assistant IA pour la comptabilite algerienne

Posez une question sur le SCF, la TVA, les charges sociales ou le droit des societes.
"""

EXAMPLES = [
    ["Quels sont les taux de TVA en Algerie ?"],
    ["Difference entre SARL et EURL ?"],
    ["Qu'est-ce que le SCF ?"],
    ["Comptabiliser un achat avec TVA 19%"],
    ["C'est quoi la CASNOS ?"],
    ["Qu'est-ce que l'IBS ?"],
    ["Comment fonctionne l'IRG ?"],
    ["Formes juridiques en Algerie ?"],
]


def chat(message, history):
    if not message or not message.strip():
        return "Posez une question sur la comptabilite algerienne."
    try:
        return find_answer(message)
    except Exception as e:
        return f"Erreur : {str(e)}"


demo = gr.ChatInterface(
    fn=chat,
    title="Comptable-SLM",
    description=WELCOME,
    examples=[[e[0]] for e in EXAMPLES],
    theme="soft",
)

if __name__ == "__main__":
    import os, socket
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
