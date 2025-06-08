import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import tempfile
from extract.extract import extract_text_from_pdf
from matcher.matching import match_resume_with_jd
from llm.llm import generate_llm_match

st.set_page_config(page_title="AI Resume & JD Matcher", layout="centered")
st.title("📄 AI Resume and JD Matcher")

resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
jd_text = st.text_area("Paste the Job Description")

if resume_file and jd_text:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(resume_file.read())
        tmp_path = tmp_file.name

    resume_text = extract_text_from_pdf(tmp_path)
    resume_text = " ".join(resume_text) if isinstance(resume_text, list) else resume_text
    jd_text = " ".join(jd_text) if isinstance(jd_text, list) else jd_text

    # TF-IDF Score
    result = match_resume_with_jd(resume_text, jd_text)
    score = float(result.get("score", 0.0))
    explanation = result.get("explanation", "")
    improvements = result.get("improvements", [])
    strong_skills = result.get("strong_skills", [])

    st.success(f"✅ TF-IDF Match Score: **{score:.2f}%**\n\n{explanation}")
    st.markdown("### 🔍 Suggestions to Improve Resume:")
    for imp in improvements:
        st.markdown(f"- {imp}")
    st.markdown("### 💪 Strong Skills Detected:")
    st.code(", ".join(strong_skills))

    # LLM-Based Feedback
    st.markdown("### 🤖 LLM-Based Feedback & Resume Suggestions")
    try:
        llm_response = generate_llm_match(resume_text, jd_text,"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")
        st.info(llm_response)
    except Exception as e:
        st.error("❌ LLM Error: Could not generate response.\n" + str(e))
