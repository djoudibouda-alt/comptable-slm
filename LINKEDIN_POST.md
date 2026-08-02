# Post LinkedIn — Comptable-SLM

## Texte du post

🇩🇿 **J'ai le plaisir de vous présenter Comptable-SLM, un assistant IA 100% adapté à la comptabilité et l'audit algériens.**

---

### Le problème 🤔

Les outils IA actuels (ChatGPT, Claude, etc.) sont entraînés sur des données US/EU. Ils **hallucinent** dès qu'on leur parle de droit comptable africain :

❌ TVA 19%/9%/0% ? → Réponses françaises
❌ SCF vs PCN ? → Confusion totale
❌ CNAS / CASNOS ? → Inventés
❌ SARL / EURL / SPA ? → Mélangés
❌ IBS / IRG ? → Barèmes étrangers

### La solution ✅

**Comptable-SLM** = RAG + SLM fine-tuné sur le droit comptable algérien

🔹 **Pipeline RAG** : 7 fichiers knowledge base (SCF, fiscalité, audit, charges sociales, droit commercial, formes juridiques, procédures)
🔹 **125 Q&A curées** : questions naturelles + réponses concises rédigées
🔹 **TF-IDF accent-insensitive** : matching robuste (déductible = déductible, declaration = déclaration)
🔹 **Réponses sourcées** : chaque réponse cite sa source (fichier + section)
🔹 **Fallback intelligent** : "Je ne sais pas" plutôt qu'hallucination
🔹 **Prêt pour l'offline** : Llama 3.2 3B fine-tuné (Unsloth/QLoRA) → GGUF → Ollama

### Ce qu'il répond parfaitement 🎯

| Sujet | Exemples |
|-------|----------|
| **TVA** | Taux, comptes 4455/4456/4457, déclaration, écritures achat/vente |
| **IBS** | Taux 19%, calcul, acomptes, assujettis |
| **IRG** | Barème mensuel 2024, retenue à la source, compte 4431 |
| **SARL/EURL** | Différences, capital 100k DA, création, commissaire aux comptes |
| **CNAS/CASNOS** | Taux, régimes, déclaration, allocations familiales |
| **Audit** | Normes ISA, commissaire aux comptes, obligations |
| **Écritures** | Achat TVA 19%, vente, amortissement, provision |
| **Procédures** | Calendrier fiscal, clôture exercice, rapprochement bancaire |

### Résultats tests 📊

**37/37** questions testées → réponses pertinentes
- "Quels sont les taux de TVA en Algérie ?" ✅
- "Différence entre SARL et EURL ?" ✅
- "TVA déductible ?" ✅
- "Comment déclarer la TVA ?" ✅
- "Congés payés ?" ✅
- "Bilan comptable ?" ✅
- "CNAS ?" ✅
- etc.

---

### 🚀 Démo en ligne (lien permanent)

👉 **https://comptable-slm-1.onrender.com**

Interface Gradio légère, hébergée sur Render (plan Free, lien permanent).

---

### 🎯 Public cible

- Experts-comptables & Commissaires aux comptes algériens
- Comptables agréés, étudiants en comptabilité/fiscalité
- Cabinets d'audit et de conseil
- Développeurs IA spécialisés domaine africain

---

### 🔮 Roadmap

- **3 mois** : Dataset 1000+ exemples, support OHADA (16 pays), beta test 20 cabinets
- **6 mois** : Modules Maroc/Tunisie/Sénégal, app mobile, intégration logiciels compta
- **Vision** : L'assistant IA panafricain de référence pour la comptabilité

---

### 🤝 Pourquoi Google Africa Applied AI Lab ?

Nous postulons pour :
- Accès anticipé **Gemini / Gemma** (requêtes multi-pays complexes)
- Mentorat technique **Google Research** (RAG + fine-tuning)
- Réseau **VCs africains** (4DX, Norrsken, Novastar) pour scaling OHADA

---

**L'IA doit servir les professionnels africains, pas l'inverse.** 💪

#Comptabilité #Algérie #IA #SCF #Audit #Innovation #ExpertComptable #GoogleAI #LLM #RAG #FineTuning #AfricaTech

---

## Variantes pour carrousel (slides)

Voir fichiers générés : `slides/` (10 PNG) + `Comptable_SLM_Pitch.pptx`