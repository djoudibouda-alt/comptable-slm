# Pitch – Comptable-SLM
## Google Africa Applied AI Lab

---

## 1. Le Problème

**La comptabilité en Afrique est fragmentée et complexe.**

Chaque pays a son propre système fiscal, plan comptable et cadre réglementaire. Rien qu'en Algérie :
- Le SCF a remplacé l'ancien PCN en 2007
- La TVA a 3 taux (19%, 9%, 0%) avec des règles spécifiques
- Les charges sociales impliquent CNAS et CASNOS avec différents régimes
- Les formes juridiques (SARL, EURL, SPA, SNC) ont des obligations distinctes

Les outils IA existants sont entraînés sur des données américaines/européennes et hallucinent dès qu'on leur parle de droit africain. Les comptables se débrouillent avec des PDF éparpillés, des manuels obsolètes ou des consultants coûteux.

## 2. La Solution

**Comptable-SLM : un assistant IA entraîné spécifiquement sur les cadres comptables africains.**

- **Pipeline RAG** : recherche instantanée dans une base de connaissances algérienne (loi SCF, code fiscal, normes d'audit)
- **SLM fine-tuné** : Llama 3.2 3B entraîné sur 150+ scénarios comptables réels, déployable hors ligne via Ollama
- **Toujours fiable** : les réponses citent leurs sources ; un filtre de distance élimine les hallucinations

## 3. Innovation Technique

| Composant | Technologie | Pourquoi |
|-----------|-------------|----------|
| Embeddings | NVIDIA Nemotron-3-Embed-1B (NIM) | Précision de recherche optimale |
| Stockage vectoriel | ChromaDB (cosinus, persistant) | Rapide, local, respect de la vie privée |
| LLM Cloud | Llama 3.1 8B Instruct | Raisonnement complexe |
| SLM Local | Llama 3.2 3B (fine-tuné, 4-bit) | Fonctionne sans internet |
| Fine-tuning | Unsloth + QLoRA | 2x plus rapide, faible VRAM |

**Différenciateur clé** : La plupart des outils IA comptables utilisent des LLM génériques. Le nôtre est fine-tuné sur des données africaines et fonctionne hors ligne — critique pour les zones à connectivité limitée.

## 4. Opportunité de Marché

- **Algérie** : ~15 000 experts-comptables + 50 000+ professionnels de la comptabilité
- **Zone OHADA** (16 pays africains) : cadre comptable unifié en Afrique de l'Ouest et Centrale
- **Potentiel panafricain** : 54 pays, chacun avec ses propres systèmes fiscaux et comptables

TAM initial : plus de 500 000 professionnels comptables en Afrique francophone.

## 5. Avancement & Roadmap

**Réalisé :**
- ✅ Pipeline RAG fonctionnel (base algérienne, 534 chunks)
- ✅ SLM fine-tuné sur 150 exemples algériens (loss : 1,89 → 0,03)
- ✅ Inférence locale via Ollama (export GGUF prêt)
- ✅ Base de connaissances : loi SCF, fiscalité, audit, charges sociales, droit commercial

**Prochains 3 mois :**
- Étendre le dataset à 1 000+ exemples
- Ajouter les normes comptables OHADA (16 pays)
- Interface web simple (Gradio/Streamlit)
- Beta test avec 10-20 cabinets algériens

**Prochains 6 mois :**
- Modules pays (Maroc, Tunisie, Sénégal, Côte d'Ivoire)
- Application mobile
- Intégration avec logiciels comptables

## 6. Pourquoi Google Africa Applied AI Lab ?

Nous avons besoin de :
- **Accès anticipé à Gemini / Gemma** – pour expérimenter sur des requêtes multi-pays complexes
- **Mentorat technique** – pour optimiser le pipeline RAG et le fine-tuning
- **Support go-to-market** – pour toucher les professionnels comptables en Afrique
- **Réseau de VCs** – pour passer de l'Algérie à la zone OHADA et au-delà

## 7. L'Équipe

**Expert-comptable & Auditeur légal** | Développeur amateur passionné par l'IA

- Plus de 15 ans d'expérience en comptabilité, audit et fiscalité algérienne
- Connaissance approfondie du SCF, du droit fiscal algérien (IBS, IRG, TVA), des charges sociales (CNAS, CASNOS)
- A construit ce projet de A à Z : pipeline RAG, fine-tuning, création du dataset
- Devise : *"L'IA doit servir les professionnels africains, pas l'inverse"*

## 8. Démo

Je peux montrer :
1. **Requête RAG** : *"Quels sont les taux de TVA en Algérie ?"* → cite la loi SCF
2. **Modèle fine-tuné** : *"Différence entre SARL et EURL ?"* → réponse précise en français
3. **Inférence hors ligne** : le modèle tourne localement via Ollama, sans cloud
