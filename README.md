# NovaAI

### Enterprise AI Transformation Intelligence

NovaAI is a local-first enterprise AI transformation intelligence platform designed to systematically evaluate how and where an organisation should adopt artificial intelligence. Rather than acting as a conversational chatbot, NovaAI analyzes end-to-end business processes, identifies granular AI opportunities, evaluates them through deterministic scoring formulas, retrieves grounded research evidence via semantic vector search, assesses multi-dimensional governance risks, and links opportunities directly to enterprise roles, skills, transformation initiatives, and blocking dependencies.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=flat&logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)
![pgvector](https://img.shields.io/badge/pgvector-0.8.6-336791?style=flat)
![Ollama](https://img.shields.io/badge/Ollama-qwen2.5%3A7b-black?style=flat)

---

## Overview

Most enterprise discussions around AI stall at the stage of brainstorming disconnected use cases. Enterprise transformation requires answering operational, strategic, human, and regulatory questions before writing code or purchasing software:

- Which processes have high automation potential versus requiring human-in-the-loop oversight?
- What evidence supports the feasibility of an AI capability in a regulated domain?
- What data, privacy, regulatory, and model risks accompany an opportunity?
- Which employee roles and skills are impacted by the transformation?
- Which strategic initiatives and technical prerequisites must be delivered first?

NovaAI answers these questions by modeling an enterprise's value chain as a relational knowledge graph backed by PostgreSQL and pgvector. A local large language model decomposes processes and reasons about qualitative factors, while a deterministic FastAPI backend calculates transparent scores and orchestrates entity relationships.

> **Project Context**: NovaAI is a portfolio and research engineering project developed to demonstrate systematic AI transformation architecture. It uses **NovaBank**—a fictional retail and commercial bank—as its demonstration enterprise context.

---

## The Problem

When business leaders ask:

> *"Where can we use AI in our enterprise?"*

A generic LLM prompt yields generic bullet points. A list of ideas does not constitute an actionable transformation roadmap. Enterprise leadership needs concrete decision support:

1. **Granularity**: Processes cannot be automated as monolithic blocks; specific activities must be isolated.
2. **Reproducibility**: Priority scores cannot fluctuate between LLM invocations; they must follow transparent, audit-ready formulas.
3. **Evidence Grounding**: Claims regarding AI viability must cite domain research and empirical benchmarks.
4. **Governance & Risk**: Opportunities must be evaluated across data security, privacy, bias, and regulatory dimensions.
5. **Organizational Impact**: Leadership must know which roles require reskilling and which skill gaps will bottleneck execution.
6. **Execution Sequencing**: Initiatives have dependencies (e.g., data pipelines or governance frameworks that must precede model deployment).

NovaAI addresses this multidimensional problem by converting business workflows into structured enterprise intelligence.

---

## What NovaAI Does

NovaAI executes a structured evaluation pipeline for any enterprise process:

```
Process
  └── Activities
        └── AI Opportunities
              ├── Deterministic Scoring
              ├── Research Evidence (pgvector)
              ├── Governance Assessment
              ├── Role & Skill Matching
              └── Transformation Initiatives
                    └── Initiative Dependencies
                          └── Enterprise Intelligence Dashboard
```

- **Process Decomposition**: Breaks down an operational workflow into granular activities and candidate AI opportunities.
- **Factor Estimation & Validation**: Extracts quantitative factor estimates validated strictly via Pydantic schemas.
- **Deterministic Scoring**: Calculates auditable priority scores using weighted mathematical formulas in the backend.
- **Semantic Research Grounding**: Queries 384-dimensional pgvector embeddings of domain research to retrieve relevant evidence chunks.
- **Governance Risk Scoring**: Evaluates 7 distinct risk dimensions (data, privacy, bias, security, decision impact, regulatory, model risk).
- **Transformation Linking**: Matches opportunities to organizational roles, required skills, and strategic initiatives using token scoring.
- **Dependency Graph Traversal**: Maps initiative dependency chains to expose execution bottlenecks and prerequisites.
- **Enterprise Aggregation**: Aggregates cross-process metrics to surface enterprise-wide transformation priorities and intelligence gaps.

---

## Architecture

NovaAI adopts a layered, local-first architecture designed to separate qualitative probabilistic reasoning from deterministic business governance:

> **Core Architectural Principle**:  
> *LLM reasons. Backend decides. Database remembers.*

![NovaAI System Architecture](docs/images/novaai_architecture_linkedin.png)

**NovaAI system architecture**

### 1. Experience Layer
A single-page application built with **React 19**, **TypeScript**, **Vite**, and **Tailwind CSS v4**. It renders the Executive Intelligence Dashboard, Transformation Priorities, Process Intelligence Drill-Down, Opportunity Detail Drawers, Governance Views, and the Surprise Record ingestion form.

### 2. Intelligence Layer
A **FastAPI** backend that acts as the central orchestrator (`analysis_persistence.py`). It coordinates LLM calls, validates payloads with Pydantic v2, computes priority and risk scores via dedicated scoring engines, performs keyword-based transformation linking, coordinates database persistence, and serves aggregated intelligence endpoints.

### 3. AI Layer
A local instance of **Ollama** serving `qwen2.5:7b` on port 11434 with structured JSON output enforcement. The LLM performs qualitative decomposition, factor estimation, evidence claim extraction, and risk reasoning.

### 4. Semantic Retrieval
A vector pipeline leveraging `sentence-transformers/all-MiniLM-L6-v2` to generate 384-dimensional dense vector embeddings. Embeddings are stored and queried in PostgreSQL using the **pgvector** extension with cosine distance.

### 5. Knowledge Layer
**PostgreSQL 16** with **pgvector**, orchestrated via **SQLAlchemy 2.x** and **psycopg3**. It stores the complete enterprise entity graph: organisations, strategies, value chain stages, processes, activities, opportunities, research sources, chunks, evidence, governance assessments, roles, skills, transformation initiatives, and recursive dependency chains.

---

## Intelligence Pipeline

![NovaAI Intelligence Pipeline](docs/images/novaai_intelligence_pipeline_linkedin.png)

**NovaAI intelligence pipeline**

When an executive or analyst triggers an analysis (either on an existing process or via a newly submitted process), the pipeline executes the following sequence:

1. **Process Input**: The user selects an existing process or submits a new process via the Surprise Record form (`POST /processes/analyze-new`).
2. **LLM Process Decomposition**: The backend constructs a structured prompt and calls Ollama (`qwen2.5:7b`). The model breaks the process into 3 sequential activities and 2 candidate AI opportunities with raw factor estimates ($[0.0, 1.0]$).
3. **Pydantic Validation**: Raw LLM output is validated against the `ProcessAnalysis` Pydantic schema to ensure structural and numeric integrity.
4. **Deterministic Priority Scoring**: The backend `scoring_engine.py` computes the composite priority score for each opportunity using its explicit mathematical formula.
5. **Semantic Research Retrieval**: The backend generates an embedding for the opportunity query (`name + description + ai_capability`) and retrieves the top-3 most similar pre-indexed research chunks from `pgvector` using cosine distance.
6. **Evidence Analysis**: For each retrieved chunk, Ollama evaluates the excerpt against the opportunity, extracting a structured claim, supporting excerpt, relevance score, and confidence score (`EvidenceAnalysis` schema).
7. **Governance Assessment**: Ollama evaluates the opportunity against 7 risk dimensions, estimating raw risk factors and identifying oversight requirements (`GovernanceAnalysis` schema).
8. **Deterministic Governance Scoring**: The backend `governance_scoring.py` computes the weighted overall governance risk score.
9. **Transformation & Role Linking**: The backend `transformation_linker.py` executes token overlap and keyword-matching algorithms to link the process to up to 3 relevant roles and link opportunities to up to 2 strategic transformation initiatives.
10. **Persistence Coordination**: `analysis_persistence.py` orchestrates the persistence of all activities, opportunities, evidence records, governance assessments, role associations, and initiative links into PostgreSQL.
11. **Enterprise Aggregation**: `enterprise_intelligence.py` queries the connected graph across all processes to compute organization-wide rankings, portfolio distributions, role impacts, and dependency paths.
12. **Executive Dashboard**: The frontend queries `/intelligence/enterprise` and `/processes/{id}/intelligence` to display unified enterprise intelligence.

> **Research Architecture Note**: NovaAI's active analysis pipeline utilizes **pre-indexed research chunks** stored in PostgreSQL + pgvector. While the repository contains live web research utilities (`research_engine.py` using DuckDuckGo search and BeautifulSoup), that live search path is currently maintained as a standalone indexing utility and is not executed synchronously during the active analysis request.

---

## AI Architecture

NovaAI enforces strict boundaries between probabilistic model output and deterministic system authority:

```
┌────────────────────────────────────────────────────────┐
│                      PROMPT INPUT                      │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│             Ollama (qwen2.5:7b) Reasoning              │
│   Qualitative analysis · Raw factor estimates [0–1]     │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│             Pydantic Validation Layer                  │
│       Strict schema validation · Type enforcement      │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│            FastAPI Backend Authority                   │
│   Deterministic scoring formulas · Business rules      │
│   Calculates final priority & governance metrics       │
└────────────────────────────────────────────────────────┘
```

### Responsibility Matrix

| Responsibility | Handled By | Implementation |
| :--- | :--- | :--- |
| Process Decomposition | **LLM** | Ollama (`qwen2.5:7b`) via JSON mode |
| Raw Factor Estimation | **LLM** | Feasibility, benefit, automation potential, risk axes |
| Evidence Evaluation | **LLM** | Claim synthesis and confidence estimation |
| Schema Enforcement | **Backend** | Pydantic v2 model validation |
| Final Priority Score | **Backend** | Deterministic weighted formula |
| Final Governance Risk | **Backend** | Deterministic weighted formula |
| Role & Initiative Matching | **Backend** | Deterministic token overlap & domain rules |
| Data Integrity & Graph | **Database** | PostgreSQL 16 relational constraints & pgvector |

### Deterministic Priority Formula

Final opportunity priority scores are calculated directly in Python (`app/services/scoring_engine.py`):

$$\text{Priority Score} = 0.20(\text{automation}) + 0.10(1 - \text{human}) + 0.25(\text{benefit}) + 0.20(\text{feasibility}) + 0.20(\text{strategic}) + 0.05(1 - \text{risk})$$

- $\text{automation}$: Automation Potential ($0.0 - 1.0$)
- $\text{human}$: Human Involvement Level ($0.0 - 1.0$)
- $\text{benefit}$: Expected Business Benefit ($0.0 - 1.0$)
- $\text{feasibility}$: Technical Feasibility ($0.0 - 1.0$)
- $\text{strategic}$: Strategic Alignment ($0.0 - 1.0$)
- $\text{risk}$: Raw Risk Level ($0.0 - 1.0$)

### Deterministic Governance Formula

Overall governance risk is calculated in Python (`app/services/governance_scoring.py`):

$$\text{Overall Risk} = 0.15(\text{data}) + 0.15(\text{privacy}) + 0.10(\text{bias}) + 0.10(\text{security}) + 0.20(\text{decision}) + 0.20(\text{regulatory}) + 0.10(\text{model})$$

Where each factor represents a normalized risk score ($0.0 - 1.0$) across data risk, privacy risk, bias risk, security risk, decision impact, regulatory exposure, and model risk.

---

## Research & Semantic Retrieval

NovaAI incorporates pre-indexed domain research to ground AI opportunity analysis in empirical findings:

```
[Pre-Indexing Workflow]
Research Source URL ──► HTML Extraction (BeautifulSoup) ──► Text Chunking (1200 chars / 200 overlap)
                                                                    │
                                                                    ▼
pgvector Table (ResearchChunk) ◄── 384-dim Vector ◄── sentence-transformers/all-MiniLM-L6-v2

─────────────────────────────────────────────────────────────────────────────────────────────

[Analysis-Time Retrieval]
AI Opportunity ──► Query String ──► generate_embedding() ──► pgvector Cosine Distance (Top-3)
                                                                     │
                                                                     ▼
Evidence Persistence ◄── Claim & Relevance ◄── LLM Evidence Analysis (qwen2.5:7b)
```

- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` generating 384-dimensional dense normalized embeddings.
- **Storage**: `research_chunks` table utilizing the PostgreSQL `vector(384)` data type.
- **Search Metric**: Cosine similarity (`embedding <=> query_vector` order by distance ascending).
- **Retrieval Scope**: The top 3 most relevant chunks are supplied to the evidence analyzer for each opportunity.

---

## Enterprise Intelligence Model

NovaAI models the enterprise as a connected relational hierarchy. The knowledge graph is fully persisted and navigable across strategic, operational, and organizational boundaries:

```mermaid
graph TD
    ORG[Organisation: NovaBank]
    STR[Strategy]
    VC[Value Chain Stage]
    PROC[Process]
    ACT[Activity]
    OPP[AI Opportunity]
    EVI[Evidence]
    SRC[Research Source & Chunks]
    GOV[Governance Assessment]
    ROLE[Role]
    SKILL[Skill]
    INIT[Transformation Initiative]
    DEP[Initiative Dependency]

    ORG --> STR
    ORG --> VC
    VC --> PROC
    PROC --> ACT
    ACT --> OPP
    PROC --> ROLE
    ROLE --> SKILL
    OPP --> EVI
    EVI --> SRC
    OPP --> GOV
    OPP --> INIT
    INIT --> DEP
    DEP -.-> INIT

    style ORG fill:#1e293b,stroke:#334155,color:#f8fafc
    style OPP fill:#1e3a5f,stroke:#2563eb,color:#bfdbfe
    style GOV fill:#14532d,stroke:#16a34a,color:#bbf7d0
    style INIT fill:#3b1f00,stroke:#92400e,color:#fed7aa
```

### Relational Schema Design

- **Organisation**: Root entity holding enterprise identity and domain context.
- **Strategy & Value Chain Stage**: High-level strategic objectives and sequential functional divisions.
- **Process & Activity**: Operational workflows and their constituent decision points.
- **AIOpportunity**: Identified AI capabilities with priority scores, estimated factors, and reasoning.
- **Evidence & ResearchSource**: Grounded research claims linked to source publications and raw chunks.
- **GovernanceAssessment**: 7-factor risk breakdown, oversight requirements, and explainability flags.
- **Role & Skill**: Personnel catalog mapped to processes via `process_roles` and skills via `role_skills`.
- **TransformationInitiative & InitiativeDependency**: Execution projects linked to opportunities with prerequisite dependency relationships.

---

## Surprise Record

To demonstrate that NovaAI is an active intelligence engine rather than a static dashboard displaying pre-seeded data, the system includes the **Surprise Record** capability.

An analyst can submit an unseeded banking process through the UI (e.g., *"Mortgage Payment Default Management"*). In response, the backend:

1. Ingests and persists the new process under the specified Value Chain Stage.
2. Invokes Ollama to dynamically decompose the new process into activities and AI opportunities.
3. Calculates deterministic priority scores for the generated opportunities.
4. Retrieves top semantic research chunks matching the newly created opportunities.
5. Evaluates grounded evidence and generates governance risk assessments.
6. Automatically links the process to existing bank roles and transformation initiatives using token matching.
7. Commits the complete graph to PostgreSQL.
8. Re-computes enterprise intelligence, immediately reflecting the new process in enterprise-wide priorities and skill impact metrics.

---

## Executive Intelligence

The frontend dashboard presents synthesized enterprise intelligence derived from cross-entity database aggregation:

- **Enterprise Summary**: Total processes analyzed, opportunities discovered, average priority scores, and identified intelligence gaps.
- **Transformation Priorities**: Ranked opportunities scored across automation potential, feasibility, and strategic value.
- **Process Intelligence Drill-Down**: In-depth view of any process, exposing its activity decomposition, AI opportunities, and linked roles.
- **AI Opportunity Landscape**: Distribution of opportunities across AI capability classes (Computer Vision, NLP, Predictive Analytics, Generative AI).
- **Governance & Risk Review**: Opportunity risk profiles detailing regulatory exposure, oversight requirements, and model transparency flags.
- **Role & Skill Impact**: Aggregated view of which operational roles are most frequently impacted and which skills are in highest demand.
- **Initiative Dependency Graph**: Visualisation of transformation initiatives and the technical or governance prerequisites blocking execution.

---

## Technology Stack

| Layer | Technology | Version / Specification | Purpose |
| :--- | :--- | :--- | :--- |
| **Frontend** | React | `^19.2.8` | Component-driven user interface |
| | TypeScript | `~6.0.2` | Type-safe application logic |
| | Vite | `^8.3.0` | Fast modern frontend tooling |
| | Tailwind CSS | `^4.3.3` | Utility-first responsive design system |
| **Backend** | Python | `3.11.9` | Core backend runtime |
| | FastAPI | `0.141.1` | REST API framework |
| | SQLAlchemy | `2.0.52` | Relational ORM and database abstraction |
| | Pydantic | `2.13.5` | Data validation and schema enforcement |
| | Alembic | `1.20.0` | Database schema migrations |
| | Uvicorn | `0.52.4` | ASGI server |
| **AI / NLP** | Ollama | Local runtime | Host for open-weights LLMs |
| | Qwen 2.5 | `7b` | Process decomposition & qualitative reasoning |
| | sentence-transformers | `6.0.1` | Local dense vector embedding generation |
| | all-MiniLM-L6-v2 | 384 dimensions | Pre-trained semantic retrieval model |
| **Data** | PostgreSQL | `16` | Primary relational database |
| | pgvector | `0.8.6` | Vector similarity search extension |
| | psycopg | `3.3.5` | Modern Python PostgreSQL driver |
| **Research** | BeautifulSoup4 | `4.15.0` | HTML content parsing and extraction |
| | ddgs | `9.16.0` | Standalone research query indexing |
| | HTTPX | `0.28.1` | Asynchronous HTTP client for Ollama & APIs |
| **Infra** | Docker Compose | Local container | Containerized PostgreSQL 16 + pgvector |

---

## Data Model

The schema is defined using SQLAlchemy 2.0 declarative models in `app/models/`:

```
Organisation (1) ───< Strategy (N)
Organisation (1) ───< ValueChainStage (N) ───< Process (N)
                                                 │
              ┌──────────────────────────────────┴──────────────────────────────────┐
              ▼                                                                     ▼
        Activity (N)                                                           ProcessRole (N)
              │                                                                     │
    ActivityAIOpportunity (N)                                                    Role (1)
              │                                                                     │
       AIOpportunity (1)                                                       RoleSkill (N)
              │                                                                     │
  ┌───────────┼───────────────────────────┐                                      Skill (1)
  ▼           ▼                           ▼
Evidence  GovernanceAssessment  AIOpportunityInitiative (N)
  │                                       │
ResearchSource (1)            TransformationInitiative (1)
  │                                       │
ResearchChunk (N)               InitiativeDependency (N)
```

- **Core Entities**: `Organisation`, `Strategy`, `ValueChainStage`, `Process`, `Activity`, `Role`, `Skill`, `AIOpportunity`, `TransformationInitiative`.
- **Knowledge & Evidence**: `ResearchSource`, `ResearchChunk` (stores `vector(384)`), `Evidence`, `GovernanceAssessment`.
- **Association Tables**:
  - `ProcessRole` (`process_id`, `role_id`): Links affected roles to processes.
  - `RoleSkill` (`role_id`, `skill_id`): Links competencies to roles.
  - `ActivityAIOpportunity` (`activity_id`, `ai_opportunity_id`): Maps opportunities to workflow activities.
  - `AIOpportunityInitiative` (`ai_opportunity_id`, `initiative_id`, `relationship_type`): Links transformation initiatives to opportunities.
  - `InitiativeDependency` (`initiative_id`, `depends_on_initiative_id`, `dependency_type`): Recursive self-referential table modeling project prerequisites.

---

## Running Locally

### Prerequisites

Ensure you have the following installed on your host machine:

- **Python**: `3.11` (tested on 3.11.9)
- **Node.js**: `18+` or `20+` (with `npm`)
- **Docker Desktop**: For running PostgreSQL with pgvector
- **Ollama**: Installed and running locally
- **Ollama Model**: `qwen2.5:7b` (`ollama pull qwen2.5:7b`)

---

### Step 1: Database Setup

Start the containerized PostgreSQL database with the pgvector extension:

```bash
docker compose up -d
```

Verify that the database container `novaai-postgres` is running on port `5432`:

```bash
docker ps
```

---

### Step 2: Backend Setup

Navigate to the `backend/` directory:

```bash
cd backend
```

Create and activate a Python 3.11 virtual environment:

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install fastapi uvicorn sqlalchemy alembic psycopg psycopg-binary pgvector pydantic pydantic-settings python-dotenv sentence-transformers beautifulsoup4 ddgs httpx
```

Configure your environment variables in `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://novaai:novaai_dev_password@localhost:5432/novaai
```

Run database migrations using Alembic:

```bash
alembic upgrade head
```

Seed initial enterprise data:

```bash
# Creates the NovaBank organisation, strategy, and 5 value chain stages
python -m app.db.seed

# Populates 8 banking roles, the skills catalog, and role-skill associations
python -m app.db.seed_roles_skills
```

*(Note: `seed_evidence.py` is an optional auxiliary script that links a sample research source to an existing `AIOpportunity #1` after process analysis has run).*

Start the FastAPI application:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Verify backend health by navigating to `http://127.0.0.1:8000/health` and `http://127.0.0.1:8000/health/db`.

---

### Step 3: Frontend Setup

Open a new terminal and navigate to `frontend/`:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

Open your browser and navigate to `http://localhost:5173`.

---

## Example Workflow

1. **Launch the System**: Start the Docker container, FastAPI backend, local Ollama runtime, and Vite frontend.
2. **Access Executive Overview**: Open `http://localhost:5173` to view the **Enterprise Intelligence Dashboard** displaying aggregated transformation metrics for NovaBank.
3. **Inspect a Value Chain Process**: Select an existing seeded process (such as *"Credit Assessment"*) to inspect its activity decomposition.
4. **Drill Down into AI Opportunities**: Click on an AI opportunity to review its automation score, feasibility rating, and supporting qualitative rationale.
5. **Inspect Grounded Evidence & Governance**: Review the top research chunks retrieved via pgvector and view the 7-dimension governance assessment.
6. **Analyze Organizational Impact**: Observe which bank roles (e.g., Credit Analyst, Compliance Officer) and competencies are impacted by the opportunity.
7. **Trace Project Dependencies**: Check which strategic initiatives support the opportunity and identify blocking prerequisite initiatives.
8. **Test Dynamic Ingestion (Surprise Record)**: Submit a brand new process (e.g., *"Fraud Detection & AML Transaction Monitoring"*) and observe the backend decompose, score, retrieve evidence, and integrate the new process into the enterprise graph in real time.

---

## Engineering Decisions

### 1. LLM as Reasoner, Backend as Authority
Probabilistic models should not be granted autonomous decision-making authority over enterprise metrics. In NovaAI, the LLM provides qualitative process decomposition and raw factor estimates, while deterministic backend formulas validate inputs via Pydantic and compute final priority and risk scores. This makes the final business metrics transparent and reproducible given the validated input factors.

### 2. Deterministic Scoring Over Generative Ratings
Allowing an LLM to directly output a priority score (e.g., *"Score: 85/100"*) produces arbitrary and non-comparable values. NovaAI calculates scores using explicit, transparent weighting formulas where each coefficient can be tuned to reflect corporate strategy without altering model prompts.

### 3. Pre-Indexed Semantic Retrieval Over Unconstrained Live Web Search
Live web search during synchronous analysis introduces latency, network fragility, and non-deterministic search engine outputs. NovaAI separates the research ingestion pipeline from the runtime analysis pipeline: domain publications are pre-chunked, embedded, and indexed in pgvector, enabling deterministic, low-latency semantic grounding at analysis time.

### 4. Relational Knowledge Graph Over Vector-Only Memory
Chat-based RAG architectures frequently treat memory as unstructured text stored in a vector index. NovaAI treats enterprise transformation as an entity-relational knowledge graph. Entities such as processes, roles, skills, and initiatives have explicit foreign keys and association tables in PostgreSQL, allowing recursive dependency traversal and exact aggregation.

### 5. Activity as the Bridge from Process to Opportunity
Business processes are too broad to automate directly. NovaAI requires the LLM to first decompose a process into sequential activities, and then attach AI opportunities to individual activities. This reflects actual systems engineering practice, where automation targets discrete operational tasks.

### 6. Synchronous Orchestration with Persistence Coordination
To ensure that all generated entities maintain referential integrity without orphan records, `analysis_persistence.py` orchestrates the complete execution flow, coordinating LLM invocations, vector searches, and entity persistence across the relational schema.

---

## Engineering Focus & Key Learnings

NovaAI was built to explore and demonstrate practical enterprise AI engineering patterns:

- **API Design**: Designing cohesive REST endpoints connecting complex enterprise data models with single-page frontend views.
- **Relational Data Modeling**: Architecting 18 SQLAlchemy ORM models with self-referential trees, association tables, and referential integrity.
- **Vector Search Integration**: Implementing pgvector embeddings within a standard SQLAlchemy 2.0 ORM workflow.
- **Structured LLM Outputs**: Enforcing deterministic JSON output and Pydantic validation across multi-stage LLM chains.
- **Auditable AI Scoring**: Implementing transparent mathematical scoring formulas that separate model reasoning from corporate authority.
- **Graph Traversal**: Implementing recursive dependency resolution for strategic initiative roadmapping.

---

## Current Limitations

As a local-first portfolio implementation, NovaAI has defined architectural boundaries:

- **Authentication & Authorization**: The platform currently operates in a single-tenant local environment without user authentication or role-based access control (RBAC).
- **Synchronous Analysis Runtime**: The analysis pipeline executes synchronously within a single HTTP request; extensive LLM reasoning passes can take 30–60 seconds on standard consumer hardware.
- **Pre-Indexed Research Requirement**: Grounded evidence depends on previously indexed research sources in the database; live web search is not currently connected to the active request flow.
- **Automated Test Coverage**: The repository currently contains manual exploratory test scripts for LLM and analyzer components, but comprehensive automated end-to-end regression testing is limited.
- **Local Deployment Constraints**: Designed for local development with Docker Compose and local Ollama, rather than distributed cloud infrastructure.

---

## Future Improvements

- **Asynchronous Task Execution**: Offload process analysis to a background queue (e.g., Celery or Redis Streams) with WebSocket status updates to the frontend.
- **HNSW Indexing on Vector Store**: Add HNSW or IVFFlat vector indexing to `research_chunks.embedding` to optimize retrieval speeds at scale.
- **Live Search Ingestion Pipeline**: Connect the existing DuckDuckGo research scraper to an automated background indexing worker that enriches the knowledge base continuously.
- **Dynamic Scoring Configuration**: Allow administrators to configure priority and governance formula weights through the UI.
- **Role-Based Authentication**: Integrate OAuth2 / JWT authentication to support multi-stakeholder enterprise workflows.
- **Automated End-to-End Test Suite**: Comprehensive pytest integration suite with database fixtures validating all 18 entity relationships.

---

## Project Structure

*Abbreviated structure showing the primary application and documentation files:*

```
novaai/
├── docker-compose.yml              # PostgreSQL 16 + pgvector container definition
├── README.md                       # Comprehensive project documentation
├── docs/
│   ├── architecture/               # Architecture diagrams, Mermaid sources, & documentation
│   │   ├── diagram1_system_architecture.mmd
│   │   ├── diagram2_intelligence_pipeline.mmd
│   │   ├── novaai_architecture_diagrams.md
│   │   ├── novaai_architecture_linkedin.png
│   │   └── novaai_intelligence_pipeline_linkedin.png
│   └── images/                     # Embedded visual assets
│       ├── novaai_architecture_linkedin.png
│       ├── novaai_intelligence_pipeline_linkedin.png
│       ├── dashboard_overview.png
│       ├── transformation_intelligence.png
│       ├── transformation_dependencies.png
│       └── surprise_record.png
├── backend/
│   ├── alembic.ini                 # Alembic migration configuration
│   ├── alembic/                    # Database migration versions
│   │   ├── env.py
│   │   └── versions/               # 10 migration scripts
│   ├── app/
│   │   ├── main.py                 # FastAPI application factory & route registration
│   │   ├── api/                    # REST API route handlers
│   │   │   ├── processes.py        # Process CRUD, analysis, & drill-down
│   │   │   ├── initiatives.py      # Transformation initiatives API
│   │   │   ├── initiative_links.py # Opportunity-initiative links API
│   │   │   ├── initiative_dependencies.py # Dependency chains API
│   │   │   └── enterprise_intelligence.py # Aggregated intelligence endpoint
│   │   ├── db/                     # Database session and seeders
│   │   │   ├── database.py         # SQLAlchemy engine and sessionmaker
│   │   │   ├── seed.py             # NovaBank enterprise seed data
│   │   │   ├── seed_roles_skills.py# Banking roles and skills seed data
│   │   │   └── seed_evidence.py    # Seed research sources and evidence
│   │   ├── models/                 # SQLAlchemy 2.0 ORM models (18 classes)
│   │   │   ├── organisation.py
│   │   │   ├── strategy.py
│   │   │   ├── value_chain.py
│   │   │   ├── process.py
│   │   │   ├── activity.py
│   │   │   ├── role.py
│   │   │   ├── skill.py
│   │   │   ├── ai_opportunity.py
│   │   │   ├── research_source.py
│   │   │   ├── research_chunk.py
│   │   │   ├── evidence.py
│   │   │   ├── governance.py
│   │   │   ├── initiative.py
│   │   │   └── initiative_dependency.py
│   │   ├── schemas/                # Pydantic v2 validation schemas
│   │   │   ├── process.py
│   │   │   ├── activity.py
│   │   │   ├── ai_opportunity.py
│   │   │   ├── evidence.py
│   │   │   ├── governance.py
│   │   │   └── initiative.py
│   │   └── services/               # Core business & intelligence logic
│   │       ├── process_analyzer.py # LLM prompt construction & decomposition
│   │       ├── scoring_engine.py   # Deterministic priority score calculation
│   │       ├── governance_analyzer.py # LLM governance risk assessment
│   │       ├── governance_scoring.py  # Deterministic governance risk calculation
│   │       ├── evidence_analyzer.py   # LLM claim evaluation against chunks
│   │       ├── embedding_service.py   # Sentence Transformers all-MiniLM-L6-v2
│   │       ├── opportunity_research.py# pgvector cosine distance search
│   │       ├── research_storage.py    # Vector search queries
│   │       ├── research_engine.py     # Standalone DuckDuckGo & HTML scraper
│   │       ├── transformation_linker.py # Keyword role & initiative matching
│   │       ├── analysis_persistence.py# Central pipeline orchestrator
│   │       └── enterprise_intelligence.py # Cross-entity graph aggregation
│   ├── test_analyzer.py            # Exploratory analyzer component test
│   ├── test_evidence_analyzer.py   # Exploratory evidence analyzer test
│   ├── test_llm.py                 # Exploratory Ollama LLM integration test
│   └── test_process_analyzer.py    # Exploratory process decomposition test
└── frontend/
    ├── package.json                # React 19, TypeScript, Tailwind CSS v4
    ├── vite.config.ts              # Vite bundler configuration
    ├── index.html                  # Single page entry point
    └── src/
        ├── main.tsx                # React DOM root
        ├── App.tsx                 # Executive dashboard, drawers, & intelligence views
        ├── services/
        │   └── api.ts              # Fetch client communicating with FastAPI
        └── index.css               # Design tokens and Tailwind configuration
```

---

## Application

NovaAI provides an executive-facing interface for exploring enterprise transformation intelligence across processes, AI opportunities, roles, skills, governance, evidence, initiatives, and dependencies.

### Executive Intelligence

![NovaAI Executive Intelligence Dashboard](docs/images/dashboard_overview.png)

The executive dashboard provides an enterprise-level view of analyzed processes, identified AI opportunities, roles, skills, and transformation initiatives.

### Transformation Intelligence

![NovaAI Transformation Intelligence](docs/images/transformation_intelligence.png)

The transformation view connects business processes with AI opportunities and exposes their transformation priorities across the enterprise.

### Transformation Dependencies

![NovaAI Transformation Dependencies](docs/images/transformation_dependencies.png)

Transformation initiatives can be connected through dependency chains, making upstream prerequisites visible before downstream initiatives are executed.

### Dynamic Process Analysis

![NovaAI Surprise Record](docs/images/surprise_record.png)

NovaAI can accept a previously unseen process and run the analysis pipeline dynamically, generating activities, AI opportunities, and a deterministic priority score before persisting the result.

---

## License

License: Not specified yet.

---

## Why NovaAI?

NovaAI demonstrates how an enterprise AI application can bridge business architecture and artificial intelligence engineering:

Instead of relying on ephemeral chatbot interactions, NovaAI combines **structured process decomposition**, **local LLM reasoning**, **auditable deterministic decision logic**, **semantic vector grounding via pgvector**, **multi-dimensional risk governance**, and **relational dependency mapping** into a coherent, persistent intelligence platform.
