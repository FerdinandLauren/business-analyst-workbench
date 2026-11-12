from pathlib import Path
import sys, os
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from src.analyzer import extract_candidate_requirements, analyze_process, make_uat_cases
from src.generator import brd_markdown, ai_or_fallback

load_dotenv()
st.set_page_config(page_title="AI Business Analyst Workbench", page_icon="🧭", layout="wide")

st.title("AI Business Analyst Workbench")
st.caption("From business problem to draft requirements, process insights, and UAT scenarios.")
st.warning("Portfolio prototype only. All generated content is a draft and must be validated by a human stakeholder.")

with st.sidebar:
    st.header("Project workspace")
    project_name = st.text_input("Project name", "Procurement Process Improvement")
    st.markdown("---")
    st.markdown("**Demo scenario**")
    st.caption("Fictional manufacturing company improving purchase-request intake, approval visibility, and auditability.")
    st.markdown("---")
    st.caption("AI mode: API if configured; otherwise local fallback.")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Requirement Analyzer", "2. BRD Draft", "3. Process Analyzer", "4. UAT Generator"
])

default_problem = (
    "Employees submit purchase requests through email and spreadsheets. "
    "Required information is sometimes missing, so the procurement team must ask for corrections. "
    "Approvals are handled through separate email conversations. "
    "Requesters cannot easily track request status. "
    "Managers need an audit history and a dashboard to monitor pending requests."
)
default_objective = (
    "Create a centralized and traceable purchase-request workflow that improves data quality, "
    "approval visibility, and management oversight while keeping approval decisions with authorized people."
)

with tab1:
    st.subheader("Turn a business problem into candidate requirements")
    problem = st.text_area("Business problem / stakeholder notes", default_problem, height=150)
    if st.button("Analyze requirements", key="analyze_req", type="primary"):
        st.session_state["requirements"] = extract_candidate_requirements(problem)
        st.session_state["problem"] = problem
    reqs = st.session_state.get("requirements", [])
    if reqs:
        st.dataframe(pd.DataFrame(reqs), use_container_width=True, hide_index=True)
        st.download_button("Download requirements CSV",
            pd.DataFrame(reqs).to_csv(index=False).encode("utf-8"),
            "candidate-requirements.csv", "text/csv")
        st.info("These are candidate statements. Confirm actor, trigger, business rule, priority, and acceptance criteria with stakeholders.")

with tab2:
    st.subheader("Generate a structured BRD draft")
    problem_brd = st.text_area("Business problem", default_problem, height=100, key="brd_problem")
    objective = st.text_area("Business objective", default_objective, height=80)
    stakeholders = st.text_area("Stakeholders", "Requester; Procurement Officer; Department Manager; Finance; IT/Application Support")
    c1, c2 = st.columns(2)
    with c1:
        scope_in = st.text_area("In scope", "Digital request intake; mandatory-field validation; approval routing; status tracking; audit history; management dashboard")
    with c2:
        scope_out = st.text_area("Out of scope", "Automatic payment execution; supplier contract negotiation; replacement of the enterprise ERP")
    reqs_for_brd = st.session_state.get("requirements") or extract_candidate_requirements(problem_brd)
    if st.button("Generate BRD", type="primary", key="generate_brd"):
        fallback = brd_markdown(project_name, problem_brd, objective, stakeholders, scope_in, scope_out, reqs_for_brd)
        prompt = (
            "Create a BRD draft using only the facts below. Clearly mark assumptions and open questions. "
            "Do not invent approval thresholds or service levels.\n\n"
            f"Project: {project_name}\nProblem: {problem_brd}\nObjective: {objective}\n"
            f"Stakeholders: {stakeholders}\nIn scope: {scope_in}\nOut of scope: {scope_out}\n"
            f"Candidate requirements: {reqs_for_brd}"
        )
        draft, mode = ai_or_fallback(prompt, fallback)
        st.session_state["brd"] = draft
        st.session_state["brd_mode"] = mode
    if "brd" in st.session_state:
        st.caption(st.session_state.get("brd_mode", "Draft"))
        st.markdown(st.session_state["brd"])
        st.download_button("Download BRD Markdown", st.session_state["brd"],
                           "BRD-draft.md", "text/markdown")

with tab3:
    st.subheader("Compare current and proposed processes")
    as_is = st.text_area("As-Is process", "Requester emails a spreadsheet. Procurement checks fields manually and asks for missing information. Approval occurs in email threads. Requester contacts procurement to ask for status.")
    to_be = st.text_area("To-Be process", "Requester submits a standardized online form. The system validates mandatory fields and shows request status. The workflow routes requests to authorized approvers. Notifications are sent and an audit log records status changes.")
    if st.button("Analyze process gaps", type="primary"):
        st.session_state["process_gaps"] = analyze_process(as_is, to_be)
    if "process_gaps" in st.session_state:
        st.dataframe(pd.DataFrame(st.session_state["process_gaps"]), use_container_width=True, hide_index=True)
        st.caption("Keyword-based observations are prompts for analyst investigation, not proof of process improvement.")

with tab4:
    st.subheader("Create draft UAT scenarios")
    reqs_uat = st.session_state.get("requirements") or extract_candidate_requirements(default_problem)
    if st.button("Generate UAT scenarios", type="primary"):
        st.session_state["uat"] = make_uat_cases(reqs_uat)
    if "uat" in st.session_state:
        uat_df = pd.DataFrame(st.session_state["uat"])
        st.dataframe(uat_df, use_container_width=True, hide_index=True)
        st.download_button("Download UAT CSV", uat_df.to_csv(index=False).encode("utf-8"),
                           "uat-scenarios.csv", "text/csv")

st.markdown("---")
st.caption("Built as a Business Analysis + AI + Automation portfolio prototype. Synthetic scenario only.")
