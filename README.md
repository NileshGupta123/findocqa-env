---
title: FinDocQA-Env
emoji: 🏦
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
short_description: OpenEnv environment for financial document QA
tags:
  - openenv
---

# FinDocQA-Env 🏦

An OpenEnv environment for evaluating AI agents on financial document 
comprehension tasks. Agents must extract key facts, answer analytical 
questions, and identify contradictions in real-world style business 
and financial reports.

---

## 🎯 Why This Environment?

Financial document analysis is a critical real-world task performed daily by:
- Investment analysts reviewing earnings reports
- Auditors checking for inconsistencies in annual reports
- Risk managers extracting key metrics from disclosures

This environment evaluates whether AI agents can perform these tasks 
accurately and reliably — a genuine benchmark for real-world utility.

---

## 📋 Tasks

### Task 1: `extract-facts` (Easy)
**Objective:** Extract 4 specific facts from a financial report excerpt.

The agent must identify:
1. Total revenue (exact figure with units)
2. Company name (full legal name)
3. Reporting period (quarter or full year)
4. Year-over-year revenue change (percentage)

**Grader:** Fuzzy string match per field, averaged across all 4 fields.  
**Expected score:** ~0.70 for capable models  
**Difficulty:** Easy

---

### Task 2: `answer-questions` (Medium)
**Objective:** Answer 4 comprehension questions about a financial document.

The agent receives a document and must answer questions about:
- Revenue figures and growth rates
- Executive names and roles
- Key financial ratios
- Segment performance

**Grader:** Token-level F1 score per question (SQuAD methodology).  
**Expected score:** ~0.45 for capable models  
**Difficulty:** Medium

---

### Task 3: `identify-conflicts` (Hard)
**Objective:** Identify all contradictions between two sections of a 
financial report written by different executives.

The agent must find conflicts in:
- Revenue guidance figures
- Margin outlooks
- Growth quality assessments
- Sustainability claims

**Grader:** Weighted keyword coverage — topic identification (40%) 
plus both-sides referencing (60%).  
**Expected score:** ~0.30 for capable models  
**Difficulty:** Hard

---

## 🔧 Action Space
```json
{
  "response": "string — agent's text response to the current task"
}
```

## 👁️ Observation Space
```json
{
  "document": "string — financial document excerpt",
  "task_type": "extract-facts | answer-questions | identify-conflicts",
  "instructions": "string — detailed task instructions",
  "questions": "array of strings | null",
  "step": "integer — current step number"
}
```

## 🏆 Reward

- Type: `float`
- Range: `0.0 to 1.0`
- Signal: Continuous partial credit — never binary
- Method: Fuzzy match / Token F1 / Keyword coverage depending on task

---

## 📊 Baseline Scores

| Task | Model | Score |
|---|---|---|
| extract-facts | llama-3.1-8b-instant | 1.000 |
| answer-questions | llama-3.1-8b-instant | 0.399 |
| identify-conflicts | llama-3.1-8b-instant | 0.822 |
| **Average** | | **0.740** |

---

## 🚀 Setup & Usage

### Prerequisites
- Python 3.11+
- Docker
- Groq API key (or any OpenAI-compatible API)

### Local Setup
```bash
# Clone the repo
git clone https://huggingface.co/spaces/Nile-2026/findocqa-env
cd findocqa-env

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "API_BASE_URL=https://api.groq.com/openai/v1" > .env
echo "MODEL_NAME=llama-3.1-8b-instant" >> .env
echo "HF_TOKEN=your_groq_api_key" >> .env

# Start the server
uvicorn server.main:app --host 0.0.0.0 --port 8000
```

### Run Baseline Inference
```bash
python inference.py
```

### Docker
```bash
# Build
docker build -t findocqa-env .

# Run
docker run -p 7860:7860 findocqa-env
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/reset` | POST | Start new episode |
| `/step` | POST | Submit agent response |
| `/state` | POST | Get current episode state |
| `/health` | GET | Health check |
| `/docs` | GET | Swagger UI |

### Example Usage
```python
import requests

# Start episode
obs = requests.post("http://localhost:7860/reset", json={}).json()
print(obs["observation"]["task_type"])

# Submit response
result = requests.post("http://localhost:7860/step", json={
    "response": "Your agent response here"
}).json()
print(result["reward"])
```

---

## 📁 Project Structure
findocqa-env/
├── inference.py          # Baseline inference script
├── openenv.yaml          # OpenEnv spec metadata
├── Dockerfile            # Container definition
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── server/
├── main.py           # FastAPI application
├── env.py            # Episode state machine
├── models.py         # Pydantic typed models
├── data/
│   └── documents.py  # Synthetic financial documents
├── tasks/
│   ├── extract_facts.py
│   ├── answer_questions.py
│   └── identify_conflicts.py
└── graders/
└── grader.py     # Scoring algorithms

---

## 📄 Documents Included

| ID | Company | Type |
|---|---|---|
| doc_001 | TechCorp Inc. | Q3 Earnings Report |
| doc_002 | GlobalBank Corporation | Annual Report |
| doc_003 | RetailMax | Q2 Earnings with Conflicts |
| doc_004 | NovaPharma Ltd. | Q1 Earnings Report |
| doc_005 | FusionEnergy Inc. | Annual Report with Conflicts |

---

## ⚙️ Environment Variables

| Variable | Description |
|---|---|
| `API_BASE_URL` | LLM API endpoint |
| `MODEL_NAME` | Model identifier |
| `HF_TOKEN` | API key |
| `ENV_BASE_URL` | Environment server URL (default: localhost:8000) |

---

*Built for the OpenEnv Hackathon by Nile-2026*