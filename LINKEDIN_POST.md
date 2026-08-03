# Post LinkedIn — Comptable-SLM

## Titre
**Prototype SLM Droit comptable et fiscal Algérien**

---

## Texte du post (≈ 2 200 caractères)

🇩🇿 **J'ai développé Comptable-SLM, un prototype de SLM (Small Language Model) spécialisé dans le droit comptable et fiscal algérien.**

### Le problème
Les LLM généralistes (ChatGPT, Claude...) hallucinent sur le droit algérien :
- TVA 19%/9%/0% → réponses françaises
- SCF (loi 07-11) vs ancien PCN → confusion
- Comptes TVA 4455/4456/4457 → inconnus
- CNAS 7% / CASNOS 15% → mélangés ou inventés
- IBS 19% uniforme, IRG barème 2024 → barèmes étrangers
- SARL/EURL/SPA, commissaire aux comptes → règles françaises

### La solution : Comptable-SLM
**RAG + SLM fine-tuné 100% droit algérien**

🔹 **Pipeline RAG** : 7 fichiers knowledge base (SCF, fiscalité, audit, charges sociales, droit commercial, formes juridiques, procédures) → 534 chunks ChromaDB
🔹 **125 Q&A curées** : questions naturelles + réponses concises rédigées par expert-comptable
🔹 **TF-IDF accent-insensitive** : matching robuste (déductible = déductible, declaration = déclaration)
🔹 **Réponses sourcées** : chaque réponse cite sa source (fichier + section)
🔹 **Fallback intelligent** : "Je ne sais pas" plutôt qu'hallucination
🔹 **SLM local** : Llama 3.2 3B fine-tuné (Unsloth/QLoRA) → GGUF → Ollama (offline)

### Ce qu'il maîtrise (tests 37/37 ✅)
| Domaine | Exemples |
|---------|----------|
| **TVA** | Taux 19/9/0%, comptes 4455/4456/4457, déclaration, écritures achat/vente |
| **IBS/IRG** | IBS 19% uniforme, IRG barème 2024, retenue source compte 4431 |
| **Charges sociales** | CNAS 7%, CASNOS 15%, allocations familiales, congés payés 30j |
| **Formes juridiques** | SARL/EURL/SPA/SNC, capital 100k DA, registre commerce |
| **Audit** | Normes ISA, commissaire aux comptes, obligations |
| **Écritures/Procédures** | Achat/vente TVA, amortissement, provision, calendrier fiscal, clôture |

### Démo en ligne (lien permanent)
👉 **https://comptable-slm-1.onrender.com**
Interface Gradio légère sur Render (Free tier, lien permanent).

### Public cible
Experts-comptables, commissaires aux comptes, comptables agréés, étudiants, cabinets d'audit algériens.

---

**L'IA doit servir les professionnels algériens, pas l'inverse.** 💪

#Comptabilité #Algérie #IA #SCF #Audit #TVA #IBS #IRG #CNAS #CASNOS #ExpertComptable #SLM #RAG #FineTuning

---

## Variantes carrousel
Voir `slides/` (10 PNG) + `Comptable_SLM_Pitch.pptx`