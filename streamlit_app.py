import os
import time

import requests
import streamlit as st

# Defaults to localhost for local dev; in Docker Compose this is
# overridden to the API service's container name (see docker-compose.yml).
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="PaperForge", layout="wide")
st.title("PaperForge")
st.caption("Upload a research paper and get a runnable PyTorch implementation.")

# --- Input: file upload or paste ---
input_mode = st.radio("How do you want to provide the paper?", ["Upload a .txt file", "Paste text"])

paper_text = ""

if input_mode == "Upload a .txt file":
    uploaded_file = st.file_uploader("Upload paper (.txt)", type=["txt"])
    if uploaded_file is not None:
        paper_text = uploaded_file.read().decode("utf-8")
else:
    paper_text = st.text_area("Paste the paper text here", height=300)

submit = st.button("Implement this paper", disabled=not paper_text.strip())

if submit:
    with st.spinner("Submitting job..."):
        response = requests.post(f"{API_URL}/papers", json={"paper_text": paper_text})

    if response.status_code != 200:
        st.error(f"Failed to submit: {response.text}")
    else:
        job_id = response.json()["job_id"]
        st.info(f"Job submitted: `{job_id}`")

        status_placeholder = st.empty()
        result = None

        # Poll until the job is done. Simple fixed-interval polling --
        # fine for a demo; a production UI might use websockets or SSE.
        while True:
            poll_response = requests.get(f"{API_URL}/papers/{job_id}")
            data = poll_response.json()
            job_status = data["job_status"]

            status_placeholder.write(f"Status: **{job_status}**")

            if job_status in ("completed", "failed"):
                result = data
                break

            time.sleep(3)

        if result["job_status"] == "failed":
            st.error(f"Job failed: {result.get('error')}")
        else:
            st.success(f"Pipeline verdict: {result.get('pipeline_status')}")

            with st.expander("Analysis", expanded=False):
                st.text(result.get("analysis"))

            with st.expander("Implementation Plan", expanded=False):
                st.text(result.get("plan"))

            with st.expander("Generated Code", expanded=True):
                st.code(result.get("generated_code"), language="python")

            with st.expander("Execution Result", expanded=True):
                st.text(result.get("execution_result"))

            with st.expander("Critique", expanded=False):
                st.text(result.get("critique") or "(none)")

            with st.expander("Evaluation", expanded=True):
                st.text(result.get("evaluation"))

            st.caption(f"Retries used: {result.get('retry_count')}")