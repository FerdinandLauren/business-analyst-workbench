# Workbench v2 Implementation Plan

> **For agentic workers:** implement task by task. Do not commit until the
> task's test command passes. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Every tab accepts an arbitrary problem statement and produces a
readable draft in English or Indonesian, fully offline, with an optional
user-supplied API key.

**Architecture:** Pure engine modules in `src/` (no Streamlit imports) + thin UI
in `app/streamlit_app.py`. Detection = curated dictionaries with word-boundary
regex, no stemming, no substring matching. Statements are assembled from
category × pain-group templates, so output is deterministic and testable.

**Tech Stack:** Python 3.10+, Streamlit 1.49+, pandas, stdlib `unittest`,
optional `openai` (already installed, used only when a key is supplied).

**Spec:** `docs/design.md`

## Global Constraints

- No new runtime dependencies. `openai` is imported only inside the function
  that uses a key.
- Engine modules must not import `streamlit`.
- Machine values (`category`, `severity`, `type`, `priority`, `status`) are
  English and stable; only display text is translated.
- Every user-visible string exists in both `en` and `id`.
- `python -m unittest discover -s tests -v` green before every commit.
- No secrets in code, logs, commits, or fixtures.
- One task = one commit, conventional messages, no co-author trailers.

## Review Focus

Each line is pinned by a test in the task named in brackets.

1. Pure Indonesian input with no dictionary hit → `status="needs_review"` and a
   clarification quoting the source, never a generic statement. [Task 4]
2. Substring collisions (`WhatsApp`/`sap`, `superb`/`erp`, `airport`/`api`) →
   no match. [Task 3]
3. Non-procurement BRD → no `ERP`, `supplier`, `approval matrix`,
   `cost center`. [Task 7]
4. Empty / whitespace / one-word input → no exception, no zero division in
   metrics. [Task 5, Task 10]
5. English input with `lang="id"` → Indonesian statement, English machine
   values (`type`, `category`, `priority`). [Task 4]

---

## Shared decisions

### D0. Files that already exist (do not create)

- `ai/prompts/brd-generator.md`, `ai/prompts/requirement-analyzer.md`,
  `ai/prompts/uat-generator.md`
- `samples/procurement-stakeholder-notes.md`
- `docs/design.md`, `docs/plan.md`

Files deleted by this plan: `src/analyzer.py` (Task 4),
`src/generator.py` (Task 9). Their callers are updated in the same commit.

### D1. Category dictionary — `src/text.py`

`CATEGORY_TERMS: dict[str, tuple[str, ...]]`, keys in this order (order breaks
ties):

| key | EN terms | ID terms |
|---|---|---|
| `scheduling` | schedule, scheduling, appointment, booking, reschedule, queue, slot, rota | jadwal, penjadwalan, booking, antrean, antrian, kuota, slot |
| `intake` | form, intake, submit, submission, registration, register, request form | formulir, pendaftaran, pengajuan, permohonan, isi data |
| `approval` | approval, approve, approver, sign-off, authorization, escalation | persetujuan, menyetujui, otorisasi, eskalasi, tanda tangan |
| `payment` | payment, pay, billing, invoice, receipt, refund, checkout, cashier | pembayaran, bayar, tagihan, invoice, struk, kuitansi, kasir, refund, transaksi |
| `reporting` | report, reporting, dashboard, analytics, statistics, kpi, recap | laporan, rekap, dasbor, analitik, statistik, kpi |
| `tracking` | track, tracking, progress, visibility, status | lacak, pelacakan, progres, riwayat status, visibilitas, status |
| `notification` | notification, notify, reminder, alert, email, sms, broadcast | notifikasi, pemberitahuan, pengingat, reminder, email, sms, pengumuman |
| `validation` | validation, validate, verify, verification, mandatory, completeness | validasi, verifikasi, wajib, kelengkapan, cek data |
| `integration` | integration, integrate, sync, synchronization, middleware, erp, sap | integrasi, terintegrasi, sinkronisasi, sambungan sistem, erp, sap, api |
| `audit` | audit, audit trail, trace, retention, compliance | audit, jejak audit, rekam, retensi, kepatuhan, regulasi |
| `search` | search, filter, sort, query, find | pencarian, cari, filter, saring, urutkan |
| `access` | access, role, permission, authentication | akses, hak akses, peran, otentikasi |
| `inventory` | inventory, stock, warehouse, asset, goods | inventaris, stok, gudang, aset, barang, persediaan |
| `support` | complaint, ticket, helpdesk, support, incident | keluhan, komplain, tiket, dukungan, gangguan, insiden |

