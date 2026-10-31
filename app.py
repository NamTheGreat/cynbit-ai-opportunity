import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Ensure src is in python path
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from aria_evaluator.pipeline import AriaEvaluationPipeline
from aria_evaluator.models import HiringRecommendation

st.set_page_config(
    page_title="Aria Studio Evaluator | Cynbit AI Opportunity",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Aria Studio Evaluator")
st.subheader("Autonomous Multi-Agent Technical Assessment & Codebase Quality Platform")
st.caption("AI/ML Proof of Concept for Cynbit Technologies — Created by Naman Kalia")

pipeline = AriaEvaluationPipeline()

# Sidebar: Evaluation Mode
st.sidebar.header("🎯 Evaluation Configuration")
eval_mode = st.sidebar.radio(
    "Select Target Source:",
    ["Evaluate Cybit Backend Codebase", "Evaluate Custom Snippet / Preset", "Evaluate Local Directory"]
)

target_name = "Cynbit Backend Reference Architecture"
files = {}

if eval_mode == "Evaluate Cybit Backend Codebase":
    codebase_dir = Path(__file__).parent.parent / "codebase"
    st.sidebar.info(f"Analyzing local codebase at `{codebase_dir}`")
    if codebase_dir.exists():
        files = pipeline.ingestor.ingest_directory(str(codebase_dir))
    else:
        st.error("Codebase directory not found.")

elif eval_mode == "Evaluate Custom Snippet / Preset":
    preset = st.sidebar.selectbox(
        "Choose Code Preset:",
        ["High Quality Backend Architecture", "Vulnerable Candidate Submission"]
    )
    if preset == "High Quality Backend Architecture":
        target_name = "Clean Architecture Submission"
        files = {
            "src/server.ts": """
import { z } from 'zod';
import express from 'express';

const app = express();
const EnvSchema = z.object({
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
});

export function startServer() {
  console.log("Server initialized safely with typed env.");
}
""",
            "src/security/ssrf.ts": """
import net from 'node:net';

export function isPrivateOrReservedIp(ip: string): boolean {
  if (ip === '127.0.0.1' || ip.startsWith('10.') || ip.startsWith('192.168.')) return true;
  if (ip === '169.254.169.254') return true; // AWS IMDS link-local
  return false;
}
""",
            "tests/server.test.ts": """
import { describe, it, expect } from 'vitest';
import { isPrivateOrReservedIp } from '../src/security/ssrf';

describe('SSRF Guard', () => {
  it('blocks AWS IMDS', () => {
    expect(isPrivateOrReservedIp('169.254.169.254')).toBe(true);
  });
});
"""
        }
    else:
        target_name = "Vulnerable Code Submission"
        files = {
            "app.py": """
import requests
import os

API_KEY = "AKIA1234567890EXAMPLESECRETKEY12" # Hardcoded Secret

def fetch_user_avatar(url):
    # Unvalidated SSRF
    return requests.get(url).content

def search_users(db, query):
    # SQL injection vulnerability
    raw_query = f"SELECT * FROM users WHERE name = '{query}'"
    return db.execute(raw_query)

def execute_plugin(code):
    eval(code) # Dangerous RCE
"""
        }

elif eval_mode == "Evaluate Local Directory":
    custom_dir = st.sidebar.text_input("Local Directory Path:", value=str(Path(__file__).parent))
    target_name = Path(custom_dir).name
    if Path(custom_dir).exists():
        files = pipeline.ingestor.ingest_directory(custom_dir)

if st.sidebar.button("🚀 Run Multi-Agent Evaluation", type="primary"):
    with st.spinner("Dispatching agents (Security, Architecture, Clean Code, Synthesis)..."):
        result = pipeline.evaluate_files(files, target_name=target_name)

        # Top metric cards
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Overall Rubric Score", f"{result.overall_score}/100")
        
        rec_color = "🟢" if "HIRE" in result.recommendation.value else "🟡" if "LEANING" in result.recommendation.value else "🔴"
        col2.metric("Recommendation", f"{rec_color} {result.recommendation.value}")
        col3.metric("Total Code Files", result.metrics.total_files)
        col4.metric("Avg Complexity", f"{result.metrics.avg_cyclomatic_complexity:.1f}")

        st.divider()

        # Dimension Breakdown & Chart
        st.subheader("📊 Dimensional Rubric Scores")
        score_df = pd.DataFrame(
            list(result.dimension_scores.items()),
            columns=["Dimension", "Score"]
        )
        st.bar_chart(score_df.set_index("Dimension"))

        # Executive Summary Box
        st.info(f"**Executive Summary:** {result.executive_summary}")

        # Agent Insights Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🛡️ Security Agent", "🏛️ Architecture Agent", "✨ Clean Code Agent", "💡 Actionable Feedback"
        ])

        with tab1:
            sec_agent = result.agent_breakdowns.get("security")
            if sec_agent:
                st.write(f"**Observations:** {sec_agent.key_observations}")
                st.write("**Strengths:**")
                for s in sec_agent.strengths:
                    st.success(f"✓ {s}")
                st.write("**Concerns:**")
                for c in sec_agent.concerns:
                    st.error(f"⚠️ {c}")

            if result.security_findings:
                st.write("### 🚨 Static Security Vulnerabilities")
                sec_records = [
                    {
                        "Rule": sf.rule_id,
                        "Severity": sf.severity.value,
                        "Title": sf.title,
                        "File": f"{sf.file_path}:{sf.line_number}",
                        "CWE": sf.cwe_id,
                        "Remediation": sf.remediation
                    }
                    for sf in result.security_findings
                ]
                st.dataframe(pd.DataFrame(sec_records), use_container_width=True)
            else:
                st.success("No static security anti-patterns or hardcoded secrets detected!")

        with tab2:
            arch_agent = result.agent_breakdowns.get("architecture")
            if arch_agent:
                st.write(f"**Observations:** {arch_agent.key_observations}")
                for s in arch_agent.strengths:
                    st.success(f"✓ {s}")
                for c in arch_agent.concerns:
                    st.warning(f"⚠️ {c}")

        with tab3:
            clean_agent = result.agent_breakdowns.get("clean_code")
            if clean_agent:
                st.write(f"**Observations:** {clean_agent.key_observations}")
                for s in clean_agent.strengths:
                    st.success(f"✓ {s}")
                for c in clean_agent.concerns:
                    st.warning(f"⚠️ {c}")

        with tab4:
            st.write("### 🎯 Candidate Feedback & Next Steps")
            for fb in result.constructive_feedback:
                st.markdown(f"- {fb}")
else:
    st.info("👈 Select an evaluation configuration in the sidebar and click **Run Multi-Agent Evaluation** to see the system in action.")
