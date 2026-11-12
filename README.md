# AI Business Analyst Workbench

A portfolio-grade, balanced Business Analysis + AI + Automation project.

**Scenario:** A fictional manufacturing company wants to improve its purchase-requisition and approval process. The workbench turns a business problem into structured requirements, a draft BRD, process-gap analysis, and UAT scenarios.

> This is a learning and portfolio project. It is not an enterprise procurement system, does not approve purchases, and does not replace human review. Generated requirements and test cases are drafts.

## What this project demonstrates

- Business problem framing and stakeholder analysis
- Functional and non-functional requirements
- As-Is / To-Be process analysis
- Draft BRD generation
- UAT scenario generation and CSV export
- AI-assisted analysis with a deterministic local fallback
- A sample n8n workflow for a human-reviewed document-intake process
- Basic test coverage and documented evaluation criteria

## Quick start

### 1. Requirements

- Python 3.10+
- Git (optional, for publishing to GitHub)

### 2. Create a virtual environment

**Windows PowerShell**
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies and run

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`).

## Optional: enable AI-assisted drafting

The application works without an API key using a local rule-based draft generator. To enable an OpenAI-compatible API:

1. Copy `.env.example` to `.env`.
2. Add your API key and a model available to your account.
3. Install dependencies (the `openai` package is included).
4. Restart Streamlit.

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

Do not commit `.env` or expose API keys in screenshots, code, or GitHub. If AI is unavailable, use the local fallback and label the result as a draft.

## Project structure

```text
ai-business-analyst-workbench/
├── app/                 # Streamlit interface
├── src/                 # Reusable analysis and generation logic
├── docs/                # Business analysis deliverables
├── diagrams/            # Mermaid process and architecture diagrams
├── ai/
│   ├── prompts/          # Prompt templates
│   └── evaluation/       # Evaluation rubric and sample cases
├── automation/          # Example n8n workflow (human approval required)
├── samples/             # Fictional business scenario input
├── tests/               # Unit tests
├── .env.example
├── .gitignore
└── requirements.txt
```

## Main application modules

1. **Requirement Analyzer** — extracts candidate requirements from a problem statement and classifies them.
2. **BRD Draft** — creates a structured first draft for analyst review.
3. **Process Analyzer** — compares current and proposed processes and highlights likely control gaps.
4. **UAT Generator** — creates test scenarios and acceptance criteria for review.
5. **Export** — download generated outputs as Markdown or CSV.

## Example scenario

A requester submits a purchase request by email or spreadsheet. Approvals happen through separate messages, and requesters cannot easily see status. The proposed workflow centralizes request intake, validates required fields, routes approvals based on policy, and records status changes. A person remains responsible for every approval decision.

See [`docs/BRD.md`](docs/BRD.md), [`docs/process-analysis.md`](docs/process-analysis.md), and [`docs/UAT.md`](docs/UAT.md).

## Quality and limitations

- The sample company, people, and process are fictional.
- AI output may be incomplete, inaccurate, or overly confident. Verify every requirement with stakeholders.
- The sample automation is illustrative; configure credentials, data retention, access controls, and approval policies before any real deployment.
- This project does not connect to an ERP, issue purchase orders, or make financial decisions.
- Never upload confidential company or personal data to an AI service without authorization.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Publish to GitHub

Create an empty repository on GitHub, then run:

```bash
git init
git add .
git commit -m "Initial AI Business Analyst Workbench"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ai-business-analyst-workbench.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## Suggested portfolio description

**AI Business Analyst Workbench** is a prototype that supports the early stages of business and systems analysis. It transforms a fictional procurement problem into draft requirements, BRD sections, process-gap observations, and UAT scenarios. The project combines structured Business Analysis methods with AI-assisted drafting and a human-in-the-loop automation concept.

## Roadmap

- [ ] Validate generated requirements with a mock stakeholder interview
- [ ] Add BPMN diagrams created in a modeling tool
- [ ] Add role-based access and audit trail for a production-grade prototype
- [ ] Add a database-backed project history
- [ ] Evaluate AI output against the rubric in `ai/evaluation/rubric.md`
- [ ] Add a sample Power BI dashboard using synthetic data
