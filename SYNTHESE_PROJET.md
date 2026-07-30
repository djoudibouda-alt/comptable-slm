# Projet Comptable-SLM / *Comptable-SLM Project*

## Assistant IA spécialisé en comptabilité et audit algériens
## *AI Assistant for Algerian Accounting & Audit*

---

**Français**

### Présentation

Comptable-SLM est un assistant intelligent spécialisé dans la comptabilité et l'audit algériens, combinant un pipeline RAG (Retrieval-Augmented Generation) et un Small Language Model (SLM) fine-tuné. Le projet vise à fournir aux experts-comptables, commissaires aux comptes et comptables agréés algériens un outil de référence fiable pour le Système Comptable et Financier (SCF), la fiscalité algérienne (IBS, TVA, IRG), les charges sociales (CNAS, CASNOS) et le droit commercial.

### Architecture technique

- **RAG Pipeline** : Embeddings via NVIDIA NIM (Nemotron-3-Embed-1B), stockage vectoriel ChromaDB (similarité cosinus), chunking par sections (534 chunks), seuil de distance < 0.6
- **LLM Cloud** : Llama 3.1 8B Instruct via NVIDIA NIM API
- **SLM Local** : Llama 3.2 3B fine-tuné avec Unsloth/QLoRA (4-bit), exporté en GGUF pour Ollama
- **Dataset** : 150 exemples algériens avec prompt system, user et assistant

### Base de connaissances (100% algérienne)

- Loi n° 07-11 du 25 novembre 2007 portant SCF
- Fiscalité algérienne (TVA 19%/9%/0%, IBS, IRG)
- Normes d'audit algériennes
- Droit commercial algérien
- Charges sociales (CNAS, CASNOS)
- Formes juridiques (SARL, EURL, SNC, SPA)
- Écritures comptables courantes

### Public cible

Experts-comptables, commissaires aux comptes, comptables agréés, étudiants en comptabilité en Algérie.

---

**English**

### Overview

Comptable-SLM is an intelligent assistant specialized in Algerian accounting and audit, combining a Retrieval-Augmented Generation (RAG) pipeline with a fine-tuned Small Language Model (SLM). The project aims to provide Algerian chartered accountants, statutory auditors, and certified public accountants with a reliable reference tool covering the Algerian Financial Accounting System (SCF), Algerian tax law (IBS, VAT, IRG), social charges (CNAS, CASNOS), and commercial law.

### Technical Architecture

- **RAG Pipeline**: NVIDIA NIM embeddings (Nemotron-3-Embed-1B), ChromaDB vector store (cosine similarity), section-based chunking (534 chunks), distance threshold < 0.6
- **Cloud LLM**: Llama 3.1 8B Instruct via NVIDIA NIM API
- **Local SLM**: Llama 3.2 3B fine-tuned with Unsloth/QLoRA (4-bit), exported as GGUF for Ollama
- **Dataset**: 150 Algerian training examples with system, user, and assistant messages

### Knowledge Base (100% Algerian)

- Law No. 07-11 of November 25, 2007 on the Financial Accounting System (SCF)
- Algerian taxation (VAT 19%/9%/0%, IBS, IRG)
- Algerian auditing standards
- Algerian commercial law
- Social charges (CNAS, CASNOS)
- Legal forms (SARL, EURL, SNC, SPA)
- Standard accounting entries

### Target Audience

Chartered accountants, statutory auditors, certified accountants, and accounting students in Algeria.

---

### Stack technique / *Tech Stack*

| Component | Technology |
|-----------|-----------|
| Embeddings | NVIDIA Nemotron-3-Embed-1B |
| Vector Store | ChromaDB (cosine, persistent) |
| Cloud LLM | Llama 3.1 8B Instruct |
| Local SLM | Llama 3.2 3B (fine-tuned) |
| Fine-tuning | Unsloth + QLoRA (4-bit) |
| Inference | Ollama (local) / NVIDIA NIM (cloud) |
| Langage | Python, JSONL dataset |

### Contact

Projet open source développé pour la communauté comptable algérienne.
*Open source project built for the Algerian accounting community.*
