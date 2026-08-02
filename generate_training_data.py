"""Generate additional training data from enriched knowledge base files."""
import json
import os
import re

SYSTEM_PROMPT = (
    "Tu es un expert-comptable et auditeur algérien. "
    "Tu réponds de manière précise, professionnelle et détaillée aux questions "
    "comptables, fiscales, d'audit et de droit commercial. "
    "Tu utilises le Plan Comptable National (SCF) algérien et la terminologie "
    "professionnelle algérienne. Tu connais parfaitement la fiscalité algérienne "
    "(IBS, TVA, IRG, taxe professionnelle) et les spécificités du cadre juridique "
    "et bancaire algérien."
)

KB_DIR = "knowledge_base"
OUTPUT_FILE = "comptable_dataset_algerien.jsonl"


def load_existing_examples(path):
    examples = set()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    q = data["messages"][1]["content"]
                    examples.add(q.strip().lower())
                except (json.JSONDecodeError, IndexError, KeyError):
                    continue
    return examples


def extract_sections(text, filename):
    sections = []
    current_section = ""
    current_content = []
    lines = text.split("\n")

    for line in lines:
        if re.match(r'^#{1,3}\s+', line):
            if current_section and current_content:
                content = "\n".join(current_content).strip()
                if content and len(content) > 50:
                    sections.append((current_section, content))
            current_section = re.sub(r'^#{1,3}\s+', '', line).strip()
            current_content = []
        else:
            current_content.append(line)

    if current_section and current_content:
        content = "\n".join(current_content).strip()
        if content and len(content) > 50:
            sections.append((current_section, content))

    return sections


def generate_qa_from_section(title, content, filename):
    qa_pairs = []
    title_lower = title.lower()

    if any(kw in title_lower for kw in ["compte", "classe", "plan comptable"]):
        qa_pairs.extend(generate_accounting_qa(title, content))
    elif any(kw in title_lower for kw in ["fiscal", "impôt", "ibs", "tva", "irg"]):
        qa_pairs.extend(generate_tax_qa(title, content))
    elif any(kw in title_lower for kw in ["audit", "contrôle", "norme"]):
        qa_pairs.extend(generate_audit_qa(title, content))
    elif any(kw in title_lower for kw in ["banque", "crédit", "paiement"]):
        qa_pairs.extend(generate_banking_qa(title, content))

    return qa_pairs


def generate_accounting_qa(title, content):
    qa = []
    if "classe 1" in title.lower():
        qa.append({
            "q": "Quels sont les comptes de la classe 1 du SCF algérien ?",
            "a": "La classe 1 comprend les comptes de financement permanent :\n- 10 : Capital social\n- 11 : Réserves\n- 12 : Résultats (bénéfice ou perte)\n- 13 : Subventions d'investissement\n- 14 : Provisions réglementées\n- 15 : Emprunts et dettes assimilées\n- 16 : Comptes de liaison des établissements"
        })
    elif "classe 2" in title.lower():
        qa.append({
            "q": "Quels sont les comptes de la classe 2 du SCF algérien ?",
            "a": "La classe 2 comprend les comptes d'actif immobilisé :\n- 20 : Immobilisations incorporelles (fonds de commerce, brevets, logiciels)\n- 21 : Immobilisations corporelles (terrains, constructions, matériel)\n- 22 : Immobilisations mises en concession\n- 23 : Immobilisations en cours\n- 24 : Immobilisations financières (prêts, participations)\n- 25 : Écarts de conversion"
        })
    elif "classe 3" in title.lower():
        qa.append({
            "q": "Quels sont les comptes de la classe 3 du SCF algérien ?",
            "a": "La classe 3 comprend les comptes de stocks :\n- 30 : Stocks de marchandises\n- 31 : Matières premières\n- 32 : Autres approvisionnements\n- 33 : En-cours de production\n- 34 : Produits intermédiaires\n- 35 : Produits finis"
        })
    elif "classe 4" in title.lower():
        qa.append({
            "q": "Quels sont les comptes de la classe 4 du SCF algérien ?",
            "a": "La classe 4 comprend les comptes de tiers :\n- 40 : Fournisseurs et comptes rattachés\n- 41 : Clients et comptes rattachés\n- 42 : Personnel\n- 43 : Organismes sociaux (CNAS, CASNOS)\n- 44 : État et collectivités publiques\n- 45 : Autres créanciers et débiteurs\n- 47 : Comptes d'attente\n- 48 : Charges et produits constatés d'avance"
        })
    elif "classe 5" in title.lower():
        qa.append({
            "q": "Quels sont les comptes de la classe 5 du SCF algérien ?",
            "a": "La classe 5 comprend les comptes de trésorerie :\n- 50 : Titres de placement\n- 52 : Banques et établissements financiers (CNEP, BADR, BEA, BNA, CPA)\n- 53 : Caisse\n- 54 : Régies d'avance et accréditifs"
        })
    elif "classe 6" in title.lower():
        qa.append({
            "q": "Quels sont les comptes de la classe 6 du SCF algérien ?",
            "a": "La classe 6 comprend les comptes de charges :\n- 60 : Achats\n- 61 : Services extérieurs\n- 62 : Autres services extérieurs\n- 63 : Charges de personnel\n- 64 : Charges sociales\n- 65 : Autres charges courantes\n- 66 : Charges financières\n- 67 : Charges exceptionnelles\n- 68 : Dotations aux amortissements et provisions"
        })
    elif "classe 7" in title.lower():
        qa.append({
            "q": "Quels sont les comptes de la classe 7 du SCF algérien ?",
            "a": "La classe 7 comprend les comptes de produits :\n- 70 : Ventes de marchandises et de produits fabriqués\n- 71 : Production vendue (biens et services)\n- 72 : Production stockée\n- 73 : Production immobilisée\n- 74 : Subventions d'exploitation\n- 76 : Produits financiers\n- 77 : Produits exceptionnels\n- 78 : Reprises sur provisions et amortissements"
        })

    return qa