Deliberately removed (false positives): `pemeriksaan`, `izin`, `log`, `erm`,
bare `api` for ID, `whatsapp` (it is a channel, not an integration).

### D2. Pain groups — `src/text.py`

`PAIN_TERMS: dict[str, tuple[str, ...]]` with **five** groups (this replaces the
earlier 10-key table; grouping is what makes verbs compose with nouns):

| group | terms (ID + EN) |
|---|---|
| `automation` | manual, manualnya, tulis tangan, spreadsheet, excel, buku, kertas, ulang, retype, input ulang, lambat, lama, tertunda, delay, slow, antre panjang, susah, sulit, ribet, merepotkan, membingungkan, confusing |
| `accuracy` | salah, keliru, error, kesalahan, typo, tidak akurat, incorrect, mistake, dobel, duplikat, ganda, duplikasi, duplicate, re-entry, tidak konsisten, beda-beda, tidak seragam, inconsistent, tidak standar, tidak lengkap, kurang lengkap, kosong, belum diisi, missing, incomplete |
| `consolidation` | bentrok, benturan, tumpang tindih, dobel jadwal, double booked, conflict, overlapping |
| `visibility` | tidak tahu, tidak jelas, tidak terlacak, tidak ada kabar, unknown, unclear, no visibility, hilang, tercecer, tidak tercatat, lost, missing record, tidak ada bukti |
| `none` | *(sentinel, never matched)* |

`detect_pain(text) -> str` returns one group (`automation`, `accuracy`,
`consolidation`, `visibility`, or `none`) using the table order.

### D3. NFR dictionary — `src/text.py`

`NFR_TERMS: dict[str, tuple[str, ...]]` keys in this order:
`security` (keamanan, security, enkripsi, encryption, kerahasiaan,
confidentiality), `performance` (performa, performance, response time, waktu
respons, throughput, detik, second), `availability` (ketersediaan, availability,
uptime, downtime, backup, cadangan, pemulihan, recovery), `compliance`
(kepatuhan, compliance, regulasi, regulation, gdpr, uu pdp), `usability`
(kemudahan, usability, user friendly, ramah pengguna, aksesibilitas,
accessibility), `maintainability` (maintainability, pemeliharaan, maintenance,
modular, scalable, skalabilitas, terdokumentasi).

### D4. Requirement rules — `src/requirements.py`

**Sentence filter:** `MIN_SENTENCE_CHARS = 10`, applied in
`extract_requirements`. `GREETINGS = ("halo", "hai", "hi", "hello", "selamat
pagi", "selamat siang", "selamat malam", "terima kasih", "thanks")` — a sentence
whose lowercase text starts with a greeting is skipped. `split_sentences`
itself drops only empty strings.

**Precedence:**
1. If any functional category matches → functional requirement. `type` =
   `"Non-functional"` **only** when the matched category set is exactly
   `{"audit"}` (legacy rule: "audit logs" is non-functional), else
   `"Functional"`. NFR signals are ignored when a functional category matched.
2. Else if `detect_nfr` matches → `type="Non-functional"`,
   `category="nfr_<key>"`.
3. Else → `type="Functional"`, `category="unclassified"`,
   `status="needs_review"`.

**Category choice** when several match: highest number of distinct matched
terms; tie → order in D1.

**Statements.** `PAIN_VERB: dict[lang, dict[group, str]]` and
`PAIN_OUTCOME: dict[lang, dict[group, str]]`:

| group | en verb / outcome | id verb / outcome |
|---|---|---|
| automation | automate / manual re-entry is removed | mengotomatiskan / pekerjaan manual berkurang |
| accuracy | standardise / the same rule applies to every case | menstandarkan / aturan yang sama berlaku untuk semua kasus |
| consolidation | consolidate / one source of truth is used | menyatukan / hanya ada satu sumber data |
| visibility | make visible / users no longer ask for status by message | menampilkan / pengguna tidak perlu bertanya status lewat pesan |
| none | provide / the process is clear and measurable | menyediakan / prosesnya jelas dan terukur |

