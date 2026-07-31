#!/usr/bin/env python3
"""
Génère un dataset Q&A curé (questions naturelles + réponses concises)
à partir des fichiers knowledge_base.
Usage: python generate_qa.py
"""
import json
from pathlib import Path

OUTPUT = "qa_dataset.json"

# Chaque entrée : question utilisateur naturelle, réponse concise
# On génère aussi des variations pour améliorer le matching
QA_PAIRS = [
    # ===== SCF =====
    {
        "question": "Qu'est-ce que le SCF ?",
        "answer": "**SCF — Système Comptable et Financier**\n\nLoi n° 07-11 du 25 novembre 2007 remplaçant le PCN.\n\n**7 classes de comptes :**\n1. Financement permanent\n2. Actif immobilisé\n3. Stocks\n4. Tiers\n5. Trésorerie\n6. Charges\n7. Produits\n\nObjectif : harmoniser avec les normes internationales (IFRS).",
        "tags": "scf systeme comptable financier pcn ifrs classes comptes",
    },
    {
        "question": "Quels sont les principes comptables du SCF ?",
        "answer": "**Principes comptables fondamentaux (SCF) :**\n- **Prudence** : ne pas surévaluer les bénéfices\n- **Permanence des méthodes** : mêmes règles d'un exercice à l'autre\n- **Sincérité** : image fidèle de la situation financière\n- **Continuité d'exploitation** : sauf liquidation\n- **Non-compensation** : actif/passif, charges/produits ne se compensent pas\n- **Coût historique** : évaluation au coût d'origine\n- **Spécialisation des exercices** : rattachement à l'exercice concerné",
        "tags": "principes comptables scf prudence sincérité continuité spécialisation",
    },
    {
        "question": "Qu'est-ce que le plan comptable SCF ?",
        "answer": "**Plan comptable SCF — 9 classes :**\n- **Classe 1** : Comptes de financement permanent\n- **Classe 2** : Comptes d'actif immobilisé\n- **Classe 3** : Comptes de stocks\n- **Classe 4** : Comptes de tiers\n- **Classe 5** : Comptes de trésorerie\n- **Classe 6** : Comptes de charges\n- **Classe 7** : Comptes de produits\n- **Classe 8** : Comptes de résultats\n- **Classe 9** : Comptes de hors-bilan",
        "tags": "plan comptable classes comptes scf nomenclature comptable",
    },
    {
        "question": "Quels sont les documents comptables obligatoires en Algérie ?",
        "answer": "**Documents comptables obligatoires (SCF) :**\n1. **Bilan** : situation patrimoniale (actif/passif)\n2. **Compte de résultat** : charges et produits\n3. **Tableau des flux de trésorerie** (TFT)\n4. **Tableau des variations des capitaux propres** (TVCP)\n5. **Notes aux états financiers** (annexes)\n\nÀ établir à la fin de chaque exercice comptable.",
        "tags": "documents comptables etats financiers bilan resultat tresorerie annexes",
    },

    # ===== TVA =====
    {
        "question": "Quels sont les taux de TVA en Algérie ?",
        "answer": "**Taux de TVA en Algérie :**\n- **19%** — Taux normal (ventes de biens, prestations de services)\n- **9%** — Taux réduit (produits alimentaires, transports, édition, santé)\n- **0%** — Exonérations (exportations, biens d'équipement importés)\n\nSource : Code des impôts algérien",
        "tags": "tva taux 19 9 pourcent normal reduit exoneration",
    },
    {
        "question": "Quels sont les comptes TVA dans le SCF ?",
        "answer": "**Comptes TVA (SCF) :**\n- **4455** — TVA à décaisser (TVA due)\n- **4456** — TVA déductible (TVA sur achats)\n- **4457** — TVA collectée (TVA sur ventes)\n\nCes comptes remplacent les anciens comptes PCN 4421/4422/4426.",
        "tags": "comptes tva 4455 4456 4457 deductible collectee decaisser scf",
    },
    {
        "question": "Comment fonctionne la TVA déductible ?",
        "answer": "**TVA déductible :**\n- Se récupère sur les achats et frais professionnels\n- Compte SCF : **4456 — TVA déductible**\n- Se déduit de la TVA collectée\n- Si TVA déductible > TVA collectée : crédit de TVA reportable\n- Délai de déduction : année d'émission de la facture\n\n**Écriture :**\nDébit 4456 (TVA déductible) / Crédit 401 (Fournisseur) pour le montant de TVA",
        "tags": "tva deductible deduction achat recuperation 4456 credit tva",
    },
    {
        "question": "Comment fonctionne la TVA collectée ?",
        "answer": "**TVA collectée :**\n- Facturée aux clients sur les ventes\n- Compte SCF : **4457 — TVA collectée**\n- Doit être reversée à l'État (après déduction de la TVA déductible)\n- Déclaration mensuelle ou trimestrielle selon le régime\n\n**Écriture :**\nDébit 411 (Client) / Crédit 4457 (TVA collectée) pour le montant de TVA",
        "tags": "tva collectee facture client vente 4457 reversement etat",
    },
    {
        "question": "Comment déclarer la TVA en Algérie ?",
        "answer": "**Déclaration de TVA :**\n- **Mensuelle** : régime général (CA > 1 million DA)\n- **Trimestrielle** : petits contribuables\n- Déclaration avant le **20 du mois suivant**\n- **TVA due** = TVA collectée — TVA déductible\n- Compte 4455 — TVA à décaisser (montant à payer)\n- Paiement par virement bancaire ou CCP",
        "tags": "declaration tva mensuelle trimestrielle date echeance 4455 paiement",
    },
    {
        "question": "Qu'est-ce que la TVA à décaisser ?",
        "answer": "**TVA à décaisser (4455) :**\n- Montant de TVA à reverser à l'État\n- Calcul : TVA collectée (4457) — TVA déductible (4456)\n- Compte de passif (créditeur)\n- Soldé lors du paiement de la déclaration\n\n**Écriture de paiement :**\nDébit 4455 / Crédit 512 (Banque)",
        "tags": "tva a decaisser 4455 passif credit tva due reversement",
    },
    {
        "question": "Quels sont les taux réduits de TVA ?",
        "answer": "**TVA à 9% (taux réduit) :**\n- Produits alimentaires de base\n- Transports terrestres de voyageurs\n- Édition, presse, livres\n- Prestations médicales et paramédicales\n- Produits pharmaceutiques\n- Fourniture d'eau et d'électricité\n\n**TVA à 0% :** exportations et biens d'équipement.",
        "tags": "tva reduit 9 pourcent alimentaire transport edition medical",
    },
    {
        "question": "Comment comptabiliser un achat avec TVA 19% ?",
        "answer": "**Achat avec TVA 19% — Écriture :**\n\nAchat de marchandises : 100 000 DA\nTVA 19% : 19 000 DA\nTotal TTC : 119 000 DA\n\n```\nDébit 60 (Achats)            100 000\nDébit 4456 (TVA déduct.)      19 000\n  Crédit 401 (Fournisseur)           119 000\n```\n\nSource : SCF algérien",
        "tags": "ecriture achat tva comptabilisation fournisseur 60 4456 401",
    },
    {
        "question": "Comment comptabiliser une vente avec TVA ?",
        "answer": "**Vente avec TVA 19% — Écriture :**\n\nVente de marchandises : 100 000 DA\nTVA 19% : 19 000 DA\nTotal TTC : 119 000 DA\n\n```\nDébit 411 (Clients)            119 000\n  Crédit 700 (Ventes)                  100 000\n  Crédit 4457 (TVA collectée)           19 000\n```\n\nSource : SCF algérien",
        "tags": "ecriture vente tva comptabilisation client 411 700 4457",
    },

    # ===== SARL / EURL =====
    {
        "question": "Quelle est la différence entre SARL et EURL ?",
        "answer": "**SARL vs EURL :**\n\n| Critère | SARL | EURL |\n|---------|------|------|\n| Associés | 2 à 50 | 1 seul |\n| Capital min. | 100 000 DA | 100 000 DA |\n| Responsabilité | Limitée aux apports | Limitée aux apports |\n| Gérant | Associé ou tiers | L'associé unique |\n| Régime fiscal | IBS | IBS |\n\nL'EURL est une SARL à associé unique.",
        "tags": "sarl eurl difference associe capital gerant responsabilite",
    },
    {
        "question": "Quel est le capital minimum d'une SARL en Algérie ?",
        "answer": "**Capital minimum SARL : 100 000 DA**\n\n- Apports en numéraire (espèces) ou en nature\n- Apports en industrie interdits\n- Libération : 100% à la constitution pour les apports en numéraire\n- Pas de capital minimum pour EURL (depuis 2022)",
        "tags": "capital minimum sarl 100000 da apport numeraire constitution",
    },
    {
        "question": "Faut-il un commissaire aux comptes pour une SARL ?",
        "answer": "**Commissaire aux comptes en SARL :**\n\n**Obligatoire si :**\n- CA > 10 millions DA\n- Total bilan > 5 millions DA\n- Effectif > 20 salariés\n\n**Facultatif :** en dessous de ces seuils.\n\nNomination par AG ordinaire pour 6 exercices.",
        "tags": "commissaire comptes sarl obligatoire seuil cac nomination",
    },
    {
        "question": "Qu'est-ce qu'une EURL ?",
        "answer": "**EURL — Entreprise Unipersonnelle à Responsabilité Limitée :**\n- 1 associé unique (personne physique ou morale)\n- Capital minimum : 100 000 DA\n- Responsabilité limitée aux apports\n- L'associé unique est le gérant\n- Même régime fiscal et social que la SARL\n- Immatriculation au registre de commerce",
        "tags": "eurl unipersonnelle associe unique entreprise responsabilite limitee",
    },
    {
        "question": "Quelles sont les formalités de création d'une SARL en Algérie ?",
        "answer": "**Création SARL — Étapes :**\n1. Rédaction des statuts (notaire)\n2. Dépôt du capital (banque)\n3. Publication dans un journal d'annonces légales\n4. Immatriculation au registre de commerce (CNRC)\n5. Obtention du numéro d'identification fiscale (NIF)\n6. Affiliation à la CASNOS/CNAS\n\nDélai moyen : 2 à 4 semaines.",
        "tags": "creation sarl formalites statuts notaire cnrc nif casnos",
    },

    # ===== IBS =====
    {
        "question": "Qu'est-ce que l'IBS ?",
        "answer": "**IBS — Impôt sur les Bénéfices des Sociétés :**\n- Impôt direct sur les bénéfices des sociétés\n- Taux : **19%** du résultat fiscal (uniforme depuis 2024)\n- Applicable à toutes les sociétés commerciales (SARL, SPA, SNC, EURL)\n- Déclaration dans les 4 mois suivant la clôture de l'exercice\n- Compte SCF : **4431 — IRG/IBS retenus à la source**",
        "tags": "ibs impot societes benefice taux 19 resultat fiscal",
    },
    {
        "question": "Comment calculer l'IBS ?",
        "answer": "**Calcul de l'IBS :**\n\nRésultat fiscal = Résultat comptable ± Réintégrations ± Déductions\n\n**IBS dû = Résultat fiscal × 19%**\n\n**Acomptes :** 40% du montant dû, versés en 2 fois :\n- 1er acompte : 20 mars\n- 2ème acompte : 20 septembre\n\n**Régularisation :** lors de la déclaration annuelle.",
        "tags": "calcul ibs resultat fiscal acompte declaration regularisation",
    },
    {
        "question": "Qui est assujetti à l'IBS ?",
        "answer": "**Assujettis à l'IBS :**\n- SARL, EURL, SPA, SNC, SCS\n- Sociétés d'économie mixte\n- Établissements publics à caractère commercial\n- Entreprises individuelles (option)\n- Personnes morales étrangères avec établissement stable en Algérie\n\n**Non assujettis :** associations à but non lucratif, services publics.",
        "tags": "assujetti ibs societe commerciale impot personne morale",
    },

    # ===== IRG =====
    {
        "question": "Comment fonctionne l'IRG ?",
        "answer": "**IRG — Impôt sur le Revenu Global :**\n- Impôt progressif sur les revenus des personnes physiques\n- **Retenue à la source** par l'employeur (salaire)\n- **Barème mensuel 2024 :**\n  - **0%** : jusqu'à 30 000 DA\n  - **23%** : 30 001 à 120 000 DA\n  - **27%** : 120 001 à 300 000 DA\n  - **35%** : plus de 300 000 DA\n- Compte SCF : **4431 — IRG retenu à la source**",
        "tags": "irg impot revenu global bareme mensuel retenue source 4431",
    },
    {
        "question": "Comment calculer l'IRG sur salaire ?",
        "answer": "**Calcul IRG sur salaire :**\n1. Salaire brut\n2. Déductions : sécurité sociale (9%), retraite (7%)\n3. Salaire net imposable = Brut — Déductions\n4. Appliquer le barème mensuel :\n   - 0% : 0 à 30 000 DA\n   - 23% : 30 001 à 120 000 DA\n   - 27% : 120 001 à 300 000 DA\n   - 35% : > 300 000 DA\n5. Déduire l'abattement de 10%\n\nCompte : 4431 pour la retenue à reverser au Trésor.",
        "tags": "calcul irg salaire bareme mensuel retenue abattement 4431",
    },
    {
        "question": "Quel est le barème de l'IRG 2024 ?",
        "answer": "**Barème IRG mensuel 2024 :**\n\n| Revenu imposable | Taux |\n|-----------------|------|\n| 0 — 30 000 DA | 0% |\n| 30 001 — 120 000 DA | 23% |\n| 120 001 — 300 000 DA | 27% |\n| > 300 000 DA | 35% |\n\nAbattement de 10% sur le montant de l'IRG calculé.\nCompte : 4431 — IRG retenu à la source.",
        "tags": "bareme irg 2024 taux mensuel abattement 10% 4431",
    },

    # ===== CASNOS =====
    {
        "question": "C'est quoi la CASNOS ?",
        "answer": "**CASNOS — Caisse Nationale de Sécurité Sociale des Non-Salariés :**\n- Pour les travailleurs indépendants, commerçants, artisans, professions libérales\n- **Taux : 15%** du revenu déclaré\n  - 7,5% : Retraite\n  - 7,5% : Assurances sociales (maladie, invalidité)\n- Régimes : Réel, IFU, Simplifié\n- Déclaration et paiement : trimestriel ou annuel",
        "tags": "casnos non salaries independant taux 15 retraite assurance sociale",
    },
    {
        "question": "Quel est le taux CASNOS ?",
        "answer": "**Taux CASNOS : 15%** du revenu déclaré\n\nRépartition :\n- **7,5%** — Retraite\n- **7,5%** — Assurances sociales (maladie, invalidité, décès)\n\nAssiette : revenu professionnel déclaré (plancher/plafond annuels).",
        "tags": "taux casnos 15 pourcent retraite assurance maladie independant",
    },

    # ===== CNAS =====
    {
        "question": "C'est quoi le CNAS ?",
        "answer": "**CNAS — Caisse Nationale d'Assurance Sociale :**\n- Gère les allocations familiales pour les salariés\n- **Taux : 7%** (employeur)\n  - Allocations familiales : 3,5%\n  - Assurance maladie : 2,5%\n  - Retraite : 1%\n- Déclaration mensuelle (CNAS)\n- Compte SCF : 431 — Personnel, rémunérations dues",
        "tags": "cnas allocations familiales salarie taux 7 employeur declaration",
    },
    {
        "question": "Quelle est la différence entre CASNOS et CNAS ?",
        "answer": "**CASNOS vs CNAS :**\n\n| CASNOS | CNAS |\n|--------|------|\n| Non-salariés (indépendants) | Salariés |\n| Taux : 15% | Taux : 7% (employeur) |\n| Retraite + assurances sociales | Allocations familiales + maladie + retraite |\n| Déclaration trimestrielle | Déclaration mensuelle |\n\nLes deux relèvent de la sécurité sociale algérienne.",
        "tags": "difference casnos cnas non salarie salarie taux declaration",
    },
    {
        "question": "Comment déclarer les charges sociales en Algérie ?",
        "answer": "**Déclaration des charges sociales :**\n\n**CNAS (salariés) :**\n- Mensuelle (déclaration + paiement)\n- Taux employeur : 7%\n- Déclaration en ligne via le portail CNAS\n\n**CASNOS (indépendants) :**\n- Trimestrielle ou annuelle\n- Taux : 15% du revenu déclaré\n- Déclaration auprès de la CASNOS de rattachement",
        "tags": "declaration charges sociales cnas casnos mensuelle trimestrielle",
    },

    # ===== AUDIT =====
    {
        "question": "Quelles sont les normes d'audit en Algérie ?",
        "answer": "**Normes d'audit en Algérie :**\n\nLes **ISA (International Standards on Auditing)** sont applicables en Algérie.\n\nPrincipales normes :\n- **ISA 200** : Objectifs généraux de l'auditeur\n- **ISA 210** : Conditions de la mission d'audit\n- **ISA 240** : Responsabilités sur la fraude\n- **ISA 300** : Planification\n- **ISA 500** : Procédures d'audit\n- **ISA 700** : Opinion et rapport d'audit\n\nRéférentiel adopté par le Conseil National de la Comptabilité.",
        "tags": "normes audit isa algerie commissaire comptes referentiel",
    },
    {
        "question": "C'est quoi le commissaire aux comptes ?",
        "answer": "**Commissaire aux Comptes (CAC) :**\n- Professionnel chargé de certifier les comptes annuels\n- Nommé par l'AG pour **6 exercices**\n- Obligatoire pour SARL (CA > 10M DA, bilan > 5M DA, +20 salariés)\n- Obligatoire pour SPA (sans condition)\n- Missions : contrôle, vérification, certification\n- Rédaction d'un rapport annuel à l'AG",
        "tags": "commissaire comptes cac certification rapport audit legal",
    },
    {
        "question": "Quelles sont les obligations du commissaire aux comptes ?",
        "answer": "**Obligations du CAC :**\n1. Vérifier la régularité et la sincérité des comptes\n2. Certifier l'image fidèle des états financiers\n3. Signaler les irrégularités au procureur\n4. Rédiger un rapport annuel à l'AG\n5. Contrôler la paie et les charges sociales\n6. Vérifier la conformité fiscale\n7. Indépendance : ne peut être lié à la société\n\nResponsabilité civile et pénale en cas de manquement.",
        "tags": "obligations commissaire comptes audit certification rapport independance",
    },
    {
        "question": "Qu'est-ce que l'audit interne ?",
        "answer": "**Audit interne :**\n- Fonction exercée au sein de l'entreprise\n- Objectif : évaluer le contrôle interne et la gestion des risques\n- Différent de l'audit externe (CAC)\n- Rapports destinés à la direction\n- Référentiel : normes IIA (Institute of Internal Auditors)\n\nNon obligatoire en Algérie, mais recommandé.",
        "tags": "audit interne controle risques entreprise iia",
    },

    # ===== DROIT / FORMES JURIDIQUES =====
    {
        "question": "Quelles sont les formes juridiques d'entreprise en Algérie ?",
        "answer": "**Formes juridiques en Algérie :**\n\n- **SARL** : 2 à 50 associés, capital 100 000 DA\n- **EURL** : 1 associé, capital 100 000 DA\n- **SNC** : 2+ associés, responsabilité illimitée\n- **SPA** : 7+ actionnaires, capital 1M DA (non cotée) ou 5M DA (cotée)\n- **SCS** : commanditaires + commandités\n\nSource : Code de commerce algérien.",
        "tags": "formes juridiques sarl eurl snc spa societe algerie",
    },
    {
        "question": "Qu'est-ce que la SNC ?",
        "answer": "**SNC — Société en Nom Collectif :**\n- 2 associés minimum\n- **Responsabilité solidaire et illimitée** sur le patrimoine personnel\n- Tous les associés sont commerçants\n- Gérant : associé ou tiers\n- Capital : pas de minimum légal\n- Fiscalité : IBS (ou IRG si option)\n\nMoins courante que la SARL.",
        "tags": "snc societe nom collectif responsabilite illimitee associe",
    },
    {
        "question": "Qu'est-ce que la SPA ?",
        "answer": "**SPA — Société Par Actions :**\n- 7 actionnaires minimum\n- Capital minimum :\n  - 1 000 000 DA (non cotée)\n  - 5 000 000 DA (cotée en bourse)\n- Responsabilité limitée aux apports\n- Conseil d'administration ou directoire\n- Commissaire aux comptes obligatoire\n- Actionnariat ouvert au public possible",
        "tags": "spa societe par actions actionnaire capital conseil administration",
    },
    {
        "question": "Qu'est-ce que le registre de commerce ?",
        "answer": "**Registre du Commerce :**\n- Registre public tenu par le greffe du tribunal\n- Obligatoire pour toute personne physique ou morale exerçant une activité commerciale\n- Contient : identité, activité, siège social, capital\n- Immatriculation au CNRC (Centre National du Registre du Commerce)\n- Renouvellement : annuel\n- Radiation en cas de cessation d'activité",
        "tags": "registre commerce cnrc immatriculation tribunal greffe",
    },
    {
        "question": "Quelles sont les obligations comptables du commerçant ?",
        "answer": "**Obligations comptables du commerçant :**\n1. Tenir une comptabilité régulière et sincère\n2. Livre journal et grand livre\n3. Inventaire annuel\n4. Établir les états financiers (bilan, compte de résultat, TFT)\n5. Archiver les documents : **10 ans**\n6. Déclaration fiscale annuelle\n7. Dépôt des comptes au greffe (pour les sociétés)\n\nSanction : gestion de fait, voire banqueroute.",
        "tags": "obligations comptables commercant livre journal inventaire archive 10 ans",
    },
    {
        "question": "Quels sont les actes de commerce ?",
        "answer": "**Actes de commerce par nature :**\n- Achat pour revente\n- Opérations bancaires et de change\n- Contrats de transport\n- Assurances\n- Actes de sociétés commerciales\n- Lettre de change, billet à ordre\n- Opérations de bourse\n- Construction et vente d'immeubles (acte mixte)",
        "tags": "actes commerce achat revente banque transport assurance lettre change",
    },

    # ===== CHARGES SOCIALES =====
    {
        "question": "Quels sont les congés payés en Algérie ?",
        "answer": "**Congés payés en Algérie :**\n- **Durée** : 30 jours par an (2,5 jours/mois)\n- **Ancienneté** : 6 mois minimum pour y avoir droit\n- **Indemnité** : maintien du salaire\n- **Fractionnement** : possible avec accord employeur\n- **Congé principal** : 15 jours minimum consécutifs\n- Jours fériés et repos hebdomadaire ne sont pas déduits\n\nCode du travail algérien.",
        "tags": "conges payes duree 30 jours indemnite anciennete fractionnement",
    },
    {
        "question": "Quelle est la durée légale du travail en Algérie ?",
        "answer": "**Durée légale du travail :**\n- **40 heures/semaine** (8h/jour)\n- **Heures supplémentaires** : majorées de 25% à 75%\n- Repos hebdomadaire : vendredi (obligatoire)\n- Travail de nuit : majoration de 50%\n- Jours fériés : 14 jours chômés et payés par an",
        "tags": "duree travail 40 heures semaine legale algerie majoration",
    },
    {
        "question": "Quel est le SMIG en Algérie ?",
        "answer": "**SMIG — Salaire Minimum Garanti :**\n- SMIG : **20 000 DA/mois** (depuis 2022)\n- Revalorisé périodiquement par le gouvernement\n- Base de calcul des cotisations sociales\n- S'applique à tous les salariés du secteur privé\n\nSNMG (fonction publique) : barème différent.",
        "tags": "smig salaire minimum 20000 da mensuel revalorisation",
    },
    {
        "question": "Comment fonctionne l'assurance maladie en Algérie ?",
        "answer": "**Assurance Maladie Obligatoire (AMO) :**\n- Gérée par la CNAS pour les salariés\n- Taux : 2,5% (employeur) + 1,5% (salarié)\n- Prise en charge des soins : 80% (taux standard)\n- Carte Chifa : carte électronique de remboursement\n- Affections de longue durée (ALD) : 100%\n- Remboursement : dans les 30 jours suivant le dépôt",
        "tags": "assurance maladie amo cnas soins remboursement chifa",
    },
    {
        "question": "Comment fonctionnent les allocations familiales en Algérie ?",
        "answer": "**Allocations familiales (CNAS) :**\n- Versées aux salariés ayant des enfants à charge\n- Taux : 3,5% (employeur)\n- Montant par enfant :\n  - 1er enfant : 600 DA/mois\n  - 2ème enfant : 600 DA/mois\n  - 3ème enfant et + : 900 DA/mois\n- Versées jusqu'à 18 ans (21 ans si études)\n- Déclaration mensuelle obligatoire",
        "tags": "allocations familiales cnas enfant prime naissance age",
    },

    # ===== GESTION DE LA PAIE =====
    {
        "question": "Comment gérer la paie en Algérie ?",
        "answer": "**Gestion de la paie — Éléments :**\n\n**Éléments du salaire :**\n- Salaire de base\n- Primes et indemnités\n- Heures supplémentaires (majoration 25% à 75%)\n\n**Cotisations :**\n- CNAS : 7% (employeur) + 1,5% (salarié) — allocations familiales\n- Retraite : 7% (salarié) + 7% (employeur)\n- Assurance maladie : 2,5% (employeur) + 1,5% (salarié)\n- IRG : retenue à la source selon barème mensuel\n\n**Comptes SCF :**\n- 421 — Personnel, avances et acomptes\n- 431 — Personnel, rémunérations dues\n- 4431 — IRG retenu à la source",
        "tags": "paie salaire cotisation cnas irg retraite bulletin paie",
    },
    {
        "question": "Qu'est-ce que la taxe professionnelle ?",
        "answer": "**Taxe professionnelle :**\n- Impôt local pesant sur l'exercice d'une activité professionnelle\n- Due par toutes les personnes physiques et morales exerçant une activité\n- Assiette : valeur locative des biens immobiliers utilisés\n- Taux variable selon la commune\n- Déclaration annuelle\n- Paiement : en 2 acomptes\n- Compte SCF : 4421 — Taxe professionnelle",
        "tags": "taxe professionnelle impot local activite assiette declaration",
    },

    # ===== PROCÉDURES PRATIQUES =====
    {
        "question": "Quel est le calendrier fiscal en Algérie ?",
        "answer": "**Calendrier fiscal 2024 — Dates clés :**\n\n| Échéance | Impôt |\n|---------|-------|\n| 20 janvier | TVA mensuelle (décembre) |\n| 20 mars | 1er acompte IBS (40%) |\n| 20 avril | Déclaration IRG annuelle |\n| 30 avril | Déclaration IBS (exercice N-1) |\n| 20 septembre | 2ème acompte IBS (40%) |\n| 20 décembre | TVA mensuelle (novembre) |\n| 31 décembre | Clôture exercice fiscal |",
        "tags": "calendrier fiscal echeance tva ibs irg declaration impot",
    },
    {
        "question": "Comment clôturer un exercice comptable ?",
        "answer": "**Clôture d'exercice — Procédure :**\n1. Inventaire physique des stocks\n2. État des créances et dettes\n3. Rapprochement bancaire\n4. Calcul des amortissements et provisions\n5. Régularisation des comptes de charges et produits\n6. Ajustement des comptes de TVA\n7. Établissement du bilan et du compte de résultat\n8. Paiement de l'IBS (dans les 4 mois)\n9. Dépôt des comptes au greffe (dans les 6 mois)",
        "tags": "cloture exercice inventaire bilan resultat regularisation",
    },
    {
        "question": "Comment faire un rapprochement bancaire ?",
        "answer": "**Rapprochement bancaire :**\n\nObjectif : vérifier la concordance entre le solde comptable (512) et le relevé bancaire.\n\n**Étapes :**\n1. Pointer les écritures communes\n2. Identifier les écarts : chèques non débités, remises non créditées\n3. Ajuster le solde comptable\n4. Lettrage des comptes 512\n\n**Fréquence :** mensuelle.\n\nÉcriture d'ajustement :\nDébit 512 / Crédit 471 (Charges à payer) ou 478 (Produits à recevoir)",
        "tags": "rapprochement bancaire 512 lettrage solde relevet ajustement",
    },
    {
        "question": "Quelles sont les obligations de conservation des documents ?",
        "answer": "**Conservation des documents :**\n\n| Document | Durée |\n|----------|-------|\n| Livres comptables | 10 ans |\n| Pièces justificatives | 10 ans |\n| Bulletins de paie | 5 ans |\n| Contrats de travail | 5 ans après fin |\n| Registre de commerce | 5 ans après radiation |\n| Documents fiscaux | 10 ans |\n\nSupports : papier ou numérique (original scanné).",
        "tags": "conservation documents duree 10 ans archive comptable legale",
    },

    # ===== AMORTISSEMENTS ET PROVISIONS =====
    {
        "question": "Comment comptabiliser un amortissement ?",
        "answer": "**Écriture d'amortissement :**\n\nAmortissement linéaire sur 5 ans, bien 100 000 DA → 20 000 DA/an\n\n```\nDébit 681 (Dotations aux amortissements)    20 000\n  Crédit 28 (Amortissements immobilisations)       20 000\n```\n\n**Modes :** Linéaire, Dégressif, Progressif\n**Durées usuelles :**\n- Constructions : 10-20 ans\n- Matériel : 5-10 ans\n- Véhicules : 5 ans\n- Informatique : 3-5 ans",
        "tags": "amortissement ecriture dotation 681 28 lineaire degressif",
    },
    {
        "question": "Comment comptabiliser une provision ?",
        "answer": "**Écriture de provision pour créances douteuses :**\n\nClient douteux : 50 000 DA, provision 40%\n\n```\nDébit 656 (Charges des provisions)    20 000\n  Crédit 490 (Provisions créances)             20 000\n```\n\n**Types de provisions :**\n- Provisions pour risques (151)\n- Provisions pour charges (153)\n- Provisions pour dépréciation (29, 39, 49, 59)\n\nRévision annuelle obligatoire.",
        "tags": "provision ecriture 656 490 creance douteuse risque depreciation",
    },
]

