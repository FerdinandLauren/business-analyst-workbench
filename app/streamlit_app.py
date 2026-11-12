"""Business Analyst Workbench — Streamlit shell.

All analysis happens in the pure modules under ``src/``. This file only renders
and keeps per-tab state so one tab never borrows another tab's input.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.brd import brd_markdown
from src.i18n import detect_language, t
from src.llm import generate_with_key, load_prompt, resolve_api_key
from src.process import analyze_process
from src.requirements import extract_requirements, requirements_to_rows
from src.uat import make_uat_cases

load_dotenv()
st.set_page_config(page_title="Business Analyst Workbench", page_icon="🧭", layout="wide")

DEFAULT_PROBLEM = (
    "Employees submit purchase requests through email and spreadsheets. "
    "Required information is sometimes missing, so the procurement team must ask for corrections. "
    "Approvals are handled through separate email conversations. "
    "Requesters cannot easily track request status. "
    "Managers need an audit history and a dashboard to monitor pending requests."
)
DEFAULT_OBJECTIVE = (
    "Create a centralized and traceable purchase-request workflow that improves data quality, "
    "approval visibility, and management oversight."
)
DEFAULT_AS_IS = (
    "Requester emails a spreadsheet. Procurement checks fields manually and asks for missing "
    "information. Approval occurs in email threads. Requester contacts procurement to ask for status."
)
DEFAULT_TO_BE = (
    "Requester submits a standardized online form. The system validates mandatory fields and shows "
    "request status. The workflow routes requests to authorized approvers. Notifications are sent and "
    "an audit log records status changes."
)

SESSION_DEFAULTS = {
    "lang": "en",
    "lang_manual": False,
    "lang_pick": "EN",
    "api_key": "",
    "ai_enabled": False,
    "ai_model": "gpt-4.1-mini",
    "project": "Procurement Process Improvement",
}
RESET_KEYS = (
    "req_hash", "req_results", "brd_text", "brd_mode", "process_result",
    "uat_cases", "api_key", "ai_enabled", "ai_model", "lang", "lang_manual",
    "lang_pick", "project",
)
if st.session_state.pop("_reset", False):
    for key in RESET_KEYS:
        st.session_state.pop(key, None)
for key, value in SESSION_DEFAULTS.items():
    st.session_state.setdefault(key, value)

# Pick up the input language unless the visitor chose one by hand. This runs
# before the language widget is created, so changing it here is safe.
if not st.session_state["lang_manual"] and st.session_state.get("req_text", "").strip():
    detected = detect_language(st.session_state["req_text"])
    if detected != st.session_state["lang"]:
        st.session_state["lang"] = detected
        st.session_state["lang_pick"] = detected.upper()

lang = st.session_state["lang"]


def tr(key: str, **fmt) -> str:
    return t(key, lang, **fmt)


def priority_label(value: str) -> str:
    mapping = {"High": "req.priority_high", "Medium": "req.priority_medium", "Low": "req.priority_low"}
    return tr(mapping.get(value, "req.priority_medium"))


title_col, lang_col = st.columns([9, 3], vertical_alignment="center")
with title_col:
    st.title(tr("ui.app_title"))
    st.caption(tr("ui.app_caption"))
with lang_col:
    picked = st.segmented_control(
        tr("ui.language"),
        ["EN", "ID"],
        key="lang_pick",
        label_visibility="collapsed",
    )
    picked = (picked or st.session_state["lang"].upper()).lower()
    if picked != st.session_state["lang"]:
        st.session_state["lang"] = picked
        st.session_state["lang_manual"] = True
        st.rerun()

lang = st.session_state["lang"]
st.warning(tr("ui.disclaimer"))

with st.sidebar:
    st.header(tr("ui.sidebar_project"))
    st.text_input(tr("ui.sidebar_project"), key="project", label_visibility="collapsed")

    with st.expander(tr("ui.ai_expander")):
        st.text_input(tr("ui.ai_key"), key="api_key", type="password")
        st.text_input(tr("ui.ai_model"), key="ai_model")
        st.checkbox(tr("ui.ai_enable"), key="ai_enabled")
        if resolve_api_key(st.session_state["api_key"]):
            st.caption(tr("ui.ai_caption_llm"))
        else:
            st.caption(tr("ui.ai_caption_local"))
        if st.button(tr("ui.ai_reset")):
            st.session_state["_reset"] = True
            st.rerun()

tab_req, tab_brd, tab_proc, tab_uat = st.tabs([
    tr("ui.tab_requirements"), tr("ui.tab_brd"), tr("ui.tab_process"), tr("ui.tab_uat"),
])


def input_key(text: str) -> str:
    return f"{text.strip()}::{lang}"


with tab_req:
    st.subheader(tr("ui.tab_requirements"))
    st.caption(tr("ui.step_analyze_hint"))
    problem = st.text_area(tr("ui.problem_input"), DEFAULT_PROBLEM, height=160, key="req_text")

    if st.button(tr("ui.btn_analyze"), type="primary", key="btn_req"):
        if problem.strip():
            reqs = extract_requirements(problem, lang)
            st.session_state["req_results"] = reqs
            st.session_state["req_hash"] = input_key(problem)
        else:
            st.session_state.pop("req_results", None)
            st.session_state.pop("req_hash", None)

    reqs = st.session_state.get("req_results")
    if not problem.strip():
        st.info(tr("ui.empty_state"))
    elif reqs is None:
        st.info(tr("ui.step_analyze_hint"))
    elif st.session_state.get("req_hash") != input_key(problem):
        st.warning(tr("ui.stale_input"))
    elif reqs:
        rows = requirements_to_rows(reqs, lang)
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
        st.download_button(
            tr("ui.download_reqs"),
            pd.DataFrame(rows).to_csv(index=False).encode("utf-8"),
            "candidate-requirements.csv",
            "text/csv",
        )

with tab_brd:
    st.subheader(tr("ui.tab_brd"))
    project = st.session_state.get("project", "")
    brd_problem = st.text_area(tr("ui.problem_input"), DEFAULT_PROBLEM, height=120, key="brd_problem")
    objective = st.text_area(tr("ui.objective"), DEFAULT_OBJECTIVE, height=80, key="brd_objective")
    stakeholders = st.text_area(tr("ui.stakeholders"),
                                "Requester; Procurement Officer; Department Manager; Finance; IT",
                                key="brd_stakeholders")
    col_in, col_out = st.columns(2)
    with col_in:
        scope_in = st.text_area(tr("ui.scope_in"),
                                "Digital request intake; mandatory-field validation; approval routing; "
                                "status tracking; audit history; management dashboard",
                                key="brd_scope_in")
    with col_out:
        scope_out = st.text_area(tr("ui.scope_out"),
                                 "Automatic payment execution; supplier contract negotiation",
                                 key="brd_scope_out")

    if st.button(tr("ui.btn_brd"), type="primary", key="btn_brd"):
        brd_reqs = extract_requirements(brd_problem, lang)
        local_draft = brd_markdown(
            project, brd_problem, objective, stakeholders, scope_in, scope_out, brd_reqs, lang
        )
        key_value = resolve_api_key(st.session_state["api_key"])
        draft, mode = local_draft, tr("ui.ai_caption_local")
        if key_value and st.session_state["ai_enabled"]:
            prompt = (
                f"{load_prompt('brd-generator')}\n\nProject: {project}\nProblem: {brd_problem}\n"
                f"Objective: {objective}\nStakeholders: {stakeholders}\nIn scope: {scope_in}\n"
                f"Out of scope: {scope_out}\n\nLocal draft to improve:\n{local_draft}"
            )
            ai_draft = generate_with_key(prompt, key_value, st.session_state["ai_model"])
            if ai_draft:
                draft, mode = ai_draft, tr("ui.ai_caption_llm")
        st.session_state["brd_text"] = draft
        st.session_state["brd_mode"] = mode

    if st.session_state.get("brd_text"):
        st.caption(st.session_state.get("brd_mode", ""))
        st.markdown(st.session_state["brd_text"])
        st.download_button(
            tr("ui.download_brd"), st.session_state["brd_text"], "BRD-draft.md", "text/markdown"
        )

with tab_proc:
    st.subheader(tr("ui.tab_process"))
    as_is = st.text_area(tr("ui.as_is"), DEFAULT_AS_IS, height=120, key="proc_as_is")
    to_be = st.text_area(tr("ui.to_be"), DEFAULT_TO_BE, height=120, key="proc_to_be")
    if st.button(tr("ui.btn_process"), type="primary", key="btn_proc"):
        st.session_state["process_result"] = analyze_process(as_is, to_be, lang)

    result = st.session_state.get("process_result")
    if result:
        summary = result["summary"]
        metric_cols = st.columns(3)
        metric_cols[0].metric(tr("proc.metric_manual"), summary["manual_steps"])
        metric_cols[1].metric(tr("proc.metric_handoffs"), summary["handoffs"])
        metric_cols[2].metric(tr("proc.metric_improve"), summary["areas_to_improve"])
        rows = [
            {
                tr("proc.col_area"): tr(f"proc.area_{row['area']}"),
                tr("proc.col_severity"): tr(f"proc.severity_{row['severity']}"),
                tr("proc.col_observation"): row["observation"],
                tr("proc.col_evidence"): row["evidence"],
            }
            for row in result["rows"]
        ]
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

with tab_uat:
    st.subheader(tr("ui.tab_uat"))
    uat_problem = st.text_area(tr("ui.problem_input"), DEFAULT_PROBLEM, height=120, key="uat_problem")
    if st.button(tr("ui.btn_uat"), type="primary", key="btn_uat"):
        uat_reqs = extract_requirements(uat_problem, lang)
        st.session_state["uat_cases"] = make_uat_cases(uat_reqs, lang)

    cases = st.session_state.get("uat_cases")
    if cases:
        rows = [
            {
                tr("uat.col_test_id"): case["test_id"],
                tr("uat.col_requirement_id"): case["requirement_id"],
                tr("uat.col_scenario"): case["scenario"],
                tr("uat.col_preconditions"): case["preconditions"],
                tr("uat.col_steps"): case["steps"],
                tr("uat.col_expected"): case["expected_result"],
                tr("uat.col_priority"): priority_label(case["priority"]),
                tr("uat.col_status"): case["status"],
            }
            for case in cases
        ]
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
        st.download_button(
            tr("ui.download_uat"),
            pd.DataFrame(rows).to_csv(index=False).encode("utf-8"),
            "uat-scenarios.csv",
            "text/csv",
        )

st.markdown("---")
st.caption(tr("ui.disclaimer"))