Patterns: EN `The system shall {verb} {noun} so that {outcome}.` ID `Sistem
harus {verb} {noun} agar {outcome}.`

`CATEGORY_NOUN[lang][category]`:

| key | en | id |
|---|---|---|
| scheduling | appointment scheduling | penjadwalan |
| intake | the request intake form | formulir permohonan |
| approval | the approval workflow | alur persetujuan |
| payment | payment and billing records | pencatatan pembayaran |
| reporting | management reports | laporan manajemen |
| tracking | request status tracking | pelacakan status |
| notification | notifications to users | notifikasi ke pengguna |
| validation | input validation rules | aturan validasi input |
| integration | integration with existing systems | integrasi dengan sistem yang ada |
| audit | the audit trail | jejak audit |
| search | search and filtering | pencarian dan penyaringan |
| access | role-based access control | kontrol akses berbasis peran |
| inventory | inventory records | pencatatan stok |
| support | complaint handling | penanganan keluhan |

NFR statements, fixed text per key (no interpolation):
`nfr_security` EN `The system shall protect data in transit and at rest, with
access limited to authorised roles.` / ID `Sistem harus melindungi data saat
dikirim dan disimpan, dengan akses terbatas pada peran berwenang.` — and the
same shape for `performance`, `availability`, `compliance`, `usability`,
`maintainability` (text authored in `src/i18n.py`, keys
`req.nfr_<key>`).

Unclassified statement: EN `The system shall support: "{fragment}".` / ID
`Sistem harus mendukung: "{fragment}".` where `fragment` = first 8 words of the
sentence without trailing punctuation. `clarification` = `t("req.clarification",
lang, fragment=fragment)` with EN `Clarify with the stakeholder: what outcome is
expected for "{fragment}"?` and ID `Konfirmasi ke stakeholder: hasil apa yang
diharapkan dari "{fragment}"?`

**Priority (D5):** `needs_review` → `Medium`; `nfr_security` and
`nfr_compliance` → `High`; category in `{approval, payment, audit, integration}`
→ `High`; otherwise `Medium`. `Low` is unused.

**Dataclass:** `Requirement(id, type, category, statement, priority, status,
clarification, source_sentence)` — frozen; no `rationale` field.

Expected output for `"Jadwal sering bentrok karena dicatat di buku."`:
EN `The system shall consolidate appointment scheduling so that one source of
truth is used.` ID `Sistem harus menyatukan penjadwalan agar hanya ada satu
sumber data.`

### D6. i18n — `src/i18n.py` (complete in Task 2)

`STRINGS: dict[lang, dict[key, str]]`, `t(key, lang="en", **fmt)`,
`detect_language(text)`. `t` raises `KeyError` for unknown keys.

Markers for `detect_language` (whole-word counting; tie or empty → `"en"`):
`ID_MARKERS = ("dan","atau","yang","tidak","dengan","untuk","dari","agar",
"sering","pada","juga","masih","belum","kami","kita","harus","bisa","sudah",
"oleh","dalam","kalau","supaya","adalah","akan","ini","itu")`
`EN_MARKERS = ("the","and","or","with","for","from","that","this","need",
"needs","must","should","users","user","system","not","can","we","our","is",
"are","be","by","in","on","of","to")`

Key groups (all present in both languages after Task 2):

- `ui.*`: `app_title`, `app_caption`, `disclaimer`, `sidebar_project`,
  `language`, `tab_requirements`, `tab_brd`, `tab_process`, `tab_uat`,
  `btn_analyze`, `btn_brd`, `btn_process`, `btn_uat`, `download_reqs`,
  `download_brd`, `download_uat`, `empty_state`, `stale_input`, `ai_expander`,
  `ai_key`, `ai_model`, `ai_enable`, `ai_caption_local`, `ai_caption_llm`,
  `ai_reset`, `step_analyze_hint`.
- `req.*`: `col_id`, `col_type`, `col_category`, `col_statement`,
  `col_priority`, `col_status`, `type_functional`, `type_nonfunctional`,
  `status_draft`, `status_needs_review`, `clarification`,
  `statement_unclassified`, plus `nfr_security`, `nfr_performance`,
  `nfr_availability`, `nfr_compliance`, `nfr_usability`,
  `nfr_maintainability`.
