#  AI Guardian — LLM Observability & Cost Intelligence Platform

> **Production-grade monitoring infrastructure for AI systems** — built to give engineering teams full visibility into every LLM interaction: latency, token usage, cost, quality scoring, hallucination detection, and real-time alerting.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=flat-square&logo=vite)

---

##  What is AI Guardian?

Most teams building LLM-powered applications stop at:
```
prompt goes in → answer comes out
```

But in production, that is not enough.

**AI Guardian** is an event-driven observability platform that sits alongside any AI application and answers the questions that matter in production:

- Did the model answer correctly?
- Was the response too slow or too expensive?
- Did the model hallucinate?
- Which model version performs better?
- Which feature is draining the budget?
- Did a prompt change make things worse?

It is the **control tower for AI systems** — turning raw LLM interactions into actionable intelligence.

---

##  System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                      AI Application                          │
│  (chatbot / RAG pipeline / agent workflow / summarizer)      │
└───────────────────────┬─────────────────────────────────────┘
                        │ SDK wraps every LLM call
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI Guardian SDK                           │
│  • @track_llm_call decorator                                 │
│  • start_trace() / log_event() / end_trace()                 │
│  • OpenAI + LangChain integrations                           │
│  • Auto-captures: latency, tokens, cost, errors              │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP events
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend                             │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ Event       │  │ Cost         │  │ Evaluation       │   │
│  │ Ingestion   │  │ Intelligence │  │ Service          │   │
│  │ Layer       │  │ Service      │  │ (quality scoring)│   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ Alert       │  │ Trace        │  │ Metrics          │   │
│  │ Service     │  │ Tracking     │  │ Aggregation      │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   PostgreSQL Database                        │
│         llm_events │ alerts │ traces                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              React + Vite Dashboard                          │
│   Dashboard │ Events │ Alerts │ Traces                      │
└─────────────────────────────────────────────────────────────┘
```

---

##  Key Features

###  Event-Driven Observability
Every LLM interaction is captured as a structured event — input prompt, output, model metadata, latency, token usage, cost, and quality scores — stored in PostgreSQL and queryable in real time.

###  Cost Intelligence Engine
Automatically computes the USD cost of every LLM call using per-model token pricing for GPT-4o, GPT-4o-mini, GPT-4-turbo, Claude 3 Opus, Claude 3 Sonnet, and more. Aggregates cost by model, session, and time period.

###  Quality & Hallucination Scoring
Every response is automatically evaluated for:
- **Quality score** (0–1) — based on output length, coherence, and refusal patterns
- **Hallucination risk** (0–1) — detects overconfident language patterns
- **Groundedness score** (0–1) — checks whether output cites context

###  Intelligent Alerting
Threshold-based alerts auto-trigger for:
- Latency > 5000ms
- Cost > $0.10 per call
- Quality score < 0.4
- Hallucination risk > 0.7
- Any failed request

Alerts are stored, displayed in the dashboard, and resolvable with one click.

###  Distributed Trace Tracking
Multi-step AI workflows (RAG pipelines, agent chains) are linked under a single `trace_id` — so you can inspect every step of a request from retrieval → reranking → generation → evaluation.

###  Drop-In SDK Integration
Any Python AI application can integrate AI Guardian in minutes:
```python
# Option 1: One decorator
@track_llm_call(model_name="gpt-4o-mini", session_id="user-123")
def call_llm(prompt):
    return openai_client.chat.completions.create(...)

# Option 2: Full RAG trace
trace_id = start_trace(session_id="rag-pipeline")
log_event(trace_id, step_name="retrieval", ...)
log_event(trace_id, step_name="generation", ...)
end_trace(trace_id)
```

---

##  Project Structure
```
ai-guardian/
├── backend/                  # FastAPI REST API
│   └── app/
│       ├── main.py           # App entry point, CORS, route registration
│       ├── db.py             # SQLAlchemy + PostgreSQL connection
│       ├── models.py         # LLMEvent, Alert, Trace ORM models
│       ├── schemas.py        # Pydantic request/response schemas
│       ├── routes/
│       │   ├── events.py     # POST/GET LLM interaction events
│       │   ├── metrics.py    # Summary, cost-by-model, latency trend
│       │   ├── alerts.py     # List and resolve alerts
│       │   └── traces.py     # Multi-step trace viewer
│       └── services/
│           ├── cost_service.py        # Per-model token cost computation
│           ├── evaluation_service.py  # Quality, hallucination, groundedness
│           └── alert_service.py       # Threshold checks, alert creation
├── sdk/                      # Python SDK for integration
│   ├── ai_guardian/
│   │   ├── client.py         # HTTP client (fire-and-forget, never crashes app)
│   │   ├── tracker.py        # @track_llm_call, start_trace, log_event
│   │   ├── models.py         # LLMEvent dataclass
│   │   └── utils.py          # Token estimation, latency formatting
│   └── examples/
│       ├── openai_tracked.py     # OpenAI decorator + RAG trace example
│       └── langchain_tracked.py  # LangChain callback handler
└── frontend/                 # React + Vite dashboard
    └── src/
        ├── App.jsx           # Sidebar navigation
        └── pages/
            ├── Dashboard.jsx  # Stat cards + latency/cost charts
            ├── EventsPage.jsx # Live event stream with badges
            ├── AlertsPage.jsx # Active alerts with resolve button
            └── TracesPage.jsx # Multi-step trace viewer
