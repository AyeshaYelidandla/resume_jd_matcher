import requests
import os
from pathlib import Path

def load_prompt_template():
    path = Path("prompts/match_prompt.txt")
    return path.read_text()

def generate_llm_match(resume_text, jd_text, api_key):
    prompt_template = load_prompt_template()
    final_prompt = prompt_template.format(resume=resume_text, jd=jd_text)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful job matching assistant."},
            {"role": "user", "content": final_prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if "choices" in result and result["choices"]:
        return result["choices"][0]["message"]["content"].strip()
    else:
        return "Error: Could not generate response"
