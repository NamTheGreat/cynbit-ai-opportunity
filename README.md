# Aria Studio Evaluator — Autonomous Multi-Agent Codebase Quality & Technical Assessment Engine

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.41-FF4B4B.svg)](https://streamlit.io/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2.10-E92063.svg)](https://docs.pydantic.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-8.3%20Passing-green.svg)](https://pytest.org/)

> **AI/ML Engineer Intern Technical Assessment Deliverable for Cynbit Technologies**  
> **Applicant**: Naman Kalia (`namankalia1904@gmail.com`)  
> **Task**: *Identify an AI Opportunity for Cynbit*  

---

## 🎯 Deliverables Matrix

This repository fulfills all three required deliverables for the **Cynbit AI/ML Engineer Intern Technical Challenge**:

| Required Deliverable | Project File / Component | Summary Description |
| :--- | :--- | :--- |
| **1. AI Opportunity Report** | [**`AI_OPPORTUNITY_REPORT.md`**](./AI_OPPORTUNITY_REPORT.md) | In-depth industry and business model analysis across Cynbit's platforms (Services, Cynbit Studio, TenantEase, Revio, Aria AI). Evaluates 4 distinct opportunities with ROI models and selects **Aria Studio Evaluator** as the highest-leverage engine. |
| **2. AI/ML Proof of Concept** | [**`app.py`**](./app.py) & [**`src/aria_evaluator/`**](./src/aria_evaluator) | Functional, executable multi-agent code evaluation prototype with interactive Streamlit UI, Rich terminal CLI, and FastAPI REST endpoints. |
| **3. Technical Approach Report** | [**`TECHNICAL_APPROACH_REPORT.md`**](./TECHNICAL_APPROACH_REPORT.md) | Technical architecture document detailing model selection (Gemini 2.5 Flash vs Claude 3.5 Sonnet vs Qwen 2.5 Coder), AST data pipelines, prompt engineering schemas, and production MLOps execution plan. |

---

## 🏛️ System Architecture

Aria Studio Evaluator replaces subjective, time-consuming manual code reviews with a **hybrid deterministic-cognitive multi-agent pipeline**:

```mermaid
flowchart LR
    subgraph 1. Preprocessing
        Repo["Input Codebase<br/>(Local Folder or Git)"] --> Ingestor["Repository Ingestor<br/>(Token Pruning)"]
    end

    subgraph 2. Deterministic AST Scanners
        Ingestor --> AST["Static AST Analyzer<br/>(LOC, Complexity, Hotspots)"]
        Ingestor --> SecScanner["Static Security Scanner<br/>(OWASP, CWE, Secrets)"]
    end

    subgraph 3. Cognitive Multi-Agent Domain Layer
        AST --> AgentSec["🛡️ Security Agent"]
        SecScanner --> AgentSec
        AST --> AgentArch["🏛️ Architecture Agent"]
        AST --> AgentClean["✨ Clean Code Agent"]
    end

    subgraph 4. Synthesis & Recommendation
        AgentSec --> Synth["🧠 Synthesis Agent"]
        AgentArch --> Synth
        AgentClean --> Synth
        Synth --> Output["Candidate Scorecard<br/>(Score: 0-100, Radar Chart, Hiring Rec)"]
    end
```

---

## 🚀 Quickstart & Verification

### 1. Prerequisites
* Python 3.11+ (Tested on Python 3.14.7)
* Virtual environment recommended

### 2. Setup & Installation
```bash
cd aiml-opportunity
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Automated Test Suite
```bash
PYTHONPATH=src pytest
```
*Executes all 10 unit tests covering AST parsing, security scanners, multi-agent evaluation, and FastAPI endpoints with a **100% pass rate**.*

---

## 🖥️ Interactive Demo Options

### Option A: Launch Interactive Streamlit Dashboard
```bash
streamlit run app.py
```
*Opens an interactive visual portal allowing you to evaluate the Cynbit backend codebase, test built-in vulnerable/clean presets, inspect radar scorecards, and review agent insights.*

### Option B: Run Rich Terminal CLI
Evaluate any local codebase or repository in the terminal:
```bash
PYTHONPATH=src python3 -m aria_evaluator.cli ../codebase --name "Cynbit Reference Architecture"
```

#### Terminal Output Example:
```text
╭─────────────────────────────── Aria Evaluator ───────────────────────────────╮
│ Running Aria Autonomous Multi-Agent Evaluation on:                           │
│ /Users/namankalia/Documents/intern projects/Cybit/codebase                   │
╰──────────────────────────────────────────────────────────────────────────────╯
                          Evaluation Scorecard                          
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Dimension                    ┃ Score (0-100) ┃ Key Agent Observation ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ Security & Access Control    │         100.0 │                       │
│ Architecture & Modularity    │         100.0 │                       │
│ Clean Code & Testability     │         100.0 │                       │
│ Complexity & Maintainability │          70.3 │                       │
└──────────────────────────────┴───────────────┴───────────────────────┘
╭──────────────────────────── Final Recommendation ────────────────────────────╮
│ Overall Rubric Score: 94.1/100                                               │
│ Hiring Recommendation: STRONG_HIRE                                           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### Option C: Launch FastAPI REST Service
```bash
PYTHONPATH=src uvicorn aria_evaluator.api:app --reload --port 8000
```
*Interactive Swagger documentation available at `http://localhost:8000/docs`.*

---

## 📊 Business Impact & ROI Summary

* **Recaptured Senior Capacity**: Saves senior engineers **~45 hours per quarter**, reducing candidate assessment overhead by **~75%** ($\approx \text{INR } 19.5\text{ Lakhs/year}$).
* **Commercialization in Cynbit Studio**: Unlocks a **B2B automated candidate evaluation SaaS tier** targeting enterprise engineering teams, with projected Year 1 ARR of **$\approx \text{INR } 81\text{ Lakhs}$**.
* **Zero Calibration Drift**: Mathematical bounding prevents score inflation while strict Pydantic schemas eliminate prompt injection risks.
