# 🇩🇿 Comptable-SLM — Assistant IA pour la Comptabilité Algérienne

**Comptable-SLM** est un assistant IA spécialisé dans la comptabilité, la fiscalité et l'audit algériens.

👉 **Démo en ligne** : https://comptable-slm-1.onrender.com
👉 **Code source** : https://github.com/djoudibouda-alt/comptable-slm

---

## 🚀 Pourquoi Comptable-SLM ?

Les outils IA actuels (ChatGPT, Claude, etc.) sont entraînés sur des données américaines/européennes. Ils **hallucinent** quand on leur pose des questions sur :

- Le **SCF** (Système Comptable et Financier algérien)
- La **TVA** algérienne (19%, 9%, 0%)
- Les charges sociales **CNAS / CASNOS**
- Les formes juridiques **SARL / EURL / SPA**
- L'**IBS**, l'**IRG**, la fiscalité algérienne

**Comptable-SLM résout ce problème.**

---

## 🧠 Architecture Technique

```
┌─────────────────────────────────────────────────────────────┐
│                    Comptable-SLM                             │
├─────────────────────────────────────────────────────────────┤
│  🔍 RAG Pipeline          │  🧠 SLM Fine-tuné              │
│  NVIDIA NIM Embeddings    │  Llama 3.2 3B (4-bit)          │
│  ChromaDB Vector Store    │  Unsloth + QLoRA               │
│  534 chunks (7 fichiers)  │  150 exemples algériens        │
│  Section-based chunking   │  GGUF → Ollama (local)         │
├─────────────────────────────────────────────────────────────┤
│  🎯 TF-IDF Search (word-level, accent-insensitive)         │
│  📚 125 Q&A curées — questions naturelles + réponses       │
│  ✅ Réponses sourcées  |  🛡️ Fallback intelligent          │
├─────────────────────────────────────────────────────────────┤
│  🏗️ En test : Extraction factures (Docling + Qwen 2.5)     │
│  🏗️ En test : Analyseur Grand Livre (audit)                │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Fonctionnalités

| Fonctionnalité | Status |
|---------------|--------|
| ✅ Questions/Réponses sur le SCF | ✅ Prêt (125 Q&A) |
| ✅ TVA (taux, comptes 4455/4456/4457, déclaration) | ✅ Prêt |
| ✅ IBS 19%, IRG barème 2024, retenue source | ✅ Prêt |
| ✅ CNAS 7% / CASNOS 15%, allocations familiales | ✅ Prêt |
| ✅ SARL / EURL / SPA / SNC, registre commerce | ✅ Prêt |
| ✅ Audit (normes ISA, commissaire aux comptes) | ✅ Prêt |
| ✅ Écritures comptables (achat, vente, amort., provision) | ✅ Prêt |
| ✅ Procédures (calendrier fiscal, clôture, rapprochement) | ✅ Prêt |
| 🔄 Extraction factures (Docling + Qwen 2.5) | 🔄 En test (100 factures Kaggle) |
| 🔄 Analyseur Grand Livre / Audit | 🔄 En test (Python) |
| 📱 Démo web Gradio (Render) | ✅ **En ligne** |
| 🌍 Support OHADA (16 pays) | 📅 Planifié (3 mois) |

---

## 🎯 Public Cible

- **Experts-comptables** algériens
- **Commissaires aux comptes**
- **Comptables agréés**
- **Étudiants** en comptabilité/fiscalité
- **Cabinets** d'audit et de conseil

---

## 📦 Installation & Test

### Option 1 : Démo légère (recommandé pour tester)

```bash
# 1. Installer Python 3.10+
# 2. Installer Gradio
pip install gradio

# 3. Lancer la démo
python comptable_demo_light.py

# 4. Ouvrir http://127.0.0.1:7860
```

### Option 2 : Version complète (avec RAG)

```bash
# 1. Cloner le repo
git clone https://github.com/votre-compte/comptable-slm
cd comptable-slm

# 2. Installer les dépendances
pip install -r requirements.txt
pip install gradio

# 3. Configurer la clé API NVIDIA NIM
# Copier .env.example vers .env et ajouter votre clé

# 4. Lancer la démo complète
python comptable_demo.py
```

---

## 📝 Publication LinkedIn (suggestion)

```
🇩🇿 J'ai le plaisir de vous présenter Comptable-SLM, 
un assistant IA spécialisé dans la comptabilité et l'audit algériens.

🔹 Basé sur Llama 3.2 fine-tuné + RAG (125 Q&A curées)
🔹 Connaît le SCF, la TVA (19/9/0%), l'IBS (19%), l'IRG (barème 2024)
🔹 CNAS/CASNOS, SARL/EURL/SPA, audit, écritures comptables
🔹 TF-IDF accent-insensitive — matching robuste
🔹 Réponses sourcées, fallback intelligent (pas d'hallucination)
🔹 Démo en ligne (lien permanent) : https://comptable-slm-1.onrender.com
🔹 Code : github.com/djoudibouda-alt/comptable-slm
🔹 Carrousel slides : 10 PNG dans /slides + PPTX modifiable

Postule à Google Africa Applied AI Lab 🚀

#Comptabilité #Algérie #IA #SCF #Audit #Innovation #ExpertComptable #GoogleAI #LLM #RAG #AfricaTech
```

---

## 📞 Contact

Créé par un **Expert-comptable & Auditeur légal** algérien (15+ ans d'expérience), 
développeur amateur passionné par l'IA.

🔗 GitHub : github.com/djoudibouda-alt
🔗 LinkedIn : linkedin.com/in/djoudibouda

---

*"L'IA doit servir les professionnels africains, pas l'inverse."*
