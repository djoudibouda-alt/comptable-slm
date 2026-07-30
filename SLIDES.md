# Slides – Comptable-SLM

---

## Slide 1 : Le Problème
**Les outils IA ne connaissent pas la comptabilité africaine.**

- Chaque pays africain a ses propres règles (SCF, TVA, charges sociales)
- ChatGPT / LLM génériques hallucinent sur le droit africain
- Les comptables africains sont sous-équipés

---

## Slide 2 : La Solution
**Comptable-SLM**

Assistant IA spécialisé en comptabilité et audit algériens.

- ✅ Réponses sourcées (pas d'hallucinations)
- ✅ Fonctionne hors ligne (zones sans internet)
- ✅ Connaît le SCF, la TVA algérienne, le droit des sociétés

---

## Slide 3 : Comment ça marche ?

```
Question → RAG (recherche dans la loi SCF, le code fiscal...)
         → Contexte + Question → LLM (Llama 3.2 fine-tuné)
         → Réponse précise avec sources
```

- **RAG** : embeddings NVIDIA NIM + ChromaDB (534 chunks)
- **SLM** : Llama 3.2 3B fine-tuné avec Unsloth/QLoRA
- **Inférence** : cloud (NVIDIA NIM) ou local (Ollama)

---

## Slide 4 : Innovation
| Technologie | Pourquoi c'est innovant |
|-------------|------------------------|
| NVIDIA NIM | Embeddings état-de-l'art |
| ChromaDB | Vector store local, privé |
| Unsloth/QLoRA | Fine-tuning 2x plus rapide |
| GGUF + Ollama | Déploiement hors ligne |

---

## Slide 5 : Marché
- **15 000** experts-comptables en Algérie
- **50 000+** professionnels comptables
- **16 pays** OHADA (Afrique francophone)
- **500 000+** comptables en Afrique francophone

---

## Slide 6 : Roadmap
| 3 mois | 6 mois |
|--------|--------|
| Dataset 1 000+ exemples | Modules pays (Maroc, Tunisie, Sénégal) |
| Support OHADA | Application mobile |
| Interface web | Intégration logiciels compta |
| Beta test 20 cabinets | |

---

## Slide 7 : Pourquoi Google AI Lab ?
- Accès anticipé **Gemini / Gemma**
- Mentorat technique **Google Research**
- Réseau de **VCs africains** (4DX, Norrsken, Novastar)
- Passer de l'Algérie à l'Afrique

---

## Slide 8 : L'Équipe
**Expert-comptable & Auditeur légal** | Développeur amateur IA

- 15+ ans d'expérience en comptabilité algérienne
- Connaissance du SCF, fiscalité, audit, droit social
- A construit ce projet seul, de A à Z

---

## Slide 9 : Démo
1. *"Quels sont les taux de TVA en Algérie ?"*
2. *"Différence entre SARL et EURL ?"*
3. *"Comment comptabiliser un achat avec TVA 19% ?"*

RAG + modèle fine-tuné → réponses précises en français.
