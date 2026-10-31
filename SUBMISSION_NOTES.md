# Cynbit AI/ML Candidate Portal Submission Guide

**Applicant**: Naman Kalia (`namankalia1904@gmail.com`)  
**Role**: AI/ML Engineer Intern  
**Active Portal**: `https://www.cynbit.in/candidate/cmunzfa2g000904lccs46stm1`  
**Reference Code**: `cmunzfa2g000804lcs62wmllr`  
**Assessment Task**: *AI/ML Engineer Intern - Task — Identify an AI Opportunity for Cynbit*

---

## 📋 Portal Submission Form Inputs

### 1. Primary Deliverable URL *(Required)*
```text
https://github.com/NamTheGreat/cynbit-ai-opportunity
```
*(Or your public GitHub repository URL once created and pushed).*

---

### 2. Additional Deliverable Links *(Optional — Up to 4 links)*
* **Link 1 (AI Opportunity Report - Industry & ROI Analysis)**:
  ```text
  https://github.com/NamTheGreat/cynbit-ai-opportunity/blob/main/AI_OPPORTUNITY_REPORT.md
  ```
* **Link 2 (Technical Approach Report - Model Selection & MLOps)**:
  ```text
  https://github.com/NamTheGreat/cynbit-ai-opportunity/blob/main/TECHNICAL_APPROACH_REPORT.md
  ```
* **Link 3 (Interactive Demo Video / Streamlit Prototype Walkthrough)**:
  ```text
  https://github.com/NamTheGreat/cynbit-ai-opportunity#interactive-demo-options
  ```

---

### 3. Execution Notes & Campaign / Architecture Rationale *(Textarea)*
*Formal, human-written summary ready to paste into the portal:*

```text
Hi Cynbit AI/ML Team,

For this assessment, I analyzed Cynbit's business model across its core platforms—Cynbit Studio, TenantEase, Revio, and the Aria AI Talent Hub. 

I identified four high-leverage AI opportunities and selected the single most transformative one to build as a working proof of concept: "Aria Studio Evaluator"—an autonomous, multi-agent code quality and technical assessment evaluation engine.

Key Highlights of the Submission:
1. AI Opportunity Report (AI_OPPORTUNITY_REPORT.md):
   Analyzes current candidate screening bottlenecks (manual reviewer fatigue, scoring inconsistency, naive single-prompt LLM hallucinations). Models the business case: recapturing ~INR 19.5 Lakhs/year in senior engineering hours internally for Aria AI, while unlocking an estimated INR 81 Lakhs ARR as a B2B automated candidate evaluation feature within Cynbit Studio.

2. Functional AI/ML Proof of Concept (Python / FastAPI / Streamlit):
   Built a fully runnable multi-agent system combining:
   - Deterministic AST Code Parsing (Python ast & TypeScript control-flow complexity analysis).
   - Static Security Scanner (OWASP API Top 10, CWE-798 hardcoded secrets, and CWE-918 SSRF detection).
   - Domain-Specific LLM Agents (SecurityAgent, ArchitectureAgent, CleanCodeAgent) orchestrated by a SynthesisAgent that computes calibrated rubric scores (0-100) and hiring recommendations.
   - Interactive Streamlit Dashboard (app.py), Rich terminal CLI (aria_evaluator.cli), and REST API (FastAPI).

3. Technical Approach Report (TECHNICAL_APPROACH_REPORT.md):
   Details the model selection trade-offs (Gemini 2.5 Flash for high-speed, long-context repo triage vs. Claude 3.5 Sonnet for deep architectural synthesis vs. Qwen 2.5 Coder 32B for air-gapped on-premise execution), token pruning heuristics, prompt injection defense, and continuous evaluation protocols (Evals on golden benchmark datasets).

All 10 automated unit tests pass cleanly (PYTHONPATH=src pytest). Looking forward to discussing the architecture and potential productization with the team.

Best regards,
Naman Kalia
```