- `cat.*`: one label per D1 key + `unclassified` + `nfr_*` keys.
- `proc.*`: `area_visibility`, `area_validation`, `area_approval`,
  `area_notification`, `area_auditability`, `severity_improve`,
  `severity_clarify`, `severity_regression`, `severity_unspecified`,
  `col_area`, `col_severity`, `col_observation`, `col_evidence`,
  `metric_manual`, `metric_handoffs`, `metric_improve`.
- `uat.*`: `col_test_id`, `col_requirement_id`, `col_scenario`,
  `col_preconditions`, `col_steps`, `col_expected`, `col_priority`,
  `col_status`, `status_not_run`, plus `steps_<category>`,
  `precondition_<category>`, `expected_<category>` for every D1 key and
  `unclassified` (steps are newline-separated, numbered `1.`…).
- `brd.*`: `section_summary`, `section_problem`, `section_objectives`,
  `section_stakeholders`, `section_scope_in`, `section_scope_out`,
  `section_requirements`, `section_traceability`, `section_assumptions`,
  `section_questions`, `section_acceptance`, `assumption_<category>` for every
  D1 key, `assumption_general`, `assumption_nfr`, `question_general`,
  `trace_header`, `status_line`, `footer`, `objective_derived_<group>` for the
  four D2 groups.

### D7. UAT rules — `src/uat.py`

`make_uat_cases(reqs: list[Requirement], lang="en") -> list[dict[str,str]]` with
keys `test_id, requirement_id, scenario, preconditions, steps, expected_result,
priority, status`. `steps` = `t("uat.steps_<category>")`, `preconditions` =
`t("uat.precondition_<category>")`, `expected_result` =
`t("uat.expected_<category>")`; unknown category falls back to
`unclassified`. `priority` copies the requirement; `status` = `t("uat.status_not_run")`.

Step content requirement: `approval` (submit → approver acts → status changes →
audit entry visible), `payment` (record → totals reconcile → receipt issued),
`reporting` (open → filter period → totals match source), `scheduling`
(book → conflict rejected → reschedule keeps history). Every other category
reuses the `unclassified` steps but must be non-empty in both languages.

### D8. Process tables — `src/process.py`

```
AREA_KEYS = ("visibility", "validation", "approval", "notification", "auditability")
AREA_TERMS = {
  "visibility":    ("status", "track", "tracking", "lacak", "pelacakan", "dashboard", "dasbor", "visibilitas"),
  "validation":    ("validate", "validation", "validasi", "verifikasi", "mandatory", "wajib", "kelengkapan"),
  "approval":      ("approval", "approve", "persetujuan", "menyetujui", "otorisasi"),
  "notification":  ("notification", "notify", "notifikasi", "pemberitahuan", "reminder", "pengingat"),
  "auditability":  ("log", "audit", "jejak", "history", "riwayat", "rekam"),
}
MANUAL_MARKERS  = ("manual", "email", "spreadsheet", "excel", "buku", "kertas", "telepon", "whatsapp", "input ulang", "retype")
HANDOFF_MARKERS = ("email", "whatsapp", "telepon", "chat", "rapat", "meeting", "diteruskan", "forward", "cc", "berjenjang")
```

`analyze_process(as_is, to_be, lang="en")` returns
`{"rows": [{"area","severity","observation","evidence"}],
"summary": {"manual_steps","handoffs","areas_to_improve"}}`.

- severity: `improve` (term only in To-Be), `regression` (only in As-Is),
  `clarify` (both), `unspecified` (neither).
- `evidence` = the first matched term per side, formatted
  `"as-is: {term} | to-be: {term}"` with `-` for a missing side.
- `summary` counts **distinct matched markers** (case-insensitive), not
  occurrences: `"Email, spreadsheet, dan telepon"` → `manual_steps=3`.
- `areas_to_improve` counts `improve` rows only.

---

## Tasks

### Task 1: Repo scaffold, license, first commit

**Files:** create `LICENSE`.

- [ ] **Step 1:** `git init -b main`; set local `user.name "Ferdinand Lauren"`,
      `user.email "ferdinandlauren78@gmail.com"`.
- [ ] **Step 2:** MIT `LICENSE`, `Copyright (c) 2026 Ferdinand Lauren`.
- [ ] **Step 3:** Verify `.gitignore` covers `.venv/`, `.env`,
      `.streamlit/secrets.toml`, `__pycache__/`, `*.py[cod]`.
