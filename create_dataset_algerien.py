import json
import os

SYSTEM_PROMPT = (
    "Tu es un expert-comptable et auditeur algérien. "
    "Tu réponds de manière précise, professionnelle et détaillée aux questions "
    "comptables, fiscales, d'audit et de droit commercial. "
    "Tu utilises le Plan Comptable National (SCF) algérien et la terminologie "
    "professionnelle algérienne. Tu connais parfaitement la fiscalité algérienne "
    "(IBS, TVA, IRG, taxe professionnelle) et les spécificités du cadre juridique "
    "et bancaire algérien."
)

DATA = [
    # ============================================================
    # SCF ALGÉRIEN — Classes et structure (25 exemples)
    # ============================================================
    {
        "q": "Quelles sont les 7 classes de comptes du Plan Comptable National algérien ?",
        "a": (
            "Le SCF algérien comprend 7 classes :\n"
            "- Classe 1 : Comptes de financement permanent (capitaux propres, emprunts)\n"
            "- Classe 2 : Comptes d'actif immobilisé (immobilisations incorporelles, corporelles, financières)\n"
            "- Classe 3 : Comptes de stocks\n"
            "- Classe 4 : Comptes de tiers (fournisseurs, clients, état, personnel)\n"
            "- Classe 5 : Comptes de trésorerie (banques, caisse)\n"
            "- Classe 6 : Comptes de charges\n"
            "- Classe 7 : Comptes de produits"
        ),
    },
    {
        "q": "Quelle est la différence entre le SCF algérien et le PCG français ?",
        "a": (
            "Le SCF algérien est largement inspiré du PCG français mais présente des différences :\n"
            "- Les taux de TVA sont différents (19% et 9% en Algérie contre 20%, 10%, 5,5% en France)\n"
            "- Les charges sociales sont différentes (CNAS/CASNOS en Algérie)\n"
            "- La fiscalité est spécifique (IBS 19%, IRG)\n"
            "- Certaines comptes sont spécifiques au contexte algérien (comptes CNAS, CASNOS)\n"
            "- Les formes juridiques sont différentes (SARL, EURL, SNC, SPA)"
        ),
    },
    {
        "q": "Qu'est-ce qu'un compte de classe 6 ?",
        "a": (
            "Les comptes de classe 6 sont les comptes de charges. Ils enregistrent toutes les dépenses "
            "de l'entreprise : achats de marchandises, services extérieurs, charges de personnel, "
            "dotations aux amortissements, charges financières et charges exceptionnelles. "
            "Ces comptes sont soldés par transfert au compte de résultat en fin d'exercice."
        ),
    },
    {
        "q": "Qu'est-ce qu'un compte de classe 7 ?",
        "a": (
            "Les comptes de classe 7 sont les comptes de produits. Ils enregistrent tous les revenus "
            "de l'entreprise : ventes de marchandises, production vendue, produits financiers, "
            "produits exceptionnels. Ces comptes sont soldés par transfert au compte de résultat "
            "en fin d'exercice."
        ),
    },
    {
        "q": "Comment fonctionne le principe de partie double en comptabilité ?",
        "a": (
            "Le principe de partie double est la règle fondamentale de la comptabilité. Toute opération "
            "comptable est enregistrée au minimum dans deux comptes : un au débit et un au crédit, "
            "de montants égaux. Par exemple, un achat au comptant débite le compte d'achat (classe 6) "
            "et crédite le compte de banque (classe 5). Ce principe assure l'équilibre permanent du bilan."
        ),
    },
    {
        "q": "Quelle est la différence entre un compte de bilan et un compte de gestion ?",
        "a": (
            "Les comptes de bilan (classes 1 à 5) sont des comptes permanents : ils figurent au bilan "
            "et leur solde est reporté d'un exercice à l'autre. Les comptes de gestion (classes 6 et 7) "
            "sont des comptes temporaires : ils sont ouverts et soldés chaque exercice pour déterminer "
            "le résultat. En fin d'exercice, on effectue le transfert des comptes de gestion pour "
            "calculer le résultat (bénéfice ou perte)."
        ),
    },
    {
        "q": "Quels sont les comptes de la classe 1 du SCF algérien ?",
        "a": (
            "La classe 1 comprend les comptes de financement permanent :\n"
            "- 10 : Capital social\n"
            "- 11 : Réserves\n"
            "- 12 : Résultats (bénéfice ou perte)\n"
            "- 13 : Subventions d'investissement\n"
            "- 14 : Provisions réglementées\n"
            "- 15 : Emprunts et dettes assimilées\n"
            "- 16 : Comptes de liaison des établissements"
        ),
    },
    {
        "q": "Quels sont les comptes de la classe 2 du SCF algérien ?",
        "a": (
            "La classe 2 comprend les comptes d'actif immobilisé :\n"
            "- 20 : Immobilisations incorporelles (fonds de commerce, brevets, logiciels)\n"
            "- 21 : Immobilisations corporelles (terrains, constructions, matériel)\n"
            "- 22 : Immobilisations mises en concession\n"
            "- 23 : Immobilisations en cours\n"
            "- 24 : Immobilisations financières (prêts, participations)\n"
            "- 25 : Écarts de conversion"
        ),
    },
    {
        "q": "Quels sont les comptes de la classe 3 du SCF algérien ?",
        "a": (
            "La classe 3 comprend les comptes de stocks :\n"
            "- 30 : Stocks de marchandises\n"
            "- 31 : Matières premières\n"
            "- 32 : Autres approvisionnements\n"
            "- 33 : En-cours de production\n"
            "- 34 : Produits intermédiaires\n"
            "- 35 : Produits finis"
        ),
    },
    {
        "q": "Quels sont les comptes de la classe 4 du SCF algérien ?",
        "a": (
            "La classe 4 comprend les comptes de tiers :\n"
            "- 40 : Fournisseurs et comptes rattachés\n"
            "- 41 : Clients et comptes rattachés\n"
            "- 42 : Personnel\n"
            "- 43 : Organismes sociaux (CNAS, CASNOS)\n"
            "- 44 : État et collectivités publiques\n"
            "- 45 : Autres créanciers et débiteurs\n"
            "- 47 : Comptes d'attente\n"
            "- 48 : Charges et produits constatés d'avance"
        ),
    },
    {
        "q": "Quels sont les comptes de la classe 5 du SCF algérien ?",
        "a": (
            "La classe 5 comprend les comptes de trésorerie :\n"
            "- 50 : Titres de placement\n"
            "- 52 : Banques et établissements financiers (CNEP, BADR, BEA, BNA, CPA)\n"
            "- 53 : Caisse\n"
            "- 54 : Régies d'avance et accréditifs"
        ),
    },
    {
        "q": "Qu'est-ce que le compte 600 ?",
        "a": (
            "Le compte 600 est le compte Achats de marchandises. Il enregistre les achats de biens "
            "destinés à la revente en l'état. Ce compte est débité lors de la réception de la marchandise "
            "et crédité lors du reversement du stock de départ en fin d'exercice."
        ),
    },
    {
        "q": "Qu'est-ce que le compte 606 ?",
        "a": (
            "Le compte 606 est le compte Services extérieurs A. Il comprend les sous-comptes :\n"
            "- 6061 : Locations de terrains et bâtiments\n"
            "- 6062 : Locations de matériel et mobilier\n"
            "- 6063 : Locations d'emballages\n"
            "- 6064 : Entretien et réparations\n"
            "- 6065 : Primes d'assurance\n"
            "- 6066 : Rémunérations d'intermédiaires\n"
            "- 6067 : Frais de publicité et de promotion\n"
            "- 6068 : Frais de transport et de déplacement"
        ),
    },
    {
        "q": "Qu'est-ce que le compte 622 ?",
        "a": (
            "Le compte 622 est le compte Honoraires et frais d'experts. Il enregistre les "
            "rémunérations des professionnels extérieurs : honoraires d'experts-comptables, "
            "d'avocats, de notaires, de consultants, et autres prestations de services intellectuels."
        ),
    },
    {
        "q": "Qu'est-ce que le compte 651 ?",
        "a": (
            "Le compte 651 est le compte Salaires et appointements. Il enregistre les "
            "rémunérations brutes versées au personnel : salaires de base, primes, "
            "indemnités, majorations pour heures supplémentaires, et tout élément de "
            "rémunération entrant dans l'assiette des cotisations sociales."
        ),
    },
    {
        "q": "Qu'est-ce que le compte 701 ?",
        "a": (
            "Le compte 701 est le compte Ventes de marchandises. Il enregistre le chiffre "
            "d'affaires réalisé par la vente de biens en l'état. Ce compte est crédité "
            "lors de l'émission de la facture client."
        ),
    },
    {
        "q": "Qu'est-ce que le compte 712 ?",
        "a": (
            "Le compte 712 est le compte Production vendue de services. Il enregistre "
            "le chiffre d'affaires réalisé par la prestation de services : consulting, "
            "formation, maintenance, conseil, et autres prestations immatérielles."
        ),
    },
    {
        "q": "Comment écrit-on un achat de marchandises au comptant en Algérie ?",
        "a": (
            "L'écriture d'un achat de marchandises au comptant est :\n"
            "Débit : 600 - Achats de marchandises\n"
            "Crédit : 521 - Banque\n"
            "Montant : HT (hors taxes). La TVA déductible (19%) est comptabilisée "
            "séparément au débit du compte 445."
        ),
    },
    {
        "q": "Comment comptabiliser une vente de marchandises en Algérie ?",
        "a": (
            "L'écriture d'une vente de marchandises est :\n"
            "Débit : 411 - Clients\n"
            "Crédit : 701 - Ventes de marchandises (HT)\n"
            "Crédit : 443 - État - TVA collectée (19%)\n"
            "Le montant TTC est débité au compte 411."
        ),
    },
    {
        "q": "Qu'est-ce que le compte 401 ?",
        "a": (
            "Le compte 401 est le compte Fournisseurs. Il enregistre les dettes de l'entreprise "
            "envers ses fournisseurs pour des achats de biens ou services. C'est un compte de crédit "
            "(son solde créditeur indique le montant dû aux fournisseurs). Les factures fournisseurs "
            "sont débitées au 401 lors de leur réception."
        ),
    },
    {
        "q": "Qu'est-ce que le compte 411 ?",
        "a": (
            "Le compte 411 est le compte Clients. Il enregistre les créances de l'entreprise "
            "sur ses clients pour des ventes de biens ou services. C'est un compte de débit "
            "(son solde débiteur indique le montant dû par les clients). Les factures clients "
            "sont créditées au 411 lors de leur émission."
        ),
    },
    {
        "q": "Qu'est-ce que le compte 445 ?",
        "a": (
            "Le compte 445 est le compte État - TVA déductible. Il enregistre la TVA facturée "
            "par les fournisseurs sur les achats. C'est un compte de débit. La TVA déductible "
            "est récupérable lors des déclarations de TVA mensuelles ou trimestrielles."
        ),
    },
    {
        "q": "Qu'est-ce que le compte 443 ?",
        "a": (
            "Le compte 443 est le compte État - TVA collectée. Il enregistre la TVA facturée "
            "aux clients sur les ventes. C'est un compte de crédit. La TVA collectée est reversée "
            "à l'administration fiscale lors des déclarations de TVA."
        ),
    },
    {
        "q": "Comment fonctionne la spécialisation des exercices ?",
        "a": (
            "La spécialisation des exercices est un principe comptable fondamental. Il consiste à "
            "rattacher les charges et les produits à l'exercice auquel ils se rapportent, "
            "indépendamment de la date de paiement ou d'encaissement. En fin d'exercice, on passe "
            "des écritures de régularisation : charges constatées d'avance, produits constatés "
            "d'avance, provisions, et amortissements."
        ),
    },

    # ============================================================
    # FISCALITÉ ALGÉRIENNE (25 exemples)
    # ============================================================
    {
        "q": "Quel est le taux de l'Impôt sur les Sociétés (IBS) en Algérie ?",
        "a": (
            "En Algérie, l'IBS est fixé à 19% du bénéfice net. Ce taux est applicable à l'ensemble "
            "des sociétés quel que soit leur chiffre d'affaires. Contrairement à la France, il n'existe "
            "pas de taux réduit pour les petites entreprises. Le bénéfice net est déterminé à partir "
            "du résultat comptable, ajusté par les réintégrations et déductions fiscales."
        ),
    },
    {
        "q": "Quels sont les taux de TVA en Algérie ?",
        "a": (
            "L'Algérie applique 3 taux de TVA :\n"
            "- Taux normal : 19% (taux de droit commun)\n"
            "- Taux réduit : 9% (produits de première nécessité, médicaments, livres, transports)\n"
            "- Taux zéro : 0% (exportations de biens et services)\n"
            "La TVA est déclarée mensuellement ou trimestriellement selon le régime de l'entreprise."
        ),
    },
    {
        "q": "Qu'est-ce que l'IRG en Algérie ?",
        "a": (
            "L'IRG (Impôt sur le Revenu Global) est l'impôt sur le revenu des personnes physiques "
            "en Algérie. Il est retenu à la source sur les salaires selon un barème progressif :\n"
            "- Jusqu'à 120 000 DA : 0%\n"
            "- De 120 001 à 300 000 DA : 20%\n"
            "- De 300 001 à 600 000 DA : 30%\n"
            "- De 600 001 à 1 200 000 DA : 35%\n"
            "- Au-delà de 1 200 000 DA : 40%"
        ),
    },
    {
        "q": "Comment calculer le résultat fiscal en Algérie ?",
        "a": (
            "Le résultat fiscal se calcule ainsi :\n"
            "Résultat fiscal = Résultat comptable + Réintégrations fiscales - Déductions fiscales\n\n"
            "Réintégrations : amendes et pénalités, charges non justifiées, provisions non déductibles, "
            "dotations aux amortissements excédant les taux autorisés.\n"
            "Déductions : abattement sur dividendes de filiales, plus-values à long terme exonérées, "
            "crédits d'impôt."
        ),
    },
    {
        "q": "Qu'est-ce que la taxe professionnelle en Algérie ?",
        "a": (
            "La taxe professionnelle est un impôt local basé sur le chiffre d'affaires. Le taux "
            "est de 0,5% à 2% du CAHT selon l'activité. Elle est due par toute entreprise exerçant "
            "une activité professionnelle non commerciale ou commerciale. La déclaration se fait "
            "annuellement et le paiement est étalé en 4 acomptes trimestriels."
        ),
    },
    {
        "q": "Qu'est-ce que le droit de timbre en Algérie ?",
        "a": (
            "Le droit de timbre est un impôt proportionnel prélevé sur certains actes et documents. "
            "Les principaux taux sont :\n"
            "- Factures : 0,01% du montant HT (plafonné)\n"
            "- Chèques : montant fixe selon la tranche\n"
            "- Actes de société : forfaitaire\n"
            "- Contrats commerciaux : variable selon le type\n"
            "Le droit de timbre est déductible du résultat fiscal."
        ),
    },
    {
        "q": "Quand doit-on déclarer la TVA en Algérie ?",
        "a": (
            "La déclaration de TVA dépend du régime :\n"
            "- Régime mensuel : déclaration avant la fin du mois suivant\n"
            "- Régime trimestriel : déclaration avant la fin du mois suivant le trimestre\n"
            "- Entreprises nouvellement créées : déclaration mensuelle les 2 premières années\n"
            "La déclaration se fait sur le portail fiscal de la DGI (Direction Générale des Impôts)."
        ),
    },
    {
        "q": "Qu'est-ce que la retenue à la source en Algérie ?",
        "a": (
            "La retenue à la source est un mécanisme par lequel l'entreprise retient un pourcentage "
            "sur les paiements effectués à des tiers. Les principaux taux sont :\n"
            "- Honoraires et prestations de services : 20%\n"
            "- Locations meublées : 10%\n"
            "- Commissions et courtages : 15%\n"
            "- Droits d'auteur : 10%\n"
            "La retenue est versée mensuellement à l'administration fiscale."
        ),
    },
    {
        "q": "Comment fonctionne l'IBS en Algérie pour les PME ?",
        "a": (
            "En Algérie, le taux d'IBS est de 19% pour toutes les sociétés, sans taux réduit "
            "pour les PME. Cependant, les entreprises nouvellement créées bénéficient d'une "
            "exonération totale d'IBS pendant les 3 premiers exercices. La base imposable est "
            "le bénéfice net, déterminé selon les règles comptables du SCF."
        ),
    },
    {
        "q": "Qu'est-ce que la DGI en Algérie ?",
        "a": (
            "La DGI (Direction Générale des Impôts) est l'administration fiscale algérienne. "
            "Elle est chargée du recouvrement des impôts, du contrôle fiscal et de la lutte "
            "contre la fraude. Les entreprises interagissent avec la DGI pour leurs déclarations "
            "fiscales, leurs paiements et les contrôles fiscaux."
        ),
    },
    {
        "q": "Quels sont les impôts directs en Algérie ?",
        "a": (
            "Les impôts directs en Algérie comprennent :\n"
            "- IBS (Impôt sur les Sociétés) : 19% du bénéfice net\n"
            "- IRG (Impôt sur le Revenu Global) : barème progressif sur les salaires\n"
            "- Taxe sur les salaires : 1% sur les rémunérations brutes\n"
            "- Taxe professionnelle : 0,5% à 2% du CA\n"
            "- Impôt foncier : basé sur la valeur locative des biens immobiliers"
        ),
    },
    {
        "q": "Quels sont les impôts indirects enAlgérie ?",
        "a": (
            "Les impôts indirects en Algérie comprennent :\n"
            "- TVA (Taxe sur la Valeur Ajoutée) : 19%, 9% ou 0%\n"
            "- Droit de timbre : sur actes et documents\n"
            "- Droits de douane : sur les importations\n"
            "- Taxe sur les transactions immobilier : 3%\n"
            "La TVA est l'impôt indirect le plus important en termes de recettes."
        ),
    },
    {
        "q": "Comment calculer la TVA à payer en Algérie ?",
        "a": (
            "La TVA à payer se calcule ainsi :\n"
            "TVA due = TVA collectée - TVA déductible\n\n"
            "TVA collectée = Montant des ventes TTC × taux de TVA applicable\n"
            "TVA déductible = Montant des achats TTC × taux de TVA applicable\n\n"
            "Si la TVA déductible est supérieure à la TVA collectée, le solde est reportable "
            "sur les périodes suivantes ou remboursable sous certaines conditions."
        ),
    },
    {
        "q": "Qu'est-ce que le régime fiscal des auto-entrepreneurs en Algérie ?",
        "a": (
            "En Algérie, le régime de l'auto-entrepreneur (micro-entreprise) est soumis à :\n"
            "- Un impôt forfaitaire basé sur le chiffre d'affaires\n"
            "- Pas de TVA si le CA est inférieur aux seuils de franchise\n"
            "- Cotisations CNAS proportionnelles au CA\n"
            "Les seuils varient selon l'activité et sont révisés annuellement."
        ),
    },
    {
        "q": "Qu'est-ce que la base imposable de l'IBS ?",
        "a": (
            "La base imposable de l'IBS est le bénéfice net fiscal. Il se calcule ainsi :\n"
            "Bénéfice net = Résultat comptable + Réintégrations fiscales - Déductions fiscales\n\n"
            "Réintégrations principales : amendes, pénalités, provisions non déductibles, "
            "dotations excédant les taux légaux.\n"
            "Déductions principales : abattement 95% sur dividendes, plus-values à long terme."
        ),
    },
    {
        "q": "Qu'est-ce que le crédit d'impôt en Algérie ?",
        "a": (
            "Le crédit d'impôt est une somme déduite directement de l'impôt dû. En Algérie, "
            "les principaux crédits d'impôt concernent :\n"
            "- L'investissement dans les zones de développement durable\n"
            "- La création d'emplois pour les jeunes\n"
            "- La formation professionnelle\n"
            "Le crédit d'impôt est reportable sur 4 exercices."
        ),
    },
    {
        "q": "Comment fonctionne le contrôle fiscal en Algérie ?",
        "a": (
            "Le contrôle fiscal en Algérie peut être :\n"
            "- Contrôle sur pièces : vérification des déclarations au bureau\n"
            "- Contrôle sur place : vérification dans les locaux de l'entreprise\n"
            "- Vérification de la comptabilité : examination des livres et documents\n"
            "Le contribuable a le droit de se faire assister par un mandataire. "
            "Le délai de reprise est de 4 ans à compter de la déclaration."
        ),
    },
    {
        "q": "Quelles sont les sanctions fiscales en Algérie ?",
        "a": (
            "Les sanctions fiscales en Algérie comprennent :\n"
            "- Amendes pour retard de déclaration : 10% du montant de l'impôt\n"
            "- Amendes pour non-déclaration : 40% du montant de l'impôt\n"
            "- Intérêts de retard : 0,2% par mois\n"
            "- Sanctions pénales en cas de fraude : emprisonnement et amende\n"
            "Le contribuable peut régulariser sa situation avant notification du contrôle."
        ),
    },
    {
        "q": "Qu'est-ce que la taxe sur la valeur ajoutée à l'importation ?",
        "a": (
            "La TVA à l'importation est due sur les biens importés. Elle est calculée sur la "
            "valeur en douane augmentée des droits de douane et taxes assimilées. Le taux applicable "
            "est de 19% pour la plupart des biens. Les entreprises peuvent déduire cette TVA "
            "comme TVA déductible sur leur déclaration de TVA."
        ),
    },
    {
        "q": "Comment déclarer le chiffre d'affaires en Algérie ?",
        "a": (
            "Le chiffre d'affaires est déclaré :\n"
            "- Dans la déclaration de TVA (mensuelle ou trimestrielle)\n"
            "- Dans la déclaration du résultat fiscal (annuelle)\n"
            "- Dans la déclaration de la taxe professionnelle (annuelle)\n"
            "Le CA est exprimé en dinars algériens (DA) et correspond au montant HT des ventes."
        ),
    },
    {
        "q": "Qu'est-ce que la taxation minimum en Algérie ?",
        "a": (
            "La taxation minimum s'applique aux entreprises dont le bénéfice net est déficitaire "
            "ou trop faible. Elle est calculée sur une base forfaitaire. Le taux est de 0,5% "
            "du chiffre d'affaires, avec un minimum absolu. Cette taxe est due même en l'absence "
            "de bénéfice."
        ),
    },
    {
        "q": "Quels sont les avantages fiscaux pour les entreprises exportatrices ?",
        "a": (
            "Les entreprises exportatrices bénéficient d'avantages fiscaux :\n"
            "- Exonération de TVA sur les exportations (taux 0%)\n"
            "- Exonération d'IBS pendant 5 ans pour les nouvelles exportatrices\n"
            "- Exonération de taxe professionnelle pendant 3 ans\n"
            "- Remboursement de la TVA sur les achats\n"
            "Ces avantages visent à encourager les exportations."
        ),
    },
    {
        "q": "Comment fonctionne l'imposition des sociétés en liquidation en Algérie ?",
        "a": (
            "Les sociétés en liquidation sont soumises à l'IBS sur leur résultat fiscal. "
            "Le liquidateur doit souscrire les déclarations fiscales et payer l'impôt dû. "
            "En cas de liquidation judiciaire, les créances fiscales sont prioritaires. "
            "La TVA collectée doit être déclarée et payée même pendant la liquidation."
        ),
    },
    {
        "q": "Qu'est-ce que la régularisation de la TVA en fin d'année ?",
        "a": (
            "La régularisation de TVA en fin d'année consiste à ajuster les déclarations pour "
            "tenir compte des éléments suivants :\n"
            "- Charges constatées d'avance et produits constatés d'avance\n"
            "- Acomptes reçus et facturés\n"
            "- Régularisation des stocks\n"
            "La régularisation doit être effectuée avant la clôture de l'exercice."
        ),
    },

    # ============================================================
    # ÉCRITURES COMPTABLES COURANTES (25 exemples)
    # ============================================================
    {
        "q": "Comment comptabiliser un achat de marchandises avec TVA en Algérie ?",
        "a": (
            "L'écriture d'un achat de marchandises avec TVA (19%) est :\n"
            "Débit : 600 - Achats de marchandises (HT)\n"
            "Débit : 445 - TVA déductible (19%)\n"
            "Crédit : 401 - Fournisseurs (TTC)\n\n"
            "Si paiement au comptant :\n"
            "Crédit : 521 - Banque"
        ),
    },
    {
        "q": "Comment comptabiliser une prestation de service avec TVA ?",
        "a": (
            "L'écriture d'une prestation de service (honoraires) avec TVA (19%) est :\n"
            "Débit : 622 - Honoraires et frais d'experts (HT)\n"
            "Débit : 445 - TVA déductible (19%)\n"
            "Crédit : 401 - Fournisseurs (TTC)"
        ),
    },
    {
        "q": "Comment comptabiliser le paiement d'un salaire en Algérie ?",
        "a": (
            "Le paiement d'un salaire comprend plusieurs écritures :\n"
            "1) Enregistrement de la charge salariale :\n"
            "   Débit : 651 - Salaires et appointements\n"
            "   Crédit : 421 - Personnel - Rémunérations dues\n"
            "2) Cotisations salariales (CNAS 1,75%) :\n"
            "   Débit : 652 - Charges sociales\n"
            "   Crédit : 431 - CNAS\n"
            "3) Cotisations patronales (CNAS 26%) :\n"
            "   Débit : 652 - Charges sociales\n"
            "   Crédit : 431 - CNAS\n"
            "4) Paiement effectif :\n"
            "   Débit : 421 - Personnel\n"
            "   Débit : 431 - CNAS\n"
            "   Crédit : 521 - Banque"
        ),
    },
    {
        "q": "Comment comptabiliser un amortissement en Algérie ?",
        "a": (
            "L'écriture d'un amortissement est :\n"
            "Débit : 681 - Dotations aux amortissements d'exploitation\n"
            "Crédit : 28x - Amortissements des immobilisations\n\n"
            "En Algérie, les taux d'amortissement sont fixés par la réglementation. "
            "L'amortissement peut être linéaire ou dégressif selon le type d'immobilisation."
        ),
    },
    {
        "q": "Comment comptabiliser une provision pour créance douteuse ?",
        "a": (
            "L'écriture d'une provision pour créance douteuse est :\n"
            "Débit : 682 - Dotations aux provisions pour dépréciations\n"
            "Crédit : 491 - Dépréciations clients\n\n"
            "Si la créance est finalement recouvrée :\n"
            "Débit : 491 - Dépréciations clients\n"
            "Crédit : 782 - Reprises sur provisions"
        ),
    },
    {
        "q": "Comment comptabiliser une charge d'assurance ?",
        "a": (
            "L'écriture d'une charge d'assurance est :\n"
            "Débit : 6065 - Primes d'assurance\n"
            "Crédit : 401 - Fournisseurs\n\n"
            "Si l'assurance est payée d'avance, on utilise le compte 481 - Charges "
            "constatées d'avance pour la partie relative à l'exercice suivant."
        ),
    },
    {
        "q": "Comment comptabiliser un loyer ?",
        "a": (
            "L'écriture d'un loyer est :\n"
            "Débit : 6061 - Locations de terrains et bâtiments\n"
            "Crédit : 401 - Fournisseurs\n\n"
            "Si le loyer est payé d'avance :\n"
            "Débit : 341 - Charges constatées d'avance\n"
            "Crédit : 401 - Fournisseurs"
        ),
    },
    {
        "q": "Comment comptabiliser les charges constatées d'avance ?",
        "a": (
            "Les charges constatées d'avance (CCA) sont des charges payées avant l'exercice "
            "auquel elles se rapportent. En fin d'exercice :\n"
            "Débit : 481 - Charges constatées d'avance\n"
            "Crédit : 6xx - Charges concernées\n\n"
            "Au début de l'exercice suivant, on passe la contrepartie :\n"
            "Débit : 6xx - Charges concernées\n"
            "Crédit : 481 - Charges constatées d'avance"
        ),
    },
    {
        "q": "Comment comptabiliser les produits constatés d'avance ?",
        "a": (
            "Les produits constatés d'avance sont des revenus encaissés avant l'exercice "
            "auquel ils se rapportent. En fin d'exercice :\n"
            "Débit : 7xx - Produits concernés\n"
            "Crédit : 482 - Produits constatés d'avance\n\n"
            "Au début de l'exercice suivant :\n"
            "Débit : 482 - Produits constatés d'avance\n"
            "Crédit : 7xx - Produits concernés"
        ),
    },
    {
        "q": "Comment comptabiliser une facture d'acompte ?",
        "a": (
            "L'écriture d'une facture d'acompte est :\n"
            "Débit : 401 - Fournisseurs (ou 411 - Clients pour une facture client)\n"
            "Crédit : 709 - Ventes d'entreprises dégroupées (ou 609 - Achats d'entreprises dégroupées)\n"
            "Crédit : 443 - TVA collectée (19%)\n\n"
            "L'acompte est régularisé lors de la facture définitive."
        ),
    },
    {
        "q": "Comment comptabiliser un avoir ?",
        "a": (
            "L'écriture d'un avoir (note de crédit) est :\n"
            "Débit : 709 - Ventes d'entreprises dégroupées\n"
            "Débit : 443 - TVA collectée\n"
            "Crédit : 411 - Clients\n\n"
            "L'avoir annule partiellement ou totalement une facture précédente."
        ),
    },
    {
        "q": "Comment comptabiliser un rapprochement bancaire ?",
        "a": (
            "Le rapprochement bancaire consiste à comparer le compte 521 (Banque) avec le "
            "relevé bancaire. Les écarts sont dus à :\n"
            "- Chèques émis non présentés au paiement\n"
            "- Virements non encore comptabilisés\n"
            "Frais bancaires :\n"
            "Débit : 627 - Frais bancaires\n"
            "Crédit : 521 - Banque"
        ),
    },
    {
        "q": "Comment comptabiliser un emprunt bancaire ?",
        "a": (
            "L'écriture d'un emprunt bancaire est :\n"
            "Débit : 521 - Banque\n"
            "Crédit : 152 - Emprunts auprès des établissements de crédit\n\n"
            "Les remboursements :\n"
            "Débit : 152 - Emprunts\n"
            "Débit : 661 - Intérêts d'emprunts\n"
            "Crédit : 521 - Banque"
        ),
    },
    {
        "q": "Comment comptabiliser une immobilisation en cours ?",
        "a": (
            "L'écriture d'une immobilisation en cours est :\n"
            "Débit : 231 - Immobilisations corporelles en cours\n"
            "Crédit : 401 - Fournisseurs (ou 521 - Banque)\n\n"
            "Lors de la mise en service :\n"
            "Débit : 21x - Immobilisation corporelle\n"
            "Crédit : 231 - Immobilisations en cours"
        ),
    },
    {
        "q": "Comment comptabiliser une cession d'immobilisation ?",
        "a": (
            "L'écriture d'une cession d'immobilisation est :\n"
            "Débit : 521 - Banque (prix de vente)\n"
            "Débit : 28x - Amortissements (cumulés)\n"
            "Crédit : 21x - Immobilisation (valeur d'origine)\n"
            "Crédit : 771 - Produits des cessions d'immobilisations (ou Débit 671 si perte)"
        ),
    },
    {
        "q": "Comment comptabiliser une subvention d'investissement ?",
        "a": (
            "L'écriture d'une subvention d'investissement reçue est :\n"
            "Débit : 521 - Banque\n"
            "Crédit : 131 - Subventions d'investissement\n\n"
            "La subvention est constatée en fin d'exercice par une dotation :\n"
            "Débit : 131 - Subventions d'investissement\n"
            "Crédit : 74 - Subventions d'exploitation"
        ),
    },
    {
        "q": "Comment comptabiliser une provision réglementée ?",
        "a": (
            "Les provisions réglementées sont des provisions dont la constitution est prévue "
            "par la législation fiscale. Exemple :\n"
            "Débit : 681 - Dotations aux amortissements\n"
            "Crédit : 145 - Amortissements dérogatoires\n\n"
            "Ces provisions permettent de constituer des réserves fiscales déductibles."
        ),
    },
    {
        "q": "Comment comptabiliser une perte sur stock ?",
        "a": (
            "L'écriture d'une perte sur stock est :\n"
            "Débit : 642 - Pertes sur stocks\n"
            "Crédit : 3x - Stocks (compte concerné)\n\n"
            "La perte sur stock peut être constatée lors de l'inventaire. "
            "Elle est déductible du résultat fiscal si elle est justifiée."
        ),
    },
    {
        "q": "Comment comptabiliser un écart de conversion ?",
        "a": (
            "Les écarts de conversion résultent des variations de change entre la date "
            "d'inscription d'une créance ou dette en devise et la date de son règlement.\n"
            "Écart favorable :\n"
            "Débit : 522 - Banque\n"
            "Crédit : 25 - Écarts de conversion passif\n"
            "Écart défavorable :\n"
            "Débit : 25 - Écarts de conversion actif\n"
            "Crédit : 522 - Banque"
        ),
    },
    {
        "q": "Comment comptabiliser la taxe sur les salaires ?",
        "a": (
            "La taxe sur les salaires est de 1% sur les rémunérations brutes versées au personnel.\n"
            "Débit : 63 - Impôts et taxes\n"
            "Crédit : 447 - État - impôts retenus à la source\n\n"
            "Cette taxe est déclarée et payée mensuellement."
        ),
    },
    {
        "q": "Comment comptabiliser les honoraires avec retenue à la source ?",
        "a": (
            "L'écriture des honoraires avec retenue à la source (20%) est :\n"
            "Débit : 622 - Honoraires (montant HT)\n"
            "Crédit : 401 - Fournisseurs (80%)\n"
            "Crédit : 447 - Retenue à la source (20%)\n\n"
            "La retenue à la source est versée mensuellement à la DGI."
        ),
    },
    {
        "q": "Comment comptabiliser la TVA sur les achats et les ventes ?",
        "a": (
            "TVA collectée (ventes) :\n"
            "Débit : 411 - Clients (TTC)\n"
            "Crédit : 701 - Ventes (HT)\n"
            "Crédit : 443 - TVA collectée (19%)\n\n"
            "TVA déductible (achats) :\n"
            "Débit : 600 - Achats (HT)\n"
            "Débit : 445 - TVA déductible (19%)\n"
            "Crédit : 401 - Fournisseurs (TTC)\n\n"
            "TVA due = TVA collectée - TVA déductible"
        ),
    },
    {
        "q": "Comment comptabiliser une dotation aux amortissements dérogatoires ?",
        "a": (
            "L'amortissement dérogatoire résulte de la différence entre l'amortissement fiscal "
            "et l'amortissement comptable.\n"
            "Si l'amortissement fiscal est supérieur à l'amortissement comptable :\n"
            "Débit : 681 - Dotations aux amortissements\n"
            "Crédit : 145 - Amortissements dérogatoires\n\n"
            "Cela crée une provision réglementée déductible fiscalement."
        ),
    },
    {
        "q": "Comment comptabiliser une vente à l'export ?",
        "a": (
            "L'écriture d'une vente à l'export (TVA 0%) est :\n"
            "Débit : 411 - Clients étrangers\n"
            "Crédit : 701 - Ventes de marchandises (HT)\n\n"
            "La TVA est à 0% pour les exportations. Les factures doivent mentionner "
            "le numéro de TVA intracommunautaire du client et la mention 'Exonération de TVA'."
        ),
    },
    {
        "q": "Comment comptabiliser un prêt d'associé ?",
        "a": (
            "L'écriture d'un prêt d'associé est :\n"
            "Débit : 521 - Banque\n"
            "Crédit : 455 - Associés - compte courant\n\n"
            "Le remboursement :\n"
            "Débit : 455 - Associés - compte courant\n"
            "Crédit : 521 - Banque\n\n"
            "Les intérêts :\n"
            "Débit : 661 - Charges financières\n"
            "Crédit : 455 - Associés - compte courant"
        ),
    },

    # ============================================================
    # FORMES JURIDIQUES (15 exemples)
    # ============================================================
    {
        "q": "Quelle est la différence entre SARL et EURL en Algérie ?",
        "a": (
            "La SARL (Société À Responsabilité Limitée) et l'EURL (Entreprise Unipersonnelle "
            "À Responsabilité Limitée) sont deux formes de sociétés à responsabilité limitée :\n"
            "- SARL : 2 associés minimum, gérant (personne physique)\n"
            "- EURL : 1 associé unique, gérant (personne physique)\n"
            "Les deux ont un capital social librement fixé par les statuts."
        ),
    },
    {
        "q": "Qu'est-ce qu'une SNC en Algérie ?",
        "a": (
            "La SNC (Société en Nom Collectif) est une société dans laquelle tous les associés "
            "ont la qualité de commerçant et sont solidairement responsables des dettes sociales. "
            "Elle est dirigée par un ou plusieurs gérants. Le capital est divisé en parts sociales "
            "incessibles sauf agrément des associés."
        ),
    },
    {
        "q": "Qu'est-ce qu'une SPA en Algérie ?",
        "a": (
            "La SPA (Société Par Actions) est une société dont le capital est divisé en actions. "
            "Elle peut être privée ou publique. En Algérie, la SPA est soumise au droit des "
            "sociétés commerciales et doit avoir au moins 7 actionnaires. Le capital social "
            "est librement fixé par les statuts."
        ),
    },
    {
        "q": "Comment créer une SARL en Algérie ?",
        "a": (
            "Les étapes de création d'une SARL en Algérie :\n"
            "1) Rédaction des statuts (acte notarié ou sous-seing privé)\n"
            "2) Publication au Journal Officiel\n"
            "3) Dépôt du capital social auprès d'une banque\n"
            "4) Immatriculation au registre du commerce\n"
            "5) Déclaration auprès de la DGI pour les impôts\n"
            "6) Affiliation à la CNAS pour les salariés"
        ),
    },
    {
        "q": "Quelles sont les obligations d'une SARL en Algérie ?",
        "a": (
            "Les obligations principales d'une SARL :\n"
            "- Tenue d'une comptabilité régulière selon le SCF\n"
            "- Déclaration et paiement de la TVA (mensuel ou trimestriel)\n"
            "- Déclaration et paiement de l'IBS (19%)\n"
            "- Déclaration des salaires et paiement des cotisations CNAS\n"
            "- Tenue d'une assemblée générale annuelle\n"
            "- Dépôt des comptes annuels au greffe du tribunal"
        ),
    },
    {
        "q": "Quelle est la responsabilité des associés d'une SARL ?",
        "a": (
            "En SARL, la responsabilité des associés est limitée à leurs apports. "
            "Cela signifie que les associés ne sont pas personnellement responsables "
            "des dettes de la société. En cas de liquidation, ils ne risquent que "
            "la perte de leur investissement. Cependant, le gérant peut engager "
            "sa responsabilité personnelle en cas de faute de gestion."
        ),
    },
    {
        "q": "Comment est imposée une SARL en Algérie ?",
        "a": (
            "La SARL est soumise à l'IBS (Impôt sur les Sociétés) au taux de 19% "
            "sur son bénéfice net. Les dividendes distribués aux associés sont soumis "
            "à une retenue à la source de 10%. La SARL est également soumise à la "
            "taxe professionnelle et à la TVA."
        ),
    },
    {
        "q": "Quelle est la différence entre gérant statutaire et gérant libre ?",
        "a": (
            "Le gérant statutaire est désigné dans les statuts de la société. "
            "Sa révocation est plus complexe (nécessite une modification statutaire). "
            "Le gérant libre est désigné par une décision des associés en dehors des statuts. "
            "Sa révocation est plus simple (décision des associés). "
            "Les deux ont les mêmes pouvoirs de gestion."
        ),
    },
    {
        "q": "Qu'est-ce que le registre du commerce en Algérie ?",
        "a": (
            "Le registre du commerce est un registre tenu par le tribunal de commerce "
            "dans lequel sont inscrites toutes les sociétés commerciales. Il permet de :\n"
            "- Officialiser la création de la société\n"
            "- Publier les modifications statutaires\n"
            "- Informer les tiers sur la situation juridique de la société\n"
            "L'immatriculation est obligatoire pour toute société commerciale."
        ),
    },
    {
        "q": "Comment modifier les statuts d'une SARL ?",
        "a": (
            "La modification des statuts d'une SARL nécessite :\n"
            "1) Une décision des associés en assemblée générale extraordinaire\n"
            "2) La modification de l'acte constitutif\n"
            "3) La publication au Journal Officiel\n"
            "4) Le dépôt au greffe du tribunal de commerce\n"
            "5) La mise à jour du registre du commerce"
        ),
    },
    {
        "q": "Qu'est-ce qu'une société en commandite en Algérie ?",
        "a": (
            "La société en commandite est une société composée de deux catégories d'associés :\n"
            "- Les commandités : associés à responsabilité illimitée\n"
            "- Les commanditaires : associés à responsabilité limitée à leurs apports\n"
            "Elle est dirigée par un commandité. Le capital est divisé en parts sociales."
        ),
    },
    {
        "q": "Quelles sont les formalités de création d'une entreprise en Algérie ?",
        "a": (
            "Les formalités de création :\n"
            "1) Obtention du numéro d'identification fiscale (NIF) auprès de la DGI\n"
            "2) Rédaction des statuts (notarié ou sous-seing privé)\n"
            "3) Publication au Journal Officiel\n"
            "4) Dépôt du capital social\n"
            "5) Immatriculation au registre du commerce\n"
            "6) Affiliation à la CNAS\n"
            "7) Déclaration d'activité auprès de la wilaya"
        ),
    },
    {
        "q": "Qu'est-ce que le capital social d'une SARL ?",
        "a": (
            "Le capital social d'une SARL est le montant des apports réalisés par les associés. "
            "Il est librement fixé par les statuts. Le capital est divisé en parts sociales "
            "de valeur égale. Chaque associé est titulaire d'un certain nombre de parts. "
            "Le capital social constitue une garantie pour les créanciers de la société."
        ),
    },
    {
        "q": "Comment fonctionne l'assemblée générale en SARL ?",
        "a": (
            "L'assemblée générale en SARL peut être ordinaire ou extraordinaire :\n"
            "- AG ordinaire : approbation des comptes, affectation du résultat, nomination du gérant\n"
            "- AG extraordinaire : modification des statuts, augmentation de capital\n"
            "Les décisions sont prises à la majorité des associés représentant plus de la moitié "
            "du capital social. Les statuts peuvent prévoir des majorités plus strictes."
        ),
    },
    {
        "q": "Quelles sont les causes de dissolution d'une SARL ?",
        "a": (
            "Les causes de dissolution d'une SARL :\n"
            "- Décision des associés en assemblée générale extraordinaire\n"
            "- Fin de durée (expiration du terme)\n"
            "- Réalisation ou expiration de l'objet social\n"
            "- Dissolution anticipée par le tribunal (faillite)\n"
            "- Réduction du nombre d'associés en dessous de 2 (sauf EURL)\n"
            "La dissolution entraîne la liquidation de la société."
        ),
    },
    {
        "q": "Comment fonctionne la transmission de parts sociales en SARL ?",
        "a": (
            "La transmission des parts sociales en SARL est soumise à agrément des associés. "
            "L'associé cédant doit notifier sa volonté de céder ses parts aux autres associés. "
            "Les associés disposent d'un droit de préférence. En l'absence d'agrément, "
            "la cession est nulle. Les statuts peuvent prévoir des règles spécifiques."
        ),
    },

    # ============================================================
    # AUDIT (15 exemples)
    # ============================================================
    {
        "q": "Quels sont les objectifs de l'audit des comptes en Algérie ?",
        "a": (
            "Les objectifs de l'audit des comptes en Algérie sont :\n"
            "1) Donner une assurance raisonnable que les états financiers sont exempts d'anomalies significatives\n"
            "2) Émettre un avis sur la régularité, la sincérité et la fidélité des comptes\n"
            "3) Vérifier la conformité des comptes au SCF algérien\n"
            "4) Identifier les risques d'anomalies significatives\n"
            "5) Vérifier la conformité aux obligations fiscales"
        ),
    },
    {
        "q": "Qu'est-ce que la matérialité en audit ?",
        "a": (
            "La matérialité est le seuil au-delà duquel une erreur ou omission dans les états "
            "financiers peut influencer les décisions des utilisateurs. L'auditeur détermine "
            "un seuil de matérialité (souvent 5-10% du résultat net ou 0,5-1% du CA). "
            "Les anomalies supérieures à ce seuil sont considérées comme significatives."
        ),
    },
    {
        "q": "Quels sont les types d'opinion du commissaire aux comptes en Algérie ?",
        "a": (
            "Le commissaire aux comptes peut émettre 4 types d'opinion :\n"
            "1) Opinion sans réserve : les comptes sont réguliers et sincères\n"
            "2) Opinion avec réserve : des réserves portent sur des éléments déterminants\n"
            "3) Avis défavorable : les comptes ne sont pas réguliers ou sincères\n"
            "4) Abstention d'opinion : l'auditeur n'a pas pu se procurer les éléments nécessaires"
        ),
    },
    {
        "q": "Qu'est-ce qu'un test de contrôle en audit ?",
        "a": (
            "Un test de contrôle est une procédure d'audit destinée à évaluer l'efficacité "
            "du dispositif de contrôle interne de l'entreprise. Il vérifie si les procédures "
            "mises en place fonctionnent effectivement. Les résultats permettent à l'auditeur "
            "d'adapter l'étendue de ses procédures substantives."
        ),
    },
    {
        "q": "Qu'est-ce qu'une procédure substantielle ?",
        "a": (
            "Une procédure substantielle est une procédure d'audit destinée à détecter "
            "les anomalies significatives dans les comptes. Elle comprend : l'analyse "
            "des comptes, le test de détail, la confirmation externe, l'inspection, "
            "l'observation, le recalcul et la réconciliation."
        ),
    },
    {
        "q": "Qu'est-ce que le contrôle interne ?",
        "a": (
            "Le contrôle interne est l'ensemble des dispositifs mis en place par la direction "
            "d'une entreprise pour atteindre ses objectifs : fiabilité des informations "
            "financières, efficacité des opérations, conformité aux lois. Il comprend "
            "5 composantes : environnement de contrôle, évaluation des risques, "
            "activités de contrôle, information et communication, et pilotage."
        ),
    },
    {
        "q": "Quelle est la mission du commissaire aux comptes en Algérie ?",
        "a": (
            "Le commissaire aux comptes (CAC) a pour mission de :\n"
            "- Vérifier la sincérité et la régularité des comptes annuels\n"
            "- Contrôler la sincérité des informations financières\n"
            "- Signaler les faits de nature à compromettre la continuité de l'exploitation\n"
            "- Émettre un rapport sur les comptes annuels\n"
            "Il est désigné par l'assemblée générale des actionnaires."
        ),
    },
    {
        "q": "Quels sont les risques d'audit ?",
        "a": (
            "Les principaux risques d'audit sont :\n"
            "1) Risque de non-détectabilité : risque que l'auditeur ne détecte pas les anomalies\n"
            "2) Risque inhérent : risque que les comptes contiennent des anomalies significatives\n"
            "3) Risque de contrôle : risque que le contrôle interne ne prévienne pas les anomalies\n"
            "Le risque d'audit = risque inhérent × risque de contrôle × risque de non-détectabilité"
        ),
    },
    {
        "q": "Comment se déroule un audit des comptes en Algérie ?",
        "a": (
            "Le déroulement d'un audit :\n"
            "1) Phase de préparation : compréhension de l'entreprise et évaluation des risques\n"
            "2) Phase de travail : tests de contrôle et procédures substantives\n"
            "3) Phase de conclusion : évaluation des résultats et émission de l'opinion\n"
            "4) Phase de rapport : rédaction du rapport d'audit\n"
            "La durée dépend de la taille et de la complexité de l'entreprise."
        ),
    },
    {
        "q": "Qu'est-ce que la continuité d'exploitation en audit ?",
        "a": (
            "La continuité d'exploitation est un concept fondamental en audit. L'auditeur "
            "doit évaluer si l'entreprise est capable de poursuivre ses activités dans un "
            "avenir prévisible (12 mois). Il doit vérifier l'existence de tout indice "
            "d'incertitude significative pouvant affecter la continuité d'exploitation."
        ),
    },
    {
        "q": "Quelle est la différence entre audit interne et audit externe ?",
        "a": (
            "L'audit interne est exercé par un service de l'entreprise. Il évalue l'efficacité "
            "du contrôle interne et des procédures. L'audit externe est exercé par un commissaire "
            "aux comptes indépendant. Il vérifie la sincérité des comptes et émet un avis. "
            "Les deux sont complémentaires et collaborent souvent."
        ),
    },
    {
        "q": "Qu'est-ce que la confirmation externe en audit ?",
        "a": (
            "La confirmation externe est une procédure d'audit qui consiste à obtenir "
            "une réponse directe de tiers (clients, fournisseurs, banques) pour confirmer "
            "les montants ou les informations comptables. Elle est utilisée pour les soldes "
            "de comptes de tiers, les opérations importantes et les engagements hors bilan."
        ),
    },
    {
        "q": "Comment évaluer le contrôle interne en audit ?",
        "a": (
            "L'évaluation du contrôle interne comprend :\n"
            "1) Description des procédures existantes\n"
            "2) Test de conception : vérifier que les procédures sont adéquates\n"
            "3) Test d'efficacité : vérifier que les procédures fonctionnent\n"
            "4) Évaluation des faiblesses identifiées\n"
            "Les résultats orientent l'étendue des procédures substantives."
        ),
    },
    {
        "q": "Quels sont les documents examinés lors d'un audit ?",
        "a": (
            "Les principaux documents examinés :\n"
            "- États financiers (bilan, CPC, TCR)\n"
            "- Livres comptables (journaux, grands livres)\n"
            "- Justificatifs comptables (factures, relevés bancaires)\n"
            "- Procédures internes\n"
            "- Déclarations fiscales\n"
            "- PV d'assemblées générales\n"
            "- Contrats commerciaux"
        ),
    },
    {
        "q": "Qu'est-ce que l'audit légal en Algérie ?",
        "a": (
            "L'audit légal en Algérie est obligatoire pour certaines sociétés (SA, SPA, "
            "sociétés dépassant des seuils de CA et de total bilan). Le commissaire aux comptes "
            "est désigné par l'assemblée générale des actionnaires. Il émet un rapport "
            "sur les comptes annuels qui est annexé aux états financiers."
        ),
    },

    # ============================================================
    # DROIT COMMERCIAL (15 exemples)
    # ============================================================
    {
        "q": "Qu'est-ce qu'une procédure collective en Algérie ?",
        "a": (
            "Une procédure collective est une procédure judiciaire destinée aux entreprises "
            "en difficulté financière. Elle comprend :\n"
            "- Le redressement judiciaire : plan de redressement sur 5 ans max\n"
            "- La liquidation judiciaire : vente des actifs et dissolution\n"
            "Le tribunal désigne un administrateur ou un liquidateur pour gérer la procédure."
        ),
    },
    {
        "q": "Qu'est-ce que l'abus de biens sociaux en Algérie ?",
        "a": (
            "L'abus de biens sociaux est un délit commis par un dirigeant qui utilise les biens "
            "ou le crédit de la société contrairement à l'intérêt social et à des fins personnelles. "
            "C'est une infraction pénale punie de 5 ans d'emprisonnement et d'amendes. "
            "L'abus de pouvoir est un délit similaire."
        ),
    },
    {
        "q": "Quelles sont les formes de procédures collectives en Algérie ?",
        "a": (
            "Les procédures collectives en Algérie :\n"
            "- Sauvegarde : procédure préventive pour éviter le redressement\n"
            "- Redressement judiciaire : plan de redressement sur 5 ans maximum\n"
            "- Liquidation judiciaire : vente des actifs et dissolution\n"
            "Le tribunal compétent est le tribunal de commerce."
        ),
    },
    {
        "q": "Comment fonctionne le redressement judiciaire en Algérie ?",
        "a": (
            "Le redressement judiciaire est ouvert aux entreprises en état de cessation de paiement "
            "mais dont la survie est possible. Le tribunal désigne un administrateur. "
            "Un plan de redressement est élaboré sur 5 ans maximum. Les créanciers sont payés "
            "selon un calendrier échelonné. L'entreprise poursuit son activité."
        ),
    },
    {
        "q": "Comment fonctionne la liquidation judiciaire en Algérie ?",
        "a": (
            "La liquidation judiciaire est ouverte aux entreprises dont la cessation de paiement "
            "est définitive. Le tribunal désigne un liquidateur. Les actifs sont vendus et le "
            "produit est distribué aux créanciers selon un ordre de priorité. La société est "
            "radiée du registre du commerce."
        ),
    },
    {
        "q": "Qu'est-ce que le tribunal de commerce en Algérie ?",
        "a": (
            "Le tribunal de commerce est une juridiction spécialisée qui traite les litiges "
            "commerciaux. Il est compétent pour :\n"
            "- Les procédures collectives (redressement, liquidation)\n"
            "- Les litiges entre commerçants\n"
            "- Les contestations relatives aux actes de commerce\n"
            "Il est composé de juges élus par les commerçants."
        ),
    },
    {
        "q": "Qu'est-ce que le registre du commerce en Algérie ?",
        "a": (
            "Le registre du commerce est un registre public tenu par le greffe du tribunal "
            "de commerce. Il enregistre toutes les sociétés commerciales et les commerçants "
            "individuels. Il permet d'informé les tiers sur la situation juridique des entreprises. "
            "L'immatriculation est obligatoire pour exercer une activité commerciale."
        ),
    },
    {
        "q": "Quels sont les actes de commerce en Algérie ?",
        "a": (
            "Les actes de commerce comprennent :\n"
            "- Les achats de biens pour les revendre\n"
            "- Les opérations de banque et de change\n"
            "- Les entreprises de transport\n"
            "- Les entreprises de commission et de courtage\n"
            "- Les opérations sur effets de commerce\n"
            "Les actes de commerce sont soumis au droit commercial."
        ),
    },
    {
        "q": "Qu'est-ce qu'un chèque en Algérie ?",
        "a": (
            "Le chèque est un écrit par lequel le tireur donne l'ordre au tiré (banque) "
            "de payer une somme déterminée au porteur. En Algérie, le chèque est régi par "
            "la législation sur les effets de commerce. Le chèque sans provision est un délit "
            "pénal passible d'emprisonnement et d'amendes."
        ),
    },
    {
        "q": "Qu'est-ce qu'une lettre de change en Algérie ?",
        "a": (
            "La lettre de change est un effet de commerce par lequel le tireur donne l'ordre "
            "au tiré de payer une somme déterminée à une échéance donnée au bénéficiaire. "
            "Elle est utilisée pour les paiements à crédit entre commerçants. "
            "La lettre de change peut être escomptée auprès d'une banque."
        ),
    },
    {
        "q": "Qu'est-ce que le protêt en Algérie ?",
        "a": (
            "Le protêt est un acte authentique dressé par un huissier pour constater "
            "le non-paiement d'un effet de commerce (chèque, lettre de change). "
            "Il constitue une mise en demeure et permet au porteur d'exercer ses droits "
            "de recours contre les endosseurs et le tiré."
        ),
    },
    {
        "q": "Qu'est-ce que l'escompte en Algérie ?",
        "a": (
            "L'escompte est une opération par laquelle une banque avance le montant "
            "d'un effet de commerce avant son échéance. L'entreprise cède son effet "
            "à la banque qui lui verse le montant diminué d'une commission (agios). "
            "L'escompte peut être commercial ou bancaire."
        ),
    },
    {
        "q": "Quelles sont les sanctions pour chèque sans provision ?",
        "a": (
            "Le chèque sans provision est sanctionné par :\n"
            "- Une amende pénale proportionnelle au montant du chèque\n"
            "- L'interdiction d'émettre des chèques pendant 5 ans\n"
            "- L'inscription au fichier des chèques sans provision\n"
            "- Des poursuites pénales pouvant conduire à l'emprisonnement\n"
            "Le tireur peut régulariser la situation en provisionnant les fonds."
        ),
    },
    {
        "q": "Qu'est-ce que la commission de cautionnement en Algérie ?",
        "a": (
            "La commission de cautionnement est une rémunération versée à une banque "
            "ou une société de cautionnement pour garantir l'exécution d'une obligation. "
            "Elle est généralement de 1% à 3% du montant garanti par an. "
            "Elle est déductible du résultat fiscal."
        ),
    },
    {
        "q": "Comment fonctionne le recouvrement de créances en Algérie ?",
        "a": (
            "Le recouvrement de créances peut être :\n"
            "- Amiable : relances, négociation avec le débiteur\n"
            "- judiciaire :assignation devant le tribunal compétent\n"
            "- Par voie d'exécution : saisie des biens du débiteur\n"
            "Le tribunal compétent dépend du montant de la créance. "
            "Le délai de prescription est de 10 ans pour les créances commerciales."
        ),
    },

    # ============================================================
    # RATIOS FINANCIERS (15 exemples)
    # ============================================================
    {
        "q": "Comment calculer la liquidité générale en Algérie ?",
        "a": (
            "La liquidité générale se calcule ainsi :\n"
            "Liquidité générale = Actif circulant / Passif circulant\n\n"
            "Un ratio supérieur à 1 indique que l'entreprise peut couvrir ses dettes "
            "à court terme avec ses actifs à court terme. C'est un indicateur de la "
            "capacité de l'entreprise à faire face à ses obligations à court terme."
        ),
    },
    {
        "q": "Comment calculer l'endettement en Algérie ?",
        "a": (
            "Le ratio d'endettement se calcule ainsi :\n"
            "Endettement = Dettes totales / Capitaux propres\n\n"
            "Un ratio inférieur à 1 est généralement considéré comme sain, signifiant "
            "que les dettes de l'entreprise sont inférieures à ses capitaux propres. "
            "Ce ratio mesure la dépendance de l'entreprise au financement externe."
        ),
    },
    {
        "q": "Comment calculer la rentabilité nette en Algérie ?",
        "a": (
            "La rentabilité nette se calcule ainsi :\n"
            "Rentabilité nette = Résultat net / Chiffre d'affaires × 100\n\n"
            "Un ratio supérieur à 5% est généralement considéré comme bon. Ce ratio "
            "mesure la capacité de l'entreprise à dégager un bénéfice après toutes "
            "les charges et impôts."
        ),
    },
    {
        "q": "Qu'est-ce que le BFR en Algérie ?",
        "a": (
            "Le BFR (Besoin en Fonds de Roulement) est le besoin de financement "
            "permanent de l'activité courante. Il se calcule ainsi :\n"
            "BFR = Actif circulant - Passif circulant\n"
            "ou BFR = Stocks + Créances clients - Dettes fournisseurs\n"
            "Un BFR positif signifie que l'entreprise doit financer son activité courante. "
            "Un BFR négatif est favorable à la trésorerie."
        ),
    },
    {
        "q": "Comment calculer le délai moyen de paiement fournisseurs ?",
        "a": (
            "Le délai moyen de paiement fournisseurs (DMP) se calcule ainsi :\n"
            "DMP = Fournisseurs / Achats TTC × 360\n\n"
            "Ce ratio mesure le nombre de jours moyen que l'entreprise met pour "
            "payer ses fournisseurs. Un DMP de 30 à 60 jours est généralement "
            "considéré comme normal en Algérie."
        ),
    },
    {
        "q": "Comment calculer le délai moyen de recouvrement clients ?",
        "a": (
            "Le délai moyen de recouvrement clients (DMR) se calcule ainsi :\n"
            "DMR = Clients / Chiffre d'affaires TTC × 360\n\n"
            "Ce ratio mesure le nombre de jours moyen que l'entreprise met pour "
            "encaisser ses créances clients. Un DMR de 30 à 60 jours est "
            "généralement considéré comme acceptable."
        ),
    },
    {
        "q": "Comment calculer la productivité du personnel ?",
        "a": (
            "La productivité du personnel se calcule ainsi :\n"
            "Productivité = Chiffre d'affaires / Effectif moyen\n\n"
            "Ce ratio mesure la productivité moyenne de chaque salarié. "
            "Il permet de comparer la performance de l'entreprise avec celles "
            "du même secteur d'activité."
        ),
    },
    {
        "q": "Comment calculer le levier financier ?",
        "a": (
            "Le levier financier se calcule ainsi :\n"
            "Levier financier = Résultat financier / Capitaux propres\n\n"
            "Un levier positif indique que l'entreprise génère plus de revenus "
            "avec l'argent emprunté que le coût de cet emprunt. "
            "C'est un indicateur de l'efficacité du financement externe."
        ),
    },
    {
        "q": "Comment calculer la rentabilité des capitaux propres ?",
        "a": (
            "La rentabilité des capitaux propres (ROE) se calcule ainsi :\n"
            "ROE = Résultat net / Capitaux propres × 100\n\n"
            "Ce ratio mesure le rendement du capital investi par les associés. "
            "Un ROE supérieur à 10% est généralement considéré comme bon."
        ),
    },
    {
        "q": "Comment calculer la rotation des stocks ?",
        "a": (
            "La rotation des stocks se calcule ainsi :\n"
            "Rotation = Achats / Stock moyen\n\n"
            "Ce ratio mesure le nombre de fois où les stocks sont renouvelés "
            "pendant l'exercice. Une rotation élevée indique une bonne gestion "
            "des stocks et un besoin en fonds de roulement réduit."
        ),
    },
    {
        "q": "Comment calculer l'autonomie financière ?",
        "a": (
            "L'autonomie financière se calcule ainsi :\n"
            "Autonomie financière = Capitaux propres / Total du bilan × 100\n\n"
            "Un ratio supérieur à 50% indique que l'entreprise est principalement "
            "financée par ses propres ressources. C'est un gage de solidité financière."
        ),
    },
    {
        "q": "Comment calculer le besoin en fonds de roulement de gestion ?",
        "a": (
            "Le BFR de gestion se calcule ainsi :\n"
            "BFR = Stocks + Créances clients - Dettes fournisseurs - Dettes fiscales\n\n"
            "Le BFR de gestion tient compte des dettes fiscales (TVA, impôts) "
            "qui constituent un financement gratuit pour l'entreprise. "
            "Un BFR de gestion positif nécessite un financement."
        ),
    },
    {
        "q": "Quels sont les indicateurs de santé financière en Algérie ?",
        "a": (
            "Les principaux indicateurs :\n"
            "- Liquidité générale > 1\n"
            "- Endettement < 1\n"
            "- Rentabilité nette > 5%\n"
            "- BFR maîtrisé\n"
            "- DMP et DMR dans les normes du secteur\n"
            "Ces indicateurs permettent d'évaluer la santé financière de l'entreprise."
        ),
    },
    {
        "q": "Comment analyser la structure financière d'une entreprise ?",
        "a": (
            "L'analyse de la structure financière comprend :\n"
            "1) Analyse du passif : répartition capitaux propres/dettes\n"
            "2) Analyse de l'actif : répartition immobilisations/actif circulant\n"
            "3) Analyse des emplois-ressources : équilibre financier\n"
            "4) Analyse des ratios d'autonomie et d'endettement\n"
            "Cette analyse permet d'évaluer la solidité financière de l'entreprise."
        ),
    },
    {
        "q": "Comment calculer le ratio de solvabilité ?",
        "a": (
            "Le ratio de solvabilité se calcule ainsi :\n"
            "Solvabilité = Total de l'actif / Total du passif\n\n"
            "Un ratio supérieur à 1 indique que l'entreprise est solvable, "
            "c'est-à-dire capable de payer l'ensemble de ses dettes avec la "
            "valeur de l'ensemble de ses actifs."
        ),
    },

    # ============================================================
    # BANQUES ET PAIEMENTS (15 exemples)
    # ============================================================
    {
        "q": "Quelles sont les principales banques en Algérie ?",
        "a": (
            "Les principales banques en Algérie :\n"
            "- CNEP (Caisse Nationale d'Épargne et de Prévoyance)\n"
            "- BADR (Banque de l'Agriculture et du Développement Rural)\n"
            "- BEA (Banque Extérieure d'Algérie)\n"
            "- BNA (Banque Nationale d'Algérie)\n"
            "- CPA (Crédit Populaire d'Algérie)\n"
            "- Société Générale Algérie\n"
            "- Banque Algeria"
        ),
    },
    {
        "q": "Quels sont les modes de paiement en Algérie ?",
        "a": (
            "Les principaux modes de paiement :\n"
            "- Chèque : écrit donnant l'ordre à la banque de payer\n"
            "- Virement bancaire : transfert de fonds entre comptes\n"
            "- Lettre de change : effet de commerce à échéance\n"
            "- Espèces : paiement en liquide (limité à 100 000 DA)\n"
            "- Carte bancaire : paiement électronique"
        ),
    },
    {
        "q": "Comment fonctionne un virement bancaire en Algérie ?",
        "a": (
            "Le virement bancaire est un ordre de transfert de fonds d'un compte à un autre. "
            "Il peut être :\n"
            "- Virement interne : entre comptes de la même banque\n"
            "- Virement externe : entre comptes de banques différentes\n"
            "Le virement est exécuté sous 1 à 3 jours ouvrés. "
            "Les frais sont variables selon les banques."
        ),
    },
    {
        "q": "Qu'est-ce qu'un chèque de banque en Algérie ?",
        "a": (
            "Un chèque de banque est un chèque émis par la banque elle-même. "
            "Il garantit le paiement car les fonds sont immédiatement bloqués "
            "sur le compte de la banque. Il est utilisé pour les transactions "
            "importantes où la garantie de paiement est nécessaire."
        ),
    },
    {
        "q": "Quelles sont les conditions pour ouvrir un compte bancaire en Algérie ?",
        "a": (
            "Les conditions pour ouvrir un compte bancaire :\n"
            "- Être majeur ou avoir l'autorisation du tuteur\n"
            "- Fournir une pièce d'identité en cours de validité\n"
            "- Justifier d'un domicile\n"
            "- Pour les entreprises : Kbis, statuts, NIF\n"
            "L'ouverture de compte est gratuite dans la plupart des banques."
        ),
    },
    {
        "q": "Comment fonctionne l'escompte commercial en Algérie ?",
        "a": (
            "L'escompte commercial est une opération par laquelle une banque avance "
            "le montant d'un effet de commerce avant son échéance. L'entreprise cède "
            "son effet à la banque qui lui verse le montant diminué des agios. "
            "Les agios sont calculés en fonction du taux d'escompte et du nombre "
            "de jours restant avant l'échéance."
        ),
    },
    {
        "q": "Qu'est-ce qu'un crédit documentaire en Algérie ?",
        "a": (
            "Le crédit documentaire est un engagement bancaire de payer le bénéficiaire "
            "(exportateur) contre remise de documents conformes. Il garantit au vendeur "
            "le paiement et à l'acheteur la réception des marchandises. "
            "Il est utilisé principalement dans le commerce international."
        ),
    },
    {
        "q": "Quelles sont les garanties bancaires en Algérie ?",
        "a": (
            "Les principales garanties bancaires :\n"
            "- Caution bancaire : engagement de payer en cas de défaillance\n"
            "- Hypothèque : garantie immobilière\n"
            "- Nantissement : garantie sur des biens mobiliers\n"
            "- Privilège : droit de préférence sur certains biens\n"
            "Les garanties sont demandées lors de l'octroi de crédits."
        ),
    },
    {
        "q": "Comment fonctionne un crédit bancaire en Algérie ?",
        "a": (
            "Un crédit bancaire est un prêt accordé par une banque à un emprunteur. "
            "Les conditions sont :\n"
            "- Taux d'intérêt : fixe ou variable\n"
            "- Durée : selon le type de crédit\n"
            "- Garanties : hypothèque, caution, nantissement\n"
            "- Remboursement : mensualités constantes ou variables\n"
            "Le crédit peut être à court, moyen ou long terme."
        ),
    },
    {
        "q": "Qu'est-ce que la facilité de caisse en Algérie ?",
        "a": (
            "La facilité de caisse est un découvert bancaire autorisé. Elle permet "
            "à l'entreprise de maintenir un solde débiteur sur son compte courant "
            "dans la limite d'un montant préalablement agréé. Les agios sont calculés "
            "sur le montant utilized et la durée du découvert."
        ),
    },
    {
        "q": "Comment fonctionne le rapprochement bancaire ?",
        "a": (
            "Le rapprochement bancaire consiste à comparer le compte 521 (Banque) "
            "du journal de caisse avec le relevé bancaire. Les écarts sont dus à :\n"
            "- Chèques émis non encore présentés\n"
            "- Virements non encore comptabilisés\n"
            "- Frais bancaires non encore enregistrés\n"
            "Il doit être effectué mensuellement."
        ),
    },
    {
        "q": "Quels sont les types de comptes bancaires en Algérie ?",
        "a": (
            "Les principaux types de comptes :\n"
            "- Compte courant : pour les opérations courantes\n"
            "- Compte d'épargne : pour constituer une épargne\n"
            "- Compte à terme : pour un placement à durée déterminée\n"
            "- Compte professionnel : pour les entreprises\n"
            "Chaque compte a ses spécificités en termes de frais et de services."
        ),
    },
    {
        "q": "Comment régler une facture par chèque en Algérie ?",
        "a": (
            "Le règlement par chèque :\n"
            "1) Le tireur remplit un chèque avec le montant de la facture\n"
            "2) Il le signe et le remet au bénéficiaire\n"
            "3) Le bénéficiaire le dépose auprès de sa banque\n"
            "4) La banque du tireur procède au virement\n"
            "Le chèque doit être provisionné sous peine de sanctions pénales."
        ),
    },
    {
        "q": "Comment fonctionne la compensation bancaire en Algérie ?",
        "a": (
            "La compensation bancaire est un système centralisé qui permet de régler "
            "les créances et dettes entre banques. Les chèques et effets de commerce "
            "sont compensés automatiquement entre les établissements bancaires. "
            "Elle permet de réduire les transferts de fonds et de sécuriser les paiements."
        ),
    },
    {
        "q": "Qu'est-ce que le financement commercial en Algérie ?",
        "a": (
            "Le financement commercial comprend les crédits accordés par les fournisseurs "
            "à leurs clients. Il peut prendre la forme de :\n"
            "- Délais de paiement : 30, 60 ou 90 jours\n"
            "- Escomptes de paiement anticipé\n"
            "- Crédit documentaire\n"
            "Le financement commercial est un élément important du BFR."
        ),
    },
    {
        "q": "Qu'est-ce que le chiffre d'affaires en Algérie ?",
        "a": (
            "Le chiffre d'affaires (CA) est le montant total des ventes de biens et services "
            "réalisées par une entreprise pendant un exercice. Il est exprimé en dinars algériens (DA) "
            "et correspond au montant HT des factures émises. Le CA est le chiffre d'affaires de référence "
            "pour le calcul de la taxe professionnelle et pour apprécier la taille de l'entreprise."
        ),
    },
]


def create_dataset(output_path: str = "comptable_dataset_algerien.jsonl"):
    with open(output_path, "w", encoding="utf-8") as f:
        for item in DATA:
            record = {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": item["q"]},
                    {"role": "assistant", "content": item["a"]},
                ]
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Dataset créé : {output_path}")
    print(f"Nombre d'exemples : {len(DATA)}")


if __name__ == "__main__":
    create_dataset()