def generate_tax_qa(title, content):
    qa = []
    if "ibs" in title.lower() or "sociétés" in title.lower():
        qa.append({
            "q": "Quel est le taux de l'Impôt sur les Sociétés (IBS) en Algérie ?",
            "a": "En Algérie, l'IBS est fixé à 19% du bénéfice net. Ce taux est applicable à l'ensemble des sociétés quel que soit leur chiffre d'affaires. Contrairement à la France, il n'existe pas de taux réduit pour les petites entreprises. Le bénéfice net est déterminé à partir du résultat comptable, ajusté par les réintégrations et déductions fiscales."
        })
    elif "tva" in title.lower():
        qa.append({
            "q": "Quels sont les taux de TVA en Algérie ?",
            "a": "L'Algérie applique 3 taux de TVA :\n- Taux normal : 19% (taux de droit commun)\n- Taux réduit : 9% (produits de première nécessité, médicaments, livres, transports)\n- Taux zéro : 0% (exportations de biens et services)\nLa TVA est déclarée mensuellement ou trimestriellement selon le régime de l'entreprise."
        })
    elif "irg" in title.lower() or "revenu" in title.lower():
        qa.append({
            "q": "Qu'est-ce que l'IRG en Algérie ?",
            "a": "L'IRG (Impôt sur le Revenu Global) est l'impôt sur le revenu des personnes physiques en Algérie. Il est retenu à la source sur les salaires selon un barème progressif :\n- Jusqu'à 120 000 DA : 0%\n- De 120 001 à 300 000 DA : 20%\n- De 300 001 à 600 000 DA : 30%\n- De 600 001 à 1 200 000 DA : 35%\n- Au-delà de 1 200 000 DA : 40%"
        })
    elif "retenue" in title.lower():
        qa.append({
            "q": "Qu'est-ce que la retenue à la source en Algérie ?",
            "a": "La retenue à la source est un mécanisme par lequel l'entreprise retient un pourcentage sur les paiements effectués à des tiers. Les principaux taux sont :\n- Honoraires et prestations de services : 20%\n- Locations meublées : 10%\n- Commissions et courtages : 15%\n- Droits d'auteur : 10%\nLa retenue est versée mensuellement à l'administration fiscale."
        })
    elif "contrôle" in title.lower():
        qa.append({
            "q": "Comment fonctionne le contrôle fiscal en Algérie ?",
            "a": "Le contrôle fiscal en Algérie peut être :\n- Contrôle sur pièces : vérification des déclarations au bureau\n- Contrôle sur place : vérification dans les locaux de l'entreprise\n- Vérification de la comptabilité : examination des livres et documents\nLe contribuable a le droit de se faire assister par un mandataire. Le délai de reprise est de 4 ans à compter de la déclaration."
        })

    return qa