- [ ] **Step 4:** Commit existing files untouched:
      `chore: import project with design docs and license`.

### Task 2: i18n + language detection (complete)

**Files:** create `src/i18n.py`, `tests/test_i18n.py`.

**Interfaces (produces):** `LANGS`, `STRINGS`, `t`, `detect_language`,
`ID_MARKERS`, `EN_MARKERS` exactly as D6.

- [ ] **Step 1:** `tests/test_i18n.py` with: `test_key_parity` (set difference
      both ways, failure message lists keys), `test_format`
      (`t("ui.stale_input", "id")` non-empty and
      `t("req.clarification", "en", fragment="x")` contains `"x"`),
      `test_detect_id` (`"Pasien mendaftar lewat telepon"` → `"id"`),
      `test_detect_en` (`"Managers need a dashboard"` → `"en"`),
      `test_detect_empty` (`""` → `"en"`), `test_unknown_key_raises`
      (`KeyError` for `"nope"`), `test_all_categories_have_labels`
      (every D1 key + `unclassified` + every `nfr_*` key has `cat.*` in both
      languages).
- [ ] **Step 2:** Run `python -m unittest tests.test_i18n -v`; expect
      `ModuleNotFoundError`.
- [ ] **Step 3:** Implement the **full** D6 key set in one file, both languages.
- [ ] **Step 4:** Run; expect pass.
- [ ] **Step 5:** Commit `feat: add bilingual strings and language detection`.

### Task 3: Text detection helpers

**Files:** create `src/text.py`, `tests/test_text.py`.

**Interfaces (produces):** `split_sentences`, `normalize`, `has_term`,
`detect_categories`, `detect_pain`, `detect_nfr`, `matched_terms`,
`MIN_SENTENCE_CHARS`, `GREETINGS`, plus D1–D3 tables.

- [ ] **Step 1:** Tests:
      `has_term("kirim lewat WhatsApp", "sap") is False`;
      `has_term("superb service", "erp") is False`;
      `has_term("the airport bus", "api") is False`;
      `has_term("The system uses SAP", "sap") is True`;
      `detect_categories("Pasien mendaftar lewat WhatsApp") == ["notification"]`;
      `"integration" not in detect_categories("Pasien mendaftar lewat WhatsApp")`;
      `"integration" in detect_categories("The system integrates with SAP ERP")`;
      `detect_categories("Jadwal sering bentrok") == ["scheduling"]`;
      `detect_pain("Jadwal sering bentrok") == "consolidation"`;
      `detect_pain("Kasir menghitung pembayaran manual") == "automation"`;
      `detect_pain("tidak ada yang tahu statusnya") == "visibility"`;
      `detect_nfr("Response time under 2 seconds") == "performance"`;
      `detect_nfr("Jadwal dokter") is None`;
      `len(split_sentences("Satu. Dua? Tiga!")) == 3`.
- [ ] **Step 2:** Run; expect `ModuleNotFoundError`.
- [ ] **Step 3:** Implement with a cached helper
      `_pattern(term) = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)`.
- [ ] **Step 4:** Run; expect pass.
- [ ] **Step 5:** Commit `refactor: add word-boundary text detection tables`.

### Task 4: Requirement generator

**Files:** create `src/requirements.py`, `tests/test_requirements.py`; delete
`src/analyzer.py` and `tests/test_analyzer.py` in the same commit.

**Interfaces (produces):** `Requirement` (D4 fields),
`extract_requirements(problem, lang="en")`,
`requirements_to_rows(reqs, lang)`.

- [ ] **Step 1:** Tests:
      dental input → `["scheduling","payment","reporting"]` ⊆ categories,
      statement starts with `Sistem harus`, ids `REQ-001…`;
      same text `lang="en"` → statement starts with `The system shall`;
      English text + `lang="id"` → statement contains `Sistem harus` while
      `type == "Functional"` and `category` stays an English key (Review Focus
      5);
      no-match sentence → `status="needs_review"`, `category="unclassified"`,
      `clarification` contains the quoted fragment;
      `"The system must provide audit logs"` → `type == "Non-functional"`,
      `category == "audit"`, `priority == "High"` (Review Focus on legacy rule);
      `"Response time under 2 seconds"` → `category == "nfr_performance"`;
      `"Sistem harus cepat menampilkan laporan"` → `category == "reporting"`
      (functional wins);
      priority table: `payment` → `High`, `reporting` → `Medium`;
      `""` and `"halo"` and `"ok"` → `[]`;
      duplicate sentences → one requirement;
      `requirements_to_rows(reqs, "id")[0]` has localized header keys from
      `req.col_*`.
