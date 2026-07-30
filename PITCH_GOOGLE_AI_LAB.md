# Pitch – Comptable-SLM
## Google Africa Applied AI Lab

---

## 1. The Problem

**Accounting in Africa is fragmented and complex.**

Each country has its own tax system, chart of accounts, and regulatory framework. In Algeria alone:
- The SCF (Système Comptable et Financier) replaced the old PCN in 2007
- VAT has 3 rates (19%, 9%, 0%) with specific rules
- Social charges involve CNAS and CASNOS with different regimes
- Legal forms (SARL, EURL, SPA, SNC) each have distinct requirements

Most existing AI accounting tools are trained on US/European data and hallucinate when asked about Algerian law. Accountants rely on scattered PDFs, outdated textbooks, or expensive consultants.

## 2. The Solution

**Comptable-SLM: an AI assistant trained specifically on African accounting frameworks.**

- **RAG pipeline**: Instantly retrieves relevant legaltexts from a curated knowledge base (SCF law, tax codes, audit standards)
- **Fine-tuned SLM**: A Llama 3.2 3B model trained on 150+ real accounting scenarios, deployable offline via Ollama
- **Always accurate**: Responses cite sources; distance threshold filtering prevents hallucinations

## 3. Technical Innovation

| Component | Technology | Why it matters |
|-----------|-----------|----------------|
| Embeddings | NVIDIA Nemotron-3-Embed-1B (NIM) | State-of-the-art retrieval accuracy |
| Vector store | ChromaDB (cosine, persistent) | Fast, local, privacy-preserving |
| Cloud LLM | Llama 3.1 8B Instruct | Handles complex reasoning |
| Local SLM | Llama 3.2 3B (fine-tuned, 4-bit) | Works offline, no internet needed |
| Fine-tuning | Unsloth + QLoRA | 2x faster training, low VRAM |

**Key differentiator**: Most AI accounting tools use generic LLMs. Ours is fine-tuned on African accounting data and can run entirely offline — critical for areas with unreliable internet.

## 4. Market Opportunity

- **Algeria**: ~15,000 chartered accountants + 50,000+ accounting professionals
- **OHADA zone** (16 African countries): Common accounting framework across West & Central Africa
- **Africa-wide potential**: 54 countries, each with unique tax and accounting systems

Initial TAM: 500,000+ accounting professionals across Francophone Africa.

## 5. Traction & Roadmap

**Completed:**
- ✅ RAG pipeline fully functional (Algerian knowledge base, 534 chunks)
- ✅ SLM fine-tuned on 150 Algerian examples (loss: 1.89 → 0.03)
- ✅ Local inference via Ollama (GGUF export ready)
- ✅ Knowledge base: SCF law, taxation, audit standards, social charges, commercial law

**Next 3 months:**
- Expand dataset to 1,000+ examples across more accounting scenarios
- Add support for OHADA accounting standards (16 countries)
- Build a simple web UI (Gradio/Streamlit)
- Beta testing with 10-20 Algerian accounting firms

**Next 6 months:**
- Country-specific modules (Morocco, Tunisia, Senegal, Ivory Coast)
- Mobile app for on-the-go queries
- Integration with accounting software (entry-level)

## 6. Why Google Africa Applied AI Lab?

We need:
- **Early access to Gemini / Gemma** – to experiment with larger, more capable models for complex multi-country queries
- **Technical mentorship** – to optimize our RAG pipeline and fine-tuning strategy
- **Go-to-market support** – to reach accounting professionals across Africa
- **VC network** – to scale beyond Algeria into the OHADA zone and beyond

## 7. The Team

**Expert-comptable & Auditeur légal** | Développeur amateur passionné par l'IA

- 15+ years of experience in Algerian accounting, audit, and tax
- Deep knowledge of SCF, Algerian tax law (IBS, IRG, TVA), social charges (CNAS, CASNOS)
- Built this project from scratch: RAG pipeline, fine-tuning, dataset creation
- Motto: *"AI should serve African professionals, not the other way around"*

---

## 8. Demo

I can show:
1. RAG query: *"Quels sont les taux de TVA en Algérie ?"* → cites SCF law
2. Fine-tuned model: *"Différence entre SARL et EURL ?"* → accurate answer in French
3. Offline inference: model runs locally via Ollama, no cloud dependency

---

**Contact**: *(à compléter)*