```

---

##  Quickstart

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 15

### 1. Backend
```bash
cd backend
pip install -r requirements.txt

# Create the database
createdb ai_guardian

# Start the server
uvicorn app.main:app --reload
```

API docs available at: **http://localhost:8000/docs**

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

Dashboard available at: **http://localhost:5173**

### 3. SDK
```bash
cd sdk
pip install -e .
```
```python
from ai_guardian import track_llm_call

@track_llm_call(model_name="gpt-4o-mini")
def ask(prompt):
    return openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
```

---

##  API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/events/` | Ingest a new LLM interaction event |
| GET | `/api/events/` | List all events with filters |
| GET | `/api/metrics/summary` | Total requests, cost, latency, alerts |
| GET | `/api/metrics/cost-by-model` | Cost breakdown per model |
| GET | `/api/metrics/latency-trend` | Latency over time |
| GET | `/api/metrics/errors` | Failed requests |
| GET | `/api/alerts/` | List active alerts |
| PATCH | `/api/alerts/{id}/resolve` | Resolve an alert |
| GET | `/api/traces/` | List all traces |
| GET | `/api/traces/{trace_id}` | Full trace with all steps |

---

##  Testing the System

Send a test event:
```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Content-Type: application/json" \
  -d '{
    "input_prompt": "What is machine learning?",
    "model_name": "gpt-4o-mini",
    "output": "Machine learning is a subset of AI...",
    "prompt_tokens": 15,
    "completion_tokens": 20,
    "latency_ms": 1200,
    "success": true
  }'
```

Trigger an alert (latency > 5000ms threshold):
```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Content-Type: application/json" \
  -d '{
    "input_prompt": "Summarize this document",
    "model_name": "gpt-4o",
    "output": "Here is the summary.",
    "prompt_tokens": 500,
    "completion_tokens": 100,
    "latency_ms": 7500,
    "success": true
  }'
```

---

##  Engineering Design Decisions

**Why FastAPI?** Async-ready, automatic OpenAPI docs, Pydantic validation — ideal for high-throughput event ingestion.

**Why PostgreSQL?** Structured event data with complex aggregation queries (cost by model, latency trends) benefits from a relational database over a NoSQL store.

**Why a separate SDK?** Decoupling the integration layer from the monitoring backend means any team can adopt AI Guardian without modifying their architecture. The SDK is fire-and-forget — it never crashes the calling application.

**Why heuristic evaluation?** The evaluation service uses lightweight heuristics (quality scoring, hallucination risk estimation) that run synchronously without adding LLM API latency. This can be swapped for an LLM-as-judge approach in production.

---

##  Roadmap

- [ ] LLM-as-judge evaluation (GPT-4o scoring outputs)
- [ ] Slack / email alert integrations
- [ ] Prompt regression testing
- [ ] Multi-tenant support
- [ ] Cost budget alerts and forecasting
- [ ] Model A/B comparison dashboard
- [ ] Vector similarity scoring for RAG grounding

---

##  Author

**Siham Boumalak**
M.S. Artificial Intelligence — Northeastern University, Khoury College of Computer Sciences
Concentration: Machine Learning | Expected 2027

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](linkedin.com/in/siham-boumalak-11014b210)
[![GitHub](https://img.shields.io/badge/GitHub-boumalaksiham-181717?style=flat-square&logo=github)](https://github.com/boumalaksiham)

---

##  Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI, Python 3.12 |
| Database | PostgreSQL 15, SQLAlchemy ORM |
| Data Validation | Pydantic v2 |
| Frontend | React 18, Vite 5, Recharts |
| SDK | Python, httpx |
| LLM Integrations | OpenAI, LangChain |
| Dev Tools | Uvicorn, npm |