- [ ] **Step 2:** Run; expect failure.
- [ ] **Step 3:** Implement D4 + D5.
- [ ] **Step 4:** Run; expect pass.
- [ ] **Step 5:** Commit `feat: generate requirements from any problem statement`.

### Task 5: Process analysis

**Files:** create `src/process.py`, `tests/test_process.py`.

- [ ] **Step 1:** Tests: `improve` / `regression` / `clarify` / `unspecified`
      one case each; `evidence == "as-is: email | to-be: -"` for a regression
      case; `analyze_process("Email, spreadsheet, dan telepon", "", "id")
      ["summary"]["manual_steps"] == 3`; handoffs with `"diteruskan lewat
      email"` → `1`; `analyze_process("", "")` → 5 rows all `unspecified`,
      summary `{"manual_steps":0,"handoffs":0,"areas_to_improve":0}`;
      localized `observation` contains no English word when `lang="id"`.
- [ ] **Step 2:** Run; expect failure.
- [ ] **Step 3:** Implement D8.
- [ ] **Step 4:** Run; expect pass.
- [ ] **Step 5:** Commit `feat: derive process gaps from detected evidence`.

### Task 6: UAT generator

**Files:** create `src/uat.py`, `tests/test_uat.py`.

- [ ] **Step 1:** Tests with real `Requirement` objects: approval vs reporting
      `steps` differ; `steps` starts with `"1."`; `requirement_id` matches;
      `priority` mirrors the requirement; `unclassified` still has non-empty
      `steps`, `preconditions`, `expected_result`; `[]` → `[]`; `lang="id"`
      output contains `Masuk` and never `Sign in`.
- [ ] **Step 2:** Run; expect failure.
- [ ] **Step 3:** Implement D7 with the D6 strings.
- [ ] **Step 4:** Run; expect pass.
- [ ] **Step 5:** Commit `feat: generate category-aware UAT scenarios`.

### Task 7: BRD builder

**Files:** create `src/brd.py`, `tests/test_brd.py`; modify `src/generator.py`
so its `brd_markdown` delegates to `src.brd.brd_markdown` (keeping the
`project_name` keyword for the UI until Task 9).

**Interfaces (produces):** `brd_markdown(project, problem, objective,
stakeholders, scope_in, scope_out, reqs, lang="en", process=None) -> str`.
Traceability is built by calling `make_uat_cases(reqs, lang)` internally;
`process` is optional and, when given, its `unspecified` areas become extra open
questions.

- [ ] **Step 1:** Tests: dental BRD contains none of `ERP`, `supplier`,
      `approval matrix`, `cost center`; procurement BRD contains
      `approval thresholds`; traceability row count equals requirement count and
      ids pair as `REQ-001 → UAT-001`; ID BRD contains `Ringkasan` and `## 1.`;
      empty `reqs` → headings present, no table row; `process` with one
      `unspecified` area adds one open question; NFR-only input does not raise
      (`assumption_nfr` used).
- [ ] **Step 2:** Run; expect failure.
- [ ] **Step 3:** Implement with assumptions limited to detected categories and
      `assumption_general` as fallback.
- [ ] **Step 4:** Run; expect pass.
- [ ] **Step 5:** Commit `feat: build BRD sections from input`.

### Task 8: Optional user API key

**Files:** create `src/llm.py`, `tests/test_llm.py`.

**Interfaces (produces):** `generate_with_key(prompt, api_key, model="gpt-4.1-mini") -> str | None`,
`load_prompt(name) -> str`, `resolve_api_key(session_key=None) -> str`
(session → env `OPENAI_API_KEY` → `""`). Never raises, never logs the key.

- [ ] **Step 1:** Tests with `unittest.mock.patch("openai.OpenAI")`: empty key →
      `None` and the constructor is not called; constructor raising → `None`;
      `load_prompt("brd-generator")` non-empty; `resolve_api_key("k") == "k"`;
      `resolve_api_key(None) == ""` with env cleared; return value stripped.
