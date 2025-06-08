from extract.extract import extract_text_from_pdf
from extract.extract import extract_jd_text
from llm.llm import generate_llm_match

# File paths
resume_path = "data/resumes/Res.pdf"
jd_path = "data/jds/sample_jd.txt"  # make sure this file exists

# Load text
resume_text = extract_text_from_pdf(resume_path)
jd_text = extract_jd_text(jd_path)

# Provide your AI21 API key here
api_key = "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"

# Generate match score using LLM
result = generate_llm_match(resume_text, jd_text, api_key)

# Output result
print("\n🔍 Match Result:\n", result)