def generate_audit_qa(title, content):
    qa = []
    if "contrôle interne" in title.lower():
        qa.append({
            "q": "Qu'est-ce que le contrôle interne en audit ?",
            "a": "Le contrôle interne est l'ensemble des dispositifs mis en place par la direction d'une entreprise pour atteindre ses objectifs : fiabilité des informations financières, efficacité des opérations, conformité aux lois. Il comprend 5 composantes : environnement de contrôle, évaluation des risques, activités de contrôle, information et communication, et pilotage."
        })
    elif "matérialité" in title.lower():
        qa.append({
            "q": "Qu'est-ce que la matérialité en audit ?",
            "a": "La matérialité est le seuil au-delà duquel une erreur ou omission dans les états financiers peut influencer les décisions des utilisateurs. L'auditeur détermine un seuil de matérialité (souvent 5-10% du résultat net ou 0,5-1% du CA). Les anomalies supérieures à ce seuil sont considérées comme significatives."
        })
    elif "opinion" in title.lower() or "commissaire" in title.lower():
        qa.append({
            "q": "Quels sont les types d'opinion du commissaire aux comptes en Algérie ?",
            "a": "Le commissaire aux comptes peut émettre 4 types d'opinion :\n1) Opinion sans réserve : les comptes sont réguliers et sincères\n2) Opinion avec réserve : des réserves portent sur des éléments déterminants\n3) Avis défavorable : les comptes ne sont pas réguliers ou sincères\n4) Abstention d'opinion : l'auditeur n'a pas pu se procurer les éléments nécessaires"
        })
    elif "risque" in title.lower():
        qa.append({
            "q": "Quels sont les risques d'audit ?",
            "a": "Les principaux risques d'audit sont :\n1) Risque de non-détectabilité : risque que l'auditeur ne détecte pas les anomalies\n2) Risque inhérent : risque que les comptes contiennent des anomalies significatives\n3) Risque de contrôle : risque que le contrôle interne ne prévienne pas les anomalies\nLe risque d'audit = risque inhérent × risque de contrôle × risque de non-détectabilité"
        })

    return qa


def generate_banking_qa(title, content):
    qa = []
    if "banque" in title.lower() and "principales" in title.lower():
        qa.append({
            "q": "Quelles sont les principales banques en Algérie ?",
            "a": "Les principales banques en Algérie :\n- CNEP (Caisse Nationale d'Épargne et de Prévoyance)\n- BADR (Banque de l'Agriculture et du Développement Rural)\n- BEA (Banque Extérieure d'Algérie)\n- BNA (Banque Nationale d'Algérie)\n- CPA (Crédit Populaire d'Algérie)\n- Société Générale Algérie\n- Banque Algeria"
        })
    elif "paiement" in title.lower():
        qa.append({
            "q": "Quels sont les modes de paiement en Algérie ?",
            "a": "Les principaux modes de paiement :\n- Chèque : écrit donnant l'ordre à la banque de payer\n- Virement bancaire : transfert de fonds entre comptes\n- Lettre de change : effet de commerce à échéance\n- Espèces : paiement en liquide (limité à 100 000 DA)\n- Carte bancaire : paiement électronique"
        })
    elif "crédit" in title.lower():
        qa.append({
            "q": "Comment fonctionne un crédit bancaire en Algérie ?",
            "a": "Un crédit bancaire est un prêt accordé par une banque à un emprunteur. Les conditions sont :\n- Taux d'intérêt : fixe ou variable\n- Durée : selon le type de crédit\n- Garanties : hypothèque, caution, nantissement\n- Remboursement : mensualités constantes ou variables\nLe crédit peut être à court, moyen ou long terme."
        })
    elif "rapprochement" in title.lower():
        qa.append({
            "q": "Comment fonctionne le rapprochement bancaire ?",
            "a": "Le rapprochement bancaire consiste à comparer le compte 521 (Banque) du journal de caisse avec le relevé bancaire. Les écarts sont dus à :\n- Chèques émis non encore présentés\n- Virements non encore comptabilisés\n- Frais bancaires non encore enregistrés\nIl doit être effectué mensuellement."
        })

    return qa


