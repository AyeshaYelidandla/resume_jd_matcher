from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import nltk
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def clean_text(text):
    words = word_tokenize(text.lower())
    filtered = [word for word in words if word.isalnum() and word not in stop_words]
    return " ".join(filtered)

def match_resume_with_jd(resume_text, jd_text):
    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(jd_text)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([clean_resume, clean_jd])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100

    resume_words = set(clean_resume.split())
    jd_words = set(clean_jd.split())
    common = resume_words.intersection(jd_words)
    missing = jd_words - resume_words

    improvements = [f"Include or emphasize '{word}' in your resume to better match the job description."
                    for word in sorted(missing)]

    return {
        "score": np.round(similarity, 2),
        "explanation": f"The resume matches the job description with a score of {similarity:.2f}%. "
                       f"Strong matches include: {', '.join(sorted(common))}. "
                       f"Consider adding these keywords to improve your match: {', '.join(sorted(missing))}.",
        "strong_skills": sorted(common),
        "improvements": improvements
    }
