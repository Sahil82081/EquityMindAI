# EquityMind AI 🧠📈

> **Autonomous Multi-Agent Investment Intelligence, Claim-Evidence Verification, and Grounded Research Q&A**

EquityMind AI is an institutional-grade investment research platform that replaces ungrounded AI chat with an auditable, deterministic multi-agent research pipeline. Every fundamental metric is calculated in Python, every narrative claim is audited against filings and market data, adversarial Bull and Bear perspectives are adjudicated by an impartial Judge agent, and overall research integrity is scored using a deterministic formula.

---

## 📑 Table of Contents

- [Key Capabilities](#-key-capabilities)
- [System Architecture](#-system-architecture)
- [Multi-Agent Research Workflow](#-multi-agent-research-workflow)
- [Deterministic Mathematical Models](#-deterministic-mathematical-models)
  - [Claim $\rightarrow$ Evidence Verification](#1-claim--evidence-verification)
  - [Research Reliability Score](#2-research-reliability-score)
- [Project Directory Structure](#-project-directory-structure)
- [API Reference](#-api-reference)
- [Grounded Research Q&A](#-grounded-research-qa)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#1-backend-setup)
  - [Frontend Setup](#2-frontend-setup)
  - [Environment Variables](#3-environment-variables)
- [Validation & Test Suite](#-validation--test-suite)
- [Disclaimer & License](#-disclaimer--license)

---

## ⚡ Key Capabilities

- **Deterministic Company Resolution**: Fast, typo-tolerant search across tickers (`AAPL`, `MSFT`, `NVDA`) and natural language company names (`Apple`, `Microsft`, `Nvidia`).
- **Empirical Market Fundamentals**: Integrates `yfinance` to retrieve live stock quotes, price changes, market cap, EPS, P/E, revenue history, and operating/net margins without LLM hallucinations.
- **News Aggregator with Sentiment**: Pulls recent market and SEC headlines with verified timestamps, original source links, and contextual sentiment classifications.
- **Algorithmic Valuation Analysis**: Computes trailing valuation multiples and compares them against multi-year historical benchmarks directly in code.
- **Adversarial Debate System**: Parallel **Bull Agent** and **Bear Agent** formulate evidence-backed investment arguments, which are then evaluated and synthesized by an impartial **Judge Agent**.
- **Claim $\rightarrow$ Evidence Verification System**: Audits every key generated assertion against raw filing numbers, calculating percentage changes and tagging claims as **Verified**, **Partially Verified**, or **Unsupported**.
- **Research Reliability Score**: A deterministic $0-100$ score derived from four measurable dimensions: Evidence Quality ($30\%$), Claim Verification ($30\%$), Source Coverage ($20\%$), and Agent Agreement ($20\%$).
- **Grounded Research Q&A**: A conversational intelligence interface strictly bound to the active research session, citing verified claims and refusing ungrounded speculative stock price predictions.
- **Premium Financial Terminal UI**: Built with React 19, TypeScript, and Vite featuring interactive radial gauges, tabbed dossiers, and real-time pipeline monitoring.

---

## 🏛 System Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       React 18 + TypeScript + Vite UI                       │
│  (Landing Page, Pipeline Monitor, Reliability Radial Gauge, 4-Tab Workspace,│
│                       Grounded Research Copilot)                            │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP / REST JSON
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FastAPI Backend Service                            │
│  [/api/v1/health, /company/search, /research, /research/{id}, /copilot]     │
└──────────────┬───────────────────────────────────────────────┬──────────────┘
               │                                               │
               ▼                                               ▼
┌──────────────────────────────┐              ┌───────────────────────────────┐
│     Company Resolver         │              │   Research Copilot Service    │
│  - Deterministic Ticker Map  │              │  - Session & State Retrieval  │
│  - Levenshtein / Fuzzy Match │              │  - In-Context Grounding       │
│  - SEC / Exchange Normalizer │              │  - Hallucination Rejection    │
└──────────────┬───────────────┘              └───────────────▲───────────────┘
               │                                               │
               ▼                                               │ Grounded
┌──────────────────────────────────────────────────────────────┴──────────────┐
│                    LangGraph Research Workflow Graph                        │
│                                                                             │
│  1. DataAgent ───────────────► 2. NewsAgent ──────────► 3. ValuationAgent   │
│     (yfinance Market Data)       (Verified Feeds)        (Code Calculations)│
│                                                                  │          │
│  5. JudgeAgent ◄───────── [4. BullAgent || 4. BearAgent] ◄───────┘          │
│     (Adjudication)           (Adversarial Debate)                           │
│           │                                                                 │
│           ▼                                                                 │
│  6. ClaimVerifier (Audit Filings vs LLM Claims via Python math)             │
│           │                                                                 │
│           ▼                                                                 │
│  7. ReliabilityCalculator (Deterministic 30/30/20/20 Weighted Score)        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Multi-Agent Research Workflow

The pipeline executes sequentially and in parallel branches through a typed LangGraph state machine:

```text
User 
  ↓ 
Company Resolution (Deterministic Search & Typo Normalization)
  ↓ 
Financial Data (Data Agent · yfinance & Market Fundamentals)
  ↓ 
News (News Agent · Verified SEC & RSS News Feeds)
  ↓ 
Valuation (Valuation Agent · Code Calculations & Multiple Comparison)
  ↓ 
Bull Agent (Evidence-backed Thesis & Growth Drivers)
  ↓ 
Bear Agent (Counter-Thesis & Multiple/Risk Challenges)
  ↓ 
Judge Agent (Adjudication & Balanced Synthesis)
  ↓ 
Claim Verification (Audited Filings vs Claims in Python)
  ↓ 
Reliability Score (Deterministic 4-Metric Weighted Model)
  ↓ 
Final Research Report & Grounded Research Copilot
```

1. **Company Resolver**: Resolves input strings into normalized equity metadata (`ticker`, `name`, `exchange`, `market`).
2. **Data Agent**: Connects to financial APIs (`yfinance`), retrieving audited income statements, revenue history, EPS, operating margins, and current quotes.
3. **News Agent**: Gathers recent company news articles, publication timestamps, and source links.
4. **Valuation Agent**: Computes P/E multiples, revenue growth trends, and historical benchmark comparisons.
5. **Bull Agent & Bear Agent**: Run in parallel to construct adversarial cases based solely on the retrieved research state.
6. **Judge Agent**: Compares arguments, checks factual backing, identifies thesis weaknesses, and crafts an impartial verdict.
7. **Verification Agent**: Extracts research claims and verifies each against source data using deterministic Python calculations.
8. **Reliability Engine**: Evaluates evidence quality, claim audit pass rate, source coverage, and agent agreement to calculate the Research Reliability Score.

---

## 🧮 Deterministic Mathematical Models

### 1. Claim $\rightarrow$ Evidence Verification

To ensure that research assertions are backed by factual source data, claims are validated using strict numerical calculations rather than LLM discretion:

$$\text{Calculated Growth \%} = \frac{\text{Current Revenue} - \text{Previous Revenue}}{\text{Previous Revenue}} \times 100$$

- **Verified (`ok`)**: Mathematical discrepancy $|\text{Claimed} - \text{Calculated}| \le 2.0\%$.
- **Partially Verified (`warn`)**: Empirical metric confirmed from primary quotes, but historical baseline relies on multi-year estimates.
- **Unsupported (`bad`)**: Forward guidance, speculative management claims, or assertions with zero backing in filing data.

### 2. Research Reliability Score

> **Important Terminology**: This metric is strictly named the **Research Reliability Score**. It measures how reliable the research process and underlying evidence are. It is **never** referred to as investment probability or stock return prediction.

The final score ($0-100$) is calculated using the documented weighting formula:

$$\text{Reliability Score} = 0.30 \cdot S_{\text{evidence}} + 0.30 \cdot S_{\text{claims}} + 0.20 \cdot S_{\text{coverage}} + 0.20 \cdot S_{\text{agreement}}$$

| Component | Weight | Criteria Evaluated |
|---|:---:|---|
| **Evidence Quality** | $30\%$ | Presence of audited balance sheet entries, quotes, and primary filings |
| **Claim Verification** | $30\%$ | Ratio of verified and partially verified claims vs unsupported assertions |
| **Source Coverage** | $20\%$ | Completeness of fundamental ratios, multi-year revenue, and news coverage |
| **Agent Agreement** | $20\%$ | Factual convergence between Bull, Bear, and Judge agent analyses |

---

## 📁 Project Directory Structure

```text
EquityMind AI/
├── README.md
├── EquityMind AI (1).html                   # Original design prototype (Source of Truth)
├── backend/
│   ├── .env.example                         # Environment template
│   ├── requirements.txt                     # Python dependencies
│   └── app/
│       ├── main.py                          # FastAPI application, middleware & CORS
│       ├── api/
│       │   └── routes/
│       │       ├── company.py               # GET /api/v1/company/search
│       │       ├── copilot.py               # POST /api/v1/copilot
│       │       ├── health.py                # GET /api/v1/health
│       │       └── research.py              # POST /api/v1/research, GET /research/{id}
│       ├── core/
│       │   └── config.py                    # Pydantic v2 application settings
│       ├── schemas/
│       │   ├── company.py                   # Company resolution models
│       │   ├── copilot.py                   # Copilot request/response contracts
│       │   ├── debate.py                    # Bull/Bear arguments and Judge models
│       │   ├── financial.py                 # Balance sheet, margins & quote schemas
│       │   ├── news.py                      # Article and sentiment models
│       │   ├── reliability.py               # Research Reliability Score breakdown
│       │   ├── research.py                  # Full research state schemas
│       │   ├── valuation.py                 # Valuation multiple models
│       │   └── verification.py              # Claim verification & evidence schemas
│       ├── agents/
│       │   ├── bear_agent.py                # Bearish thesis & risk analysis
│       │   ├── bull_agent.py                # Bullish thesis & growth drivers
│       │   ├── data_agent.py                # Financial market data fetcher
│       │   ├── judge_agent.py               # Impartial debate adjudicator
│       │   ├── news_agent.py                # Recent news aggregator
│       │   ├── valuation_agent.py           # Multiple & margin evaluator
│       │   └── verification_agent.py        # LangGraph claim auditor node
│       ├── services/
│       │   ├── claim_verifier.py            # Python claim verification engine
│       │   ├── company_resolver.py          # Deterministic company ticker search
│       │   ├── copilot_service.py           # Grounded Copilot reasoning engine
│       │   ├── market_data.py               # yfinance data client & normalizer
│       │   ├── reliability_calculator.py    # Deterministic reliability formula
│       │   └── research_service.py          # Workflow orchestrator & memory cache
│       └── workflows/
│           ├── research_state.py            # LangGraph state typed definition
│           └── research_workflow.py         # 7-node LangGraph execution graph
└── frontend/
    ├── package.json                         # React 19, TypeScript, Vite, Oxlint
    ├── tsconfig.json                        # Strict TypeScript configuration
    ├── vite.config.ts                       # Vite build configuration
    └── src/
        ├── App.tsx                          # App state & workspace routing
        ├── main.tsx                         # DOM entry point
        ├── types/index.ts                   # TypeScript interfaces matching backend
        ├── pages/
        │   ├── LandingPage.tsx              # Initial hero search screen
        │   └── ResearchWorkspace.tsx        # Central 4-tab intelligence workspace
        ├── components/
        │   ├── AgentPipeline.tsx            # Live agent execution steps
        │   ├── ClaimsTab.tsx                # Verified claims & calculation proofs
        │   ├── CompanySearch.tsx            # Autocomplete & typo-tolerant search
        │   ├── CompanySuggestions.tsx       # Trending company quick-select
        │   ├── DataTab.tsx                  # Fundamental metrics & history table
        │   ├── DebateTab.tsx                # Bull vs Bear cases + Judge verdict
        │   ├── ReliabilityScore.tsx         # Radial score gauge & metric cards
        │   ├── ReportTab.tsx                # Executive research dossier
        │   ├── ResearchCopilot.tsx          # Grounded conversational interface
        │   ├── SelectedCompany.tsx          # Active ticker badge & change action
        │   └── WorkspaceHeader.tsx          # Company summary & action triggers
        └── services/
            ├── api.ts                       # Axios/Fetch HTTP client for backend
            ├── copilotService.ts            # Copilot query delegation
            └── mockData.ts                  # Design system initial fallbacks
```

---

## 📡 API Reference

Base URL: `http://127.0.0.1:8000/api/v1`

### 1. Health Check
`GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "EquityMind AI Backend",
  "version": "1.0.0"
}
```

---

### 2. Company Search & Resolution
`GET /company/search?q={query}`

**Query Parameters:**
- `q` (string, required): Ticker symbol or company name (e.g., `AAPL`, `Apple`, `Microsft`, `Nvidia`).

**Response:**
```json
{
  "query": "Microsft",
  "count": 1,
  "results": [
    {
      "name": "Microsoft Corporation",
      "ticker": "MSFT",
      "exchange": "NASDAQ",
      "market": "US",
      "sector": "Technology"
    }
  ]
}
```

---

### 3. Start Research Workflow
`POST /research`

**Request Body:**
```json
{
  "company": {
    "name": "Apple Inc.",
    "ticker": "AAPL",
    "exchange": "NASDAQ",
    "market": "US",
    "sector": "Technology"
  }
}
```

**Response (`201 Created`):**
Returns the complete research state, including:
- `research_id`: Unique identifier for the research session
- `financial_data`: Real-time quote, P/E, EPS, margins, and revenue history
- `news`: Recent headlines, source links, and sentiment tags
- `valuation`: Multiple comparisons and growth metrics
- `debate`: Bull arguments, Bear arguments, and Judge adjudication
- `claims`: Array of audited claims with source data, formulas, and proofs
- `reliability_score`: Overall score ($0-100$) and 4-metric breakdown
- `agent_status`: Completion status for all 7 pipeline agents

---

### 4. Retrieve Research Dossier
`GET /research/{research_id}`

Retrieves an existing research state by its unique `research_id`.

---

### 5. Research Copilot Query
`POST /copilot`

**Request Body:**
```json
{
  "research_id": "1a61b1f8-eb84-4430-ac2e-db14f3f1824e",
  "question": "Why is the valuation expensive?"
}
```

**Response (`200 OK`):**
```json
{
  "research_id": "1a61b1f8-eb84-4430-ac2e-db14f3f1824e",
  "answer": "AAPL trades at a trailing valuation multiple of 39.4x against its 5-year historical baseline of ~24.8x, representing a significant 1.59x premium. Both the Valuation Agent and Bear Agent highlight that multiple expansion has outpaced revenue growth.",
  "sources_cited": ["Claim 3", "Valuation Analysis", "Historical Benchmark"],
  "is_grounded": true,
  "sample": false
}
```

---

## 💬 Grounded Research Q&A

The Research Q&A interface is strictly grounded in the research state of the selected company:

### Supported Queries
- **"Why is the valuation expensive?"**: Retrieves valuation multiples, compares them against historical baselines, and cites Bear Agent arguments.
- **"What are the biggest risks?"**: Details risks identified by the Bear Agent, including valuation stretch and market saturation.
- **"Show me evidence behind the bullish thesis."**: Highlights audited claims backing the Bull Agent's case with filing references.
- **"Challenge the current conclusion."**: Summarizes the Judge Agent's critical analysis of both sides of the debate.
- **"Why did the reliability score decrease?"**: Explains the exact mathematical deduction based on the four component scores (e.g., presence of unsupported claims or missing multi-year filings).

### Hallucination Protection
The Copilot will politely reject speculative questions outside the evidence base:
- **Speculative Question**: *"What will the stock price be tomorrow?"*
- **Copilot Answer**: *"This inquiry cannot be answered from EquityMind research evidence. EquityMind AI evaluates audited historical filings, code-calculated multiples, and multi-agent debate for the selected company. It strictly avoids ungrounded price predictions or forward return forecasts."*

---

## 🚀 Getting Started

### Prerequisites

- **Python**: Version 3.10, 3.11, or 3.12
- **Node.js**: Version 18.0.0 or higher
- **npm**: Version 9.0.0 or higher

---

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt

# Start backend server with live reload
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The backend API will be live at `http://127.0.0.1:8000`. Interactive OpenAPI documentation is available at `http://127.0.0.1:8000/docs`.

---

### 2. Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```

The frontend application will be live at `http://localhost:5173`.

---

### 3. Environment Variables

Create a `backend/.env` file (copy from `backend/.env.example`):

```env
# Application Configuration
PROJECT_NAME="EquityMind AI API"
VERSION="1.0.0"
API_V1_STR="/api/v1"
HOST="127.0.0.1"
PORT=8000

# CORS Allowed Origins
CORS_ORIGINS=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"]

# Optional: Google Gemini API Key for narrative generation
GEMINI_API_KEY="your-gemini-api-key"
GEMINI_MODEL="gemini-1.5-flash"
```

> **Note**: If `GEMINI_API_KEY` is not provided, the system seamlessly uses deterministic mathematical calculations and structured algorithmic analysis.

---

## 🧪 Validation & Test Suite

The system has passed end-to-end integration tests across all key capabilities:

1. **API Health**: Verified `GET /api/v1/health` responds with HTTP 200.
2. **Company Search (Exact)**: `Apple` $\rightarrow$ `Apple Inc. (AAPL, NASDAQ)`.
3. **Company Search (Fuzzy/Typo)**: `Microsft` $\rightarrow$ `Microsoft Corporation (MSFT, NASDAQ)`.
4. **Successful Research Execution**: Full 7-agent pipeline execution for `AAPL` resulting in complete research state.
5. **Bull vs Bear Adversarial Debate**: Divergent perspectives evaluated and synthesized by the Judge Agent.
6. **Claim Verification Audit**: Correctly identifies Verified, Partially Verified, and Unsupported assertions.
7. **Research Reliability Formula**: Deterministic computation matching the $30/30/20/20$ weighted model.
8. **Incomplete Company Fallback**: Graceful handling of OTC or data-sparse tickers without application crash.
9. **Invalid Company Fallback**: Defensive error handling when market data is unavailable.
10. **Grounded Copilot Queries**: Evaluates and responds to all five core research questions with source citations.
11. **Copilot Speculation Rejection**: Refuses ungrounded price targets and forward return predictions.
12. **Missing Research Session Handling**: Gracefully handles unknown session IDs while maintaining evidence grounding.

---

## ⚖️ Disclaimer & License

### Disclaimer
EquityMind AI is an educational and analytical research demonstration tool. It does not provide personalized investment advice, financial planning, or endorsement of any security. All valuation multiples, debate arguments, and reliability metrics are generated for research demonstration purposes only. Consult a registered financial advisor before making any investment decisions.

### License
This project is open-source under the MIT License.
