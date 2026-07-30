# 🇩🇿 Comptable-SLM — Assistant IA pour la Comptabilité Algérienne

**Comptable-SLM** est un assistant IA spécialisé dans la comptabilité, la fiscalité et l'audit algériens.

👉 **Démo en ligne** : https://huggingface.co/spaces/votre-espace  *(à venir)*
👉 **Code source** : https://github.com/votre-compte/comptable-slm *(à créer)*

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
│  534 chunks (SCF + lois)  │  150 exemples algériens        │
├─────────────────────────────────────────────────────────────┤
│  🏗️ En développement : Extraction factures (Docling+Qwen) │
│  🏗️ En développement : Analyseur Grand Livre (Python)      │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Fonctionnalités

| Fonctionnalité | Status |
|---------------|--------|
| ✅ Questions/Réponses sur le SCF | ✅ Prêt |
| ✅ TVA, IBS, IRG, charges sociales | ✅ Prêt |
| ✅ SARL, EURL, droit des sociétés | ✅ Prêt |
| ✅ Écritures comptables | ✅ Prêt |
| 🔄 Extraction factures (OCR+IA) | 🔄 En test |
| 🔄 Analyseur Grand Livre / Audit | 🔄 En test |
| 📱 Interface web | 🚧 À venir |
| 🌍 Support OHADA | 📅 Planifié |

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

🔹 Basé sur Llama 3.2 fine-tuné + RAG
🔹 Connaît le SCF, la TVA, l'IBS, l'IRG, les charges sociales
🔹 100% adapté au contexte algérien
🔹 Démo disponible (lien en commentaire)

#Comptabilité #Algérie #IA #SCF #Audit #Innovation #ExpertComptable
```

---

## 📞 Contact

Créé par un **Expert-comptable & Auditeur légal** algérien, 
développeur amateur passionné par l'IA.

📧 Votre.Email@example.com
🔗 linkedin.com/in/votre-profil

---

*"L'IA doit servir les professionnels africains, pas l'inverse."*