- [ ] **Step 2:** Run; expect failure.
- [ ] **Step 3:** Implement with a local import inside the function and a
      `try/except Exception` returning `None`.
- [ ] **Step 4:** Run; expect pass.
- [ ] **Step 5:** Commit `feat: support optional user-supplied API key`.

### Task 9: Streamlit UI

**Files:** modify `app/streamlit_app.py` (rewrite); delete `src/generator.py`
and update the import sites.

- [ ] **Step 1:** Header `st.columns([9, 3])`; right column
      `st.segmented_control("", ["EN", "ID"], default=None)` with
      `label_visibility="collapsed"`; map selection to `st.session_state["lang"]`
      and set `st.session_state["lang_manual"] = True` on change.
- [ ] **Step 2:** Language default: if `lang` unset, `detect_language(problem)`
      at the first analyze; a manual choice is never overridden.
- [ ] **Step 3:** Sidebar: project name, `st.expander(t("ui.ai_expander"))`
      with password input, model input, checkbox; when no key show
      `t("ui.ai_caption_local")`; key lives only in `st.session_state["api_key"]`;
      reset button clears session state.
- [ ] **Step 4:** Requirements tab: text area + button; results recomputed from
      the current text; if `st.session_state["req_hash"] != hash(text, lang)`
      show `t("ui.stale_input")` instead of old rows; blank input shows
      `t("ui.empty_state")`; CSV download.
- [ ] **Step 5:** BRD tab: own problem/objective/scope inputs; requirements
      derived from **its own** text; when a key exists and the checkbox is on,
      call `generate_with_key(load_prompt("brd-generator") + prompt, key, model)`
      and fall back to `brd_markdown` with `t("ui.ai_caption_local")` naming the
      fallback; Markdown download.
- [ ] **Step 6:** Process tab: rows table with localized headers, three
      `st.metric` values from `summary`, guard against empty input.
- [ ] **Step 7:** UAT tab: own problem text; steps rendered as markdown; CSV
      download.
- [ ] **Step 8:** Replace `use_container_width=True` with `width="stretch"`
      everywhere; bump `requirements.txt` to `streamlit>=1.49,<2.0`.
- [ ] **Step 9:** Manual run (default procurement + dental input, both
      languages, all four tabs), confirm zero console errors and the app boots
      from a clean session state.
- [ ] **Step 10:** Commit `feat: rebuild UI with language toggle and clean state`.

### Task 10: Regression and edge-case tests

**Files:** create `tests/test_integration.py`.

- [ ] **Step 1:** End-to-end: dental input, both languages, extract → process →
      uat → brd; assert no `ERP|supplier|approval matrix` in the BRD, one UAT
      case per requirement, and that statement language follows `lang`.
- [ ] **Step 2:** Edge cases: `""`, `"   "`, `"ok"`, a 5 000-character
      paragraph (finishes under 2 s), mixed ID/EN, and the content of
      `samples/procurement-stakeholder-notes.md`.
- [ ] **Step 3:** Run the full suite; fix engine gaps, not expectations.
- [ ] **Step 4:** Commit `test: cover generic and edge-case inputs`.

### Task 11: Docs

**Files:** modify `README.md`, `PANDUAN-INDONESIA.md`; modify `docs/design.md`
only if implementation deviates.

- [ ] **Step 1:** README: features, limitations (heuristic, draft-only),
      language toggle, optional key, module map (one line per `src/` module),
      run command `python -m streamlit run app/streamlit_app.py`, test command.
- [ ] **Step 2:** Add "How the engine decides" (dictionary → pain group →
      template, no LLM by default) plus one input → output example.
- [ ] **Step 3:** PANDUAN: same content in Indonesian, correct venv commands.
- [ ] **Step 4:** Commit `docs: document the deterministic engine and setup`.

### Task 12: CI and publish

**Files:** create `.github/workflows/tests.yml`.

- [ ] **Step 1:** On `push`/`pull_request`, matrix `3.11/3.12/3.13`,
      `pip install -r requirements.txt`,
      `python -m unittest discover -s tests -v`.
- [ ] **Step 2:** Commit `ci: run unit tests on push`.
- [ ] **Step 3:** Owner runs `gh auth login`.
- [ ] **Step 4:** Create the public repo `business-analyst-workbench` and push
      after every 2–3 commits, never one final dump. Confirm the last Actions
      run is green.