def generate_diverse_qa():
    diverse = []
    kb_files = read_knowledge_base_files()
    existing = load_existing_examples(OUTPUT_FILE)

    for filename, content in kb_files.items():
        if "08_droit_fiscal_avance" in filename:
            diverse.extend([
                {"q": "Quels sont les avantages fiscaux pour les zones de développement durable en Algérie ?",
                 "a": "Les entreprises implantées en zones de développement durable bénéficient d'une exonération totale d'IBS pendant 5 ans, puis d'un taux réduit de 50% les 5 années suivantes. Cette mesure vise à encourager l'investissement dans les régions en retard de développement."},
                {"q": "Comment fonctionne la taxe sur les transactions financières en Algérie ?",
                 "a": "La taxe sur les transactions financières est prélevée sur les opérations bancaires. Le taux est de 0,1% sur les virements et chèques. Elle est déductible du résultat fiscal."},
                {"q": "Qu'est-ce que le régime fiscal des entreprises publiques en Algérie ?",
                 "a": "Les entreprises publiques sont soumises à l'IBS au taux de 19%, comme les entreprises privées. Elles bénéficient cependant de certaines exonérations temporaires pour les investissements publics."},
                {"q": "Comment calculer la pénalité de retard fiscale en Algérie ?",
                 "a": "La pénalité de retard est de 0,2% par mois de retard sur le montant de l'impôt dû. Elle s'ajoute à l'amende pour retard de déclaration qui est de 10% du montant de l'impôt."},
                {"q": "Quels sont les seuils de chiffre d'affaires pour la TVA en Algérie ?",
                 "a": "Les seuils de franchise de TVA en Algérie sont :\n- Taux normal : obligatoire pour tous les assujettis\n- Franchise : pour les entreprises dont le CA est inférieur à un certain seuil (révisé annuellement)\n- Les seuils varient selon l'activité (commerciale, industrielle, de services)."},
                {"q": "Qu'est-ce que l'optimisation fiscale en Algérie ?",
                 "a": "L'optimisation fiscale consiste à organiser ses affaires de manière à réduire légalement la charge fiscale. En Algérie, elle comprend : le choix du statut juridique, l'utilisation des incitations fiscales, la planification des investissements, et la gestion du BFR fiscal."},
                {"q": "Comment fonctionne le crédit d'impôt recherche en Algérie ?",
                 "a": "Le crédit d'impôt recherche permet de déduire une partie des dépenses de R&D de l'impôt dû. En Algérie, les entreprises peuvent bénéficier d'un crédit d'impôt pour les dépenses de recherche et développement, avec un taux pouvant atteindre 30% des dépenses éligibles."},
                {"q": "Quelles sont les obligations fiscales des entreprises nouvellement créées ?",
                 "a": "Les entreprises nouvellement créées doivent :\n- S'inscrire à la DGI dans les 30 jours\n- Déclarer la TVA mensuellement les 2 premières années\n- Souscrire la déclaration du résultat fiscal annuellement\n- Bénéficier de l'exonération d'IBS pendant 3 ans"},
                {"q": "Comment fonctionne la TVA sur les prestations de services transfrontalières ?",
                 "a": "Les prestations de services transfrontalières sont soumises à des règles spécifiques :\n- Services exportés : exonération de TVA\n- Services importés : auto-liquidation de la TVA\n- Règle du lieu de consommation pour certains services"},
                {"q": "Qu'est-ce que la convention fiscale algérienne ?",
                 "a": "L'Algérie a conclu des conventions fiscales avec plusieurs pays pour éviter la double imposition. Ces conventions déterminent quel pays a le droit d'imposer les revenus et prévoient des taux réduits de retenue à la source."},
            ])
        elif "09_comptabilite_bancaire" in filename:
            diverse.extend([
                {"q": "Qu'est-ce qu'un crédit documentaire en Algérie ?",
                 "a": "Le crédit documentaire est un engagement bancaire de payer le bénéficiaire (exportateur) contre remise de documents conformes. Il garantit au vendeur le paiement et à l'acheteur la réception des marchandises. Il est utilisé principalement dans le commerce international."},
                {"q": "Comment fonctionne l'escompte commercial en Algérie ?",
                 "a": "L'escompte commercial est une opération par laquelle une banque avance le montant d'un effet de commerce avant son échéance. L'entreprise cède son effet à la banque qui lui verse le montant diminué des agios. Les agios sont calculés en fonction du taux d'escompte et du nombre de jours restant avant l'échéance."},
                {"q": "Quelles sont les garanties bancaires en Algérie ?",
                 "a": "Les principales garanties bancaires :\n- Caution bancaire : engagement de payer en cas de défaillance\n- Hypothèque : garantie immobilière\n- Nantissement : garantie sur des biens mobiliers\n- Privilège : droit de préférence sur certains biens\nLes garanties sont demandées lors de l'octroi de crédits."},
                {"q": "Comment fonctionne la facilité de caisse en Algérie ?",
                 "a": "La facilité de caisse est un découvert bancaire autorisé. Elle permet à l'entreprise de maintenir un solde débiteur sur son compte courant dans la limite d'un montant préalablement agréé. Les agios sont calculés sur le montant utilisé et la durée du découvert."},
                {"q": "Quels sont les types de comptes bancaires en Algérie ?",
                 "a": "Les principaux types de comptes :\n- Compte courant : pour les opérations courantes\n- Compte d'épargne : pour constituer une épargne\n- Compte à terme : pour un placement à durée déterminée\n- Compte professionnel : pour les entreprises\nChaque compte a ses spécificités en termes de frais et de services."},
                {"q": "Comment fonctionne le change en Algérie ?",
                 "a": "Le change est soumis à la réglementation du Bank of Algeria. Les opérations de change comprennent :\n- Change au comptant : achat/vente de devises immédiat\n- Change à terme : achat/vente de devises à une date future\n- Couverture de change : protection contre les variations de change"},
                {"q": "Qu'est-ce que la compensation bancaire en Algérie ?",
                 "a": "La compensation bancaire est un système centralisé qui permet de régler les créances et dettes entre banques. Les chèques et effets de commerce sont compensés automatiquement entre les établissements bancaires. Elle permet de réduire les transferts de fonds et de sécuriser les paiements."},
                {"q": "Comment fonctionne le financement commercial en Algérie ?",
                 "a": "Le financement commercial comprend les crédits accordés par les fournisseurs à leurs clients. Il peut prendre la forme de :\n- Délais de paiement : 30, 60 ou 90 jours\n- Escomptes de paiement anticipé\n- Crédit documentaire\nLe financement commercial est un élément important du BFR."},
                {"q": "Qu'est-ce que le leasing en Algérie ?",
                 "a": "Le leasing (location-vente) est un contrat par lequel une banque finance l'acquisition d'un bien pour le louer à l'entreprise. À l'issue du contrat, l'entreprise peut acquérir le bien à un prix résiduel. Le leasing est soumis à la réglementation bancaire algérienne."},
                {"q": "Comment fonctionne l'affacturage (factoring) en Algérie ?",
                 "a": "L'affacturage est une technique de financement par laquelle une entreprise cède ses créances clients à une société de factoring. Cette dernière avance le montant des factures et prend en charge le recouvrement. L'affacturage améliore le BFR de l'entreprise."},
            ])
        elif "10_audit_systeme_info" in filename:
            diverse.extend([
                {"q": "Qu'est-ce que l'audit des systèmes d'information en Algérie ?",
                 "a": "L'audit des SI est une évaluation indépendante des systèmes informatiques de l'entreprise. Il vérifie la sécurité, la performance, la conformité et l'efficacité des technologies de l'information. Il comprend l'audit des applications, des infrastructures et des processus IT."},
                {"q": "Quels sont les risques liés aux systèmes d'information ?",
                 "a": "Les principaux risques IT :\n- Risque de sécurité : accès non autorisé, virus, piratage\n- Risque de disponibilité : panne, interruption de service\n- Risque de données : perte, corruption, erreur\n- Risque de conformité : non-respect des réglementations\n- Risque opérationnel : erreurs humaines, défaillances processus"},
                {"q": "Comment auditer la sécurité informatique en Algérie ?",
                 "a": "L'audit de sécurité IT comprend :\n- Évaluation des politiques de sécurité\n- Test d'intrusion et analyse de vulnérabilité\n- Vérification des contrôles d'accès\n- Audit des sauvegardes et plans de reprise\n- Revue des procédures de gestion des incidents"},
                {"q": "Qu'est-ce que la norme ISO 27001 en Algérie ?",
                 "a": "ISO 27001 est la norme internationale pour les systèmes de management de la sécurité de l'information (SMSI). Elle définit les exigences pour établir, mettre en œuvre, maintenir et améliorer un SMSI. L'audit de certification vérifie la conformité aux exigences de la norme."},
                {"q": "Comment mesurer la performance des SI en Algérie ?",
                 "a": "Les indicateurs de performance IT :\n- Disponibilité : % de temps de fonctionnement\n- Temps de réponse : durée de traitement des transactions\n- Taux d'erreur : nombre d'erreurs par transaction\n- Coût IT : rapport entre budget IT et chiffre d'affaires\n- Satisfaction utilisateurs : enquêtes de satisfaction"},
                {"q": "Qu'est-ce que COBIT en Algérie ?",
                 "a": "COBIT (Control Objectives for Information and Related Technologies) est un cadre de référence pour la gouvernance et le management des SI. Il définit les processus IT et les objectifs de contrôle. En Algérie, COBIT est utilisé pour l'audit et l'amélioration des systèmes d'information."},
                {"q": "Comment auditer un ERP en Algérie ?",
                 "a": "L'audit d'un ERP comprend :\n- Évaluation de la configuration des modules\n- Test des contrôles internes dans l'ERP\n- Vérification de la sécurité des accès\n- Audit des interfaces avec les autres systèmes\n- Évaluation de la qualité des données migrées"},
                {"q": "Qu'est-ce que la gouvernance IT en Algérie ?",
                 "a": "La gouvernance IT est l'ensemble des processus qui ensures que les SI apportent de la valeur à l'entreprise. Elle comprend :\n- Le comité de pilotage IT\n- La gestion des projets IT\n- La gestion des risques IT\n- La gestion des contrats et des prestataires"},
                {"q": "Comment auditer la continuité d'activité en Algérie ?",
                 "a": "L'audit de continuité d'activité vérifie :\n- L'existence d'un plan de reprise d'activité (PRA)\n- La sauvegarde régulière des données\n- Les tests de restauration\n- La formation du personnel aux procédures d'urgence\n- Les accords avec les sites de secours"},
                {"q": "Quels sont les outils d'audit IT en Algérie ?",
                 "a": "Les principaux outils :\n- Logiciels d'analyse de données (ACL, IDEA)\n- Outils de test de sécurité (Nessus, Metasploit)\n- Logiciels de gestion des incidents (ServiceNow)\n- Outils de monitoring (Nagios, Zabbix)\n- Logiciels de gestion des actifs IT (GLPI)"},
            ])
        elif "01_scf_algerien" in filename:
            diverse.extend([
                {"q": "Comment comptabiliser une immobilisation enAlgérie ?",
                 "a": "L'écriture d'une immobilisation est :\nDébit : 21x - Immobilisation corporelle\nCrédit : 401 - Fournisseurs (ou 521 - Banque)\n\nL'amortissement est comptabilisé mensuellement :\nDébit : 681 - Dotations aux amortissements\nCrédit : 28x - Amortissements"},
                {"q": "Qu'est-ce que le fonds de commerce en Algérie ?",
                 "a": "Le fonds de commerce est un ensemble d'éléments corporels et incorporels utilisés pour exploiter une activité commerciale. Il comprend : la clientèle, l'enseigne, le droit au bail, les licences, les brevets, les marques. Il est comptabilisé en compte 207."},
                {"q": "Comment calculer les amortissements en Algérie ?",
                 "a": "Les amortissements peuvent être :\n- Linéaires : la valeur d'origine est étalée sur la durée de vie\n- Dégressifs : le taux est multiplié par un coefficient (1,5 ou 2)\nLes taux sont fixés par la réglementation fiscale algérienne."},
                {"q": "Qu'est-ce qu'une provision pour dépréciation en Algérie ?",
                 "a": "Une provision pour dépréciation est une diminution de la valeur d'un actif. Elle est comptabilisée :\nDébit : 682 - Dotations aux provisions\nCrédit : 49x - Dépréciations (compte concerné)\n\nElle est déductible du résultat fiscal si elle est justifiée."},
                {"q": "Comment comptabiliser une réforme d'immobilisation ?",
                 "a": "La réforme consiste à remplacer une immobilisation usée par une nouvelle :\nDébit : 21x - Nouvelle immobilisation\nCrédit : 21x - Ancienne immobilisation\nCrédit : 771 - Produits des cessions (ou Débit 671 si perte)\n\nLes amortissements cumulés de l'ancienne immobilisation sont réintegrés."},
            ])
        elif "04_droit_commercial_algerie" in filename:
            diverse.extend([
                {"q": "Quelles sont les formes juridiques en Algérie ?",
                 "a": "Les principales formes juridiques :\n- SARL : Société À Responsabilité Limitée (2 associés minimum)\n- EURL : Entreprise Unipersonnelle À Responsabilité Limitée (1 associé)\n- SNC : Société en Nom Collectif\n- SPA : Société Par Actions\n- Société en commandite"},
                {"q": "Comment créer une entreprise en Algérie ?",
                 "a": "Les étapes de création :\n1) Obtention du numéro d'identification fiscale (NIF)\n2) Rédaction des statuts\n3) Publication au Journal Officiel\n4) Dépôt du capital social\n5) Immatriculation au registre du commerce\n6) Affiliation à la CNAS"},
                {"q": "Qu'est-ce que le registre du commerce en Algérie ?",
                 "a": "Le registre du commerce est un registre public tenu par le greffe du tribunal de commerce. Il enregistre toutes les sociétés commerciales et les commerçants individuels. L'immatriculation est obligatoire pour exercer une activité commerciale."},
                {"q": "Quelles sont les obligations d'une SARL en Algérie ?",
                 "a": "Les obligations principales :\n- Tenue d'une comptabilité régulière selon le SCF\n- Déclaration et paiement de la TVA\n- Déclaration et paiement de l'IBS (19%)\n- Déclaration des salaires et paiement des cotisations CNAS\n- Tenue d'une assemblée générale annuelle\n- Dépôt des comptes annuels au greffe du tribunal"},
                {"q": "Comment fonctionne l'assemblée générale en SARL ?",
                 "a": "L'assemblée générale peut être ordinaire ou extraordinaire :\n- AG ordinaire : approbation des comptes, affectation du résultat\n- AG extraordinaire : modification des statuts, augmentation de capital\nLes décisions sont prises à la majorité des associés représentant plus de la moitié du capital social."},
            ])
        elif "05_charges_sociales" in filename:
            diverse.extend([
                {"q": "Quelles sont les cotisations CNAS en Algérie ?",
                 "a": "Les cotisations CNAS comprennent :\n- Part salariale : 1,75% du salaire brut\n- Part patronale : 26% du salaire brut\nTotal : 27,75% du salaire brut\nElles couvrent les prestations sociales (retraite, maladie, accidents du travail)."},
                {"q": "Comment calculer les charges sociales en Algérie ?",
                 "a": "Les charges sociales se calculent ainsi :\n- Cotisations CNAS : 27,75% du salaire brut\n- Taxe sur les salaires : 1% du salaire brut\n- Assurance accidents du travail : 1,25% du salaire brut\nTotal : environ 30% du salaire brut"},
                {"q": "Qu'est-ce que la CASNOS en Algérie ?",
                 "a": "La CASNOS (Caisse Nationale de Sécurité Sociale des Non-Salariés) gère la protection sociale des travailleurs indépendants. Les cotisants bénéficient des prestations sociales (retraite, maladie, maternité) selon un régime forfaitaire."},
                {"q": "Quelles sont les prestations sociales en Algérie ?",
                 "a": "Les principales prestations :\n- Retraite : pension de vieillesse\n- Maladie : remboursement des soins\n- Maternité : indemnités journalières\n- Accidents du travail : indemnités et soins\n- Allocations familiales"},
                {"q": "Comment déclarer les charges sociales en Algérie ?",
                 "a": "La déclaration se fait mensuellement via le portail CNAS. L'entreprise doit :\n- Déclarer les salaires versés\n- Payer les cotisations (part salariale et patronale)\n- Transmettre les bulletins de paie\nLe paiement doit être effectué avant la fin du mois suivant."},
            ])
        elif "06_formes_juridiques" in filename:
            diverse.extend([
                {"q": "Quelle est la différence entre SARL et EURL ?",
                 "a": "La SARL nécessite 2 associés minimum, tandis que l'EURL n'en nécessite qu'un seul. Les deux ont un capital social librement fixé et une responsabilité limitée aux apports."},
                {"q": "Qu'est-ce qu'une SPA en Algérie ?",
                 "a": "La SPA (Société Par Actions) est une société dont le capital est divisé en actions. Elle doit avoir au moins 7 actionnaires. Le capital social est librement fixé par les statuts."},
                {"q": "Comment modifier les statuts d'une SARL ?",
                 "a": "La modification nécessite :\n1) Une décision des associés en assemblée générale extraordinaire\n2) La modification de l'acte constitutif\n3) La publication au Journal Officiel\n4) Le dépôt au greffe du tribunal de commerce\n5) La mise à jour du registre du commerce"},
                {"q": "Quelles sont les causes de dissolution d'une SARL ?",
                 "a": "Les causes de dissolution :\n- Décision des associés en assemblée générale extraordinaire\n- Fin de durée (expiration du terme)\n- Réalisation ou expiration de l'objet social\n- Dissolution anticipée par le tribunal (faillite)\n- Réduction du nombre d'associés en dessous de 2"},
            ])
        elif "07_procedures_pratiques" in filename:
            diverse.extend([
                {"q": "Comment comptabiliser une provision pour créance douteuse ?",
                 "a": "L'écriture est :\nDébit : 682 - Dotations aux provisions\nCrédit : 491 - Dépréciations clients\n\nSi la créance est recouvrée :\nDébit : 491 - Dépréciations clients\nCrédit : 782 - Reprises sur provisions"},
                {"q": "Comment effectuer un rapprochement bancaire ?",
                 "a": "Le rapprochement bancaire consiste à comparer le compte 521 avec le relevé bancaire. Les écarts sont dus à :\n- Chèques émis non présentés\n- Virements non comptabilisés\n- Frais bancaires non enregistrés\nIl doit être effectué mensuellement."},
                {"q": "Comment comptabiliser un emprunt bancaire ?",
                 "a": "L'écriture d'un emprunt :\nDébit : 521 - Banque\nCrédit : 152 - Emprunts\n\nLes remboursements :\nDébit : 152 - Emprunts\nDébit : 661 - Intérêts d'emprunts\nCrédit : 521 - Banque"},
                {"q": "Comment comptabiliser une cession d'immobilisation ?",
                 "a": "L'écriture :\nDébit : 521 - Banque (prix de vente)\nDébit : 28x - Amortissements (cumulés)\nCrédit : 21x - Immobilisation (valeur d'origine)\nCrédit : 771 - Produits des cessions (ou Débit 671 si perte)"},
                {"q": "Comment comptabiliser une subvention d'investissement ?",
                 "a": "L'écriture :\nDébit : 521 - Banque\nCrédit : 131 - Subventions d'investissement\n\nEn fin d'exercice :\nDébit : 131 - Subventions d'investissement\nCrédit : 74 - Subventions d'exploitation"},
            ])
        elif "02_fiscalite_algerie" in filename:
            diverse.extend([
                {"q": "Comment calculer la taxe professionnelle en Algérie ?",
                 "a": "La taxe professionnelle se calcule ainsi :\nTaxe = CAHT × taux selon l'activité\n\nLe taux varie de 0,5% à 2% selon le secteur d'activité. Elle est déclarée annuellement et payée en 4 acomptes trimestriels."},
                {"q": "Qu'est-ce que le droit de timbre en Algérie ?",
                 "a": "Le droit de timbre est un impôt proportionnel sur les actes et documents :\n- Factures : 0,01% du montant HT (plafonné)\n- Chèques : montant fixe selon la tranche\n- Actes de société : forfaitaire\nIl est déductible du résultat fiscal."},
                {"q": "Comment fonctionne la taxation minimum en Algérie ?",
                 "a": "La taxation minimum s'applique aux entreprises déficitaires ou à faible résultat. Elle est calculée sur une base forfaitaire (0,5% du CA avec un minimum absolu). Elle est due même en l'absence de bénéfice."},
                {"q": "Quels sont les avantages fiscaux pour les exportateurs ?",
                 "a": "Les entreprises exportatrices bénéficient :\n- Exonération de TVA sur les exportations (0%)\n- Exonération d'IBS pendant 5 ans\n- Exonération de taxe professionnelle pendant 3 ans\n- Remboursement de la TVA sur les achats"},
            ])
        elif "03_normes_audit_algerie" in filename:
            diverse.extend([
                {"q": "Quelle est la mission du commissaire aux comptes ?",
                 "a": "Le commissaire aux comptes doit :\n- Vérifier la sincérité et la régularité des comptes annuels\n- Contrôler la sincérité des informations financières\n- Signaler les faits compromettant la continuité d'exploitation\n- Émettre un rapport sur les comptes annuels"},
                {"q": "Quels sont les types d'opinion d'audit ?",
                 "a": "Les 4 types d'opinion :\n1) Sans réserve : comptes réguliers et sincères\n2) Avec réserve : réserves sur éléments déterminants\n3) Défavorable : comptes non réguliers\n4) Abstention : éléments insuffisants pour émettre une opinion"},
                {"q": "Comment se déroule un audit ?",
                 "a": "Les phases d'un audit :\n1) Préparation : compréhension de l'entreprise\n2) Travail : tests de contrôle et procédures substantives\n3) Conclusion : évaluation des résultats\n4) Rapport : rédaction du rapport d'audit"},
                {"q": "Qu'est-ce que la confirmation externe en audit ?",
                 "a": "La confirmation externe est une procédure d'audit qui consiste à obtenir une réponse directe de tiers (clients, fournisseurs, banques) pour confirmer les montants ou les informations comptables. Elle est utilisée pour les soldes de comptes de tiers, les opérations importantes et les engagements hors bilan."},
                {"q": "Comment fonctionne le test de contrôle en audit ?",
                 "a": "Le test de contrôle est une procédure d'audit destinée à évaluer l'efficacité du dispositif de contrôle interne. Il vérifie si les procédures mises en place fonctionnent effectivement. Les résultats permettent d'adapter l'étendue des procédures substantives."},
            ])

    return diverse


