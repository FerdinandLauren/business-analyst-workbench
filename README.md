# Business Analyst Workbench

A small tool that turns plain-language business notes into reviewable analysis
artifacts: candidate requirements, a draft BRD, process-gap observations, and
UAT scenarios.

It is not tied to the procurement demo. Paste notes about a clinic, a warehouse,
a support desk, or any other process and the same engine runs. English and
Indonesian are both supported, including the generated documents.

> Portfolio prototype. Every output is a draft and must be checked by a human
> stakeholder. The app does not approve requests, move money, or replace an
> analyst.

## Features

- **Generic input.** Write one sentence per problem or expectation; the engine
  splits the text and classifies each sentence. No scenario-specific templates.
- **Deterministic by default.** The local engine is rule-based: no API key, no
  network, no data leaving the machine.
- **Language toggle (EN / ID)** in the top-right corner. The interface, tables,
  BRD, and UAT text follow the selected language. The language is auto-detected
  from the input until you pick one by hand.
- **Four workspaces.** Requirement analyzer, BRD draft, process analyzer, and
  UAT generator, each with its own input so one tab never borrows another tab's
  text.
- **Exports.** Requirements and UAT scenarios download as CSV; the BRD downloads
  as Markdown.
- **Optional AI drafting.** A visitor can paste their own OpenAI-compatible API
  key in the sidebar. If the call fails or no key is present, the app quietly
  falls back to the local draft.

## Quick start

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python -m streamlit run app/streamlit_app.py
```

Open `http://localhost:8501`. Use `python -m streamlit` rather than the bare
`streamlit` command if the launcher is not on your PATH.

Run the tests with:

```bash
python -m unittest discover -s tests -v
```

## How the engine decides

Every sentence goes through the same three steps, all in `src/`:

1. **Detect a topic.** A dictionary maps terms to categories such as
   `scheduling`, `payment`, `approval`, `reporting`, and `integration`. Matching
   is word-boundary based, so `WhatsApp` does not match `sap`.
2. **Detect the pain.** A second dictionary maps wording such as "manual",
   "bentrok", "salah", or "tidak tahu" to one of five pain groups:
   consolidation, visibility, accuracy, automation, or none.
3. **Fill a template.** The statement combines the pain verb, the category noun,
   and the expected outcome.

Example:

```text
Input:  Kasir mencatat pembayaran manual.
Topic:  payment
Pain:   automation
Output: Sistem harus mengotomatiskan pencatatan pembayaran agar pekerjaan
        manual berkurang.
```

Sentences that match nothing become `unclassified` requirements with
`needs_review` status and an open question, so the gap is visible instead of
being silently dropped. The BRD lists those questions in its final sections,
and process areas with no evidence are reported as `unspecified`.

## Project structure

```text
app/streamlit_app.py     Streamlit shell: layout, per-tab state, language toggle
src/i18n.py              English/Indonesian strings and language detection
src/text.py              Word-boundary dictionaries, sentence splitting
src/requirements.py      Requirement extraction, priorities, table rows
src/process.py           As-Is / To-Be comparison per process area
src/uat.py               Category-aware UAT scenarios
src/brd.py               Markdown BRD assembled from the same inputs
src/llm.py               Optional user-supplied key, never required
tests/                   Unit and end-to-end tests
samples/                 Fictional stakeholder notes used by the tests
docs/                    Plan, design notes, sample deliverables
ai/prompts/              Prompt templates for optional AI drafting
```

## Limitations

- Classification is heuristic. Synonyms outside the dictionaries fall into
  `unclassified`; extend the tables in `src/text.py` rather than trusting a
  guess.
- One sentence produces at most one requirement, so compound sentences should
  be split by the author.
- Priorities are category-based defaults, not a substitute for stakeholder
  negotiation.
- AI output can be incomplete or overconfident. The app labels which engine
  produced a draft, and human review is still mandatory.
- The sample company and data are fictional. Do not paste confidential data into
  a third-party API without authorization.

## License

MIT. See [LICENSE](LICENSE).