# Variations supplémentaires pour améliorer le matching
VARIATIONS = {
    "Qu'est-ce que le SCF ?": [
        "SCF explication",
        "Systeme comptable financier algerie",
        "C'est quoi le SCF",
        "Definir le SCF",
    ],
    "Quels sont les taux de TVA en Algérie ?": [
        "TVA taux",
        "Taux TVA algerie",
        "TVA 19%",
        "TVA 9%",
        "Taux de TVA",
        "Quel est le taux de TVA",
    ],
    "Comment fonctionne la TVA déductible ?": [
        "TVA deductible",
        "TVA deductibilite",
        "recuperation TVA",
        "TVA sur achat",
    ],
    "Comment fonctionne la TVA collectée ?": [
        "TVA collectee",
        "TVA sur ventes",
        "TVA facture client",
    ],
    "Comment déclarer la TVA en Algérie ?": [
        "declaration TVA",
        "declarer la TVA",
        "TVA declaration echeance",
        "declaration mensuelle TVA",
    ],
    "Quelle est la différence entre SARL et EURL ?": [
        "Difference SARL EURL",
        "SARL ou EURL",
        "Choix SARL EURL",
    ],
    "Qu'est-ce que l'IBS ?": [
        "IBS impot societe",
        "Impot sur les benefices",
        "Taux IBS",
    ],
    "Comment fonctionne l'IRG ?": [
        "IRG impot revenu",
        "retenue source IRG",
        "Bareme IRG",
    ],
    "Quel est le barème de l'IRG 2024 ?": [
        "bareme IRG 2024",
        "IRG bareme mensuel",
        "tranches IRG",
    ],
    "C'est quoi la CASNOS ?": [
        "CASNOS non salarie",
        "CASNOS taux",
        "Assurance independant",
    ],
    "C'est quoi le CNAS ?": [
        "CNAS salarie",
        "CNAS declaration",
        "Allocations familiales",
    ],
    "Quelle est la différence entre CASNOS et CNAS ?": [
        "difference CASNOS CNAS",
        "CASNAS ou CNAS",
        "non salarie salarie securite sociale",
    ],
    "Quels sont les comptes TVA dans le SCF ?": [
        "Comptes TVA",
        "4455 4456 4457",
        "Comptabilite TVA",
    ],
    "Comment comptabiliser un achat avec TVA 19% ?": [
        "Ecriture achat TVA",
        "Comptabiliser achat",
        "Achat fournisseur TVA",
    ],
    "Comment comptabiliser une vente avec TVA ?": [
        "Ecriture vente TVA",
        "Comptabiliser vente",
        "Vente client TVA",
    ],
    "Quelles sont les formes juridiques en Algérie ?": [
        "Formes societe algerie",
        "Types societe",
        "SARL SPA SNC",
    ],
    "Quels sont les congés payés en Algérie ?": [
        "conges payes",
        "duree conges",
        "combien de conges payes",
        "30 jours conges",
    ],
    "Comment fonctionne l'assurance maladie en Algérie ?": [
        "assurance maladie",
        "couverture sociale",
        "remboursement soins",
        "carte chifa",
    ],
    "Quels sont les documents comptables obligatoires en Algérie ?": [
        "bilan comptable",
        "etats financiers",
        "documents comptables",
        "compte de resultat",
    ],
    "Comment gérer la paie en Algérie ?": [
        "paie",
        "gestion paie",
        "bulletin salaire",
        "element salaire",
    ],
    "Qu'est-ce que la taxe professionnelle ?": [
        "taxe professionnelle",
        "taxe professionnel",
        "taxe activite",
    ],
    "Comment clôturer un exercice comptable ?": [
        "cloture exercice",
        "fin d exercice comptable",
        "procedure cloture",
    ],
}

# Ajouter les variations au dataset
def generate_dataset():
    seen_questions = set()
    dataset = []

    for pair in QA_PAIRS:
        q = pair["question"]
        if q not in seen_questions:
            seen_questions.add(q.lower())
            dataset.append({
                "question": q,
                "answer": pair["answer"],
                "tags": pair["tags"],
            })

        # Ajouter les variations
        if q in VARIATIONS:
            for v in VARIATIONS[q]:
                v_lower = v.lower()
                if v_lower not in seen_questions:
                    seen_questions.add(v_lower)
                    dataset.append({
                        "question": v,
                        "answer": pair["answer"],
                        "tags": pair["tags"],
                    })

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"Dataset généré : {len(dataset)} questions ({OUTPUT})")

if __name__ == "__main__":
    generate_dataset()