def read_knowledge_base_files():
    kb_content = {}
    for filename in os.listdir(KB_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(KB_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                kb_content[filename] = f.read()
    return kb_content


def generate_additional_examples():
    existing = load_existing_examples(OUTPUT_FILE)
    kb_files = read_knowledge_base_files()
    additional = []

    for filename, content in kb_files.items():
        sections = extract_sections(content, filename)
        for title, section_content in sections:
            qa_pairs = generate_qa_from_section(title, section_content, filename)
            for qa in qa_pairs:
                if qa["q"].strip().lower() not in existing:
                    additional.append(qa)
                    existing.add(qa["q"].strip().lower())

    diverse = generate_diverse_qa()
    for qa in diverse:
        if qa["q"].strip().lower() not in existing:
            additional.append(qa)
            existing.add(qa["q"].strip().lower())

    return additional


def append_to_dataset(additional_examples, output_path):
    with open(output_path, "a", encoding="utf-8") as f:
        for item in additional_examples:
            record = {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": item["q"]},
                    {"role": "assistant", "content": item["a"]},
                ]
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def count_examples(path):
    count = 0
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    count += 1
    return count


if __name__ == "__main__":
    print("Loading existing dataset...")
    existing_count = count_examples(OUTPUT_FILE)
    print(f"Existing examples: {existing_count}")

    print("\nGenerating additional examples from knowledge base...")
    additional = generate_additional_examples()
    print(f"New examples to add: {len(additional)}")

    if additional:
        print("\nAppending to dataset...")
        append_to_dataset(additional, OUTPUT_FILE)
        final_count = count_examples(OUTPUT_FILE)
        print(f"Total examples after update: {final_count}")
    else:
        print("No new examples to add.")
