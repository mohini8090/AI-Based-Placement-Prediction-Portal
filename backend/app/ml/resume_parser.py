"""
Resume parsing & analysis (Modules 3 & 4). No heavyweight NLP dependency
— transparent keyword/regex matching against SKILL_KEYWORDS. Swap in
spaCy/transformers later without changing the router contract if you
need fuzzier extraction.
"""
import io
import re
from typing import Dict, List

from pypdf import PdfReader
import docx

from app.ml.skills_taxonomy import SKILL_KEYWORDS

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s-]?)?\d{10}")

SECTION_HEADERS = [
    "education", "experience", "projects", "skills",
    "certifications", "internship", "achievements", "summary",
]


def extract_text(filename: str, file_bytes: bytes) -> str:
    """Extracts raw text from a PDF, DOCX, or plain-text resume."""
    lower = filename.lower()
    if lower.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if lower.endswith(".docx"):
        document = docx.Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in document.paragraphs)
    if lower.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    raise ValueError("Unsupported file type. Upload a PDF, DOCX, or TXT resume.")


def extract_skills(text: str) -> List[str]:
    lower_text = text.lower()
    found = []
    for skill, patterns in SKILL_KEYWORDS.items():
        if any(pattern in lower_text for pattern in patterns):
            found.append(skill)
    return found


def _found_sections(text: str) -> List[str]:
    lower_text = text.lower()
    return [s for s in SECTION_HEADERS if s in lower_text]


def analyze_resume(text: str) -> Dict:
    """Heuristic ATS-style analysis: not a real applicant-tracking-system
    clone, but a transparent proxy score based on structure and content
    signals recruiters commonly screen for."""
    words = text.split()
    word_count = len(words)
    email_match = EMAIL_RE.search(text)
    phone_match = PHONE_RE.search(text)
    sections = _found_sections(text)
    skills = extract_skills(text)

    score = 0
    suggestions = []

    if email_match:
        score += 10
    else:
        suggestions.append("Add a contactable email address near the top of your resume.")

    if phone_match:
        score += 10
    else:
        suggestions.append("Add a phone number so recruiters can reach you directly.")

    section_score = min(len(sections) / len(SECTION_HEADERS), 1.0) * 30
    score += section_score
    missing_sections = [s for s in ("education", "experience", "projects", "skills") if s not in sections]
    if missing_sections:
        suggestions.append(f"Add a clear {', '.join(missing_sections)} section — ATS systems look for these headers.")

    skill_score = min(len(skills) / 8, 1.0) * 30
    score += skill_score
    if len(skills) < 5:
        suggestions.append("List more concrete technical skills — aim for at least 5-8 relevant keywords.")

    if 300 <= word_count <= 900:
        score += 20
    elif word_count < 300:
        suggestions.append("Your resume looks thin — expand on projects and impact with specific numbers.")
        score += 8
    else:
        suggestions.append("Your resume is long — tighten it to the most relevant 1-2 pages.")
        score += 12

    return {
        "ats_score": round(min(score, 100), 1),
        "word_count": word_count,
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "sections_found": sections,
        "skills": skills,
        "suggestions": suggestions[:5],
    }
