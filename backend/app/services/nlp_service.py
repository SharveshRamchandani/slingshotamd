import spacy
from dateutil import parser
import re
from datetime import datetime

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_deadline(text: str):
    """
    Extracts deadline from text using spaCy and simple heuristics.
    Returns parsed datetime string if found.
    """
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME"]:
            try:
                # Naive date parsing
                dt = parser.parse(ent.text, fuzzy=True)
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass
    
    # regex fallback for common patterns
    due_pattern = r"(due by|deadline is)\s+([A-Za-z0-9\s:]+)"
    match = re.search(due_pattern, text, re.IGNORECASE)
    if match:
        try:
            dt = parser.parse(match.group(2), fuzzy=True)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass
            
    return None

def extract_task_type(text: str) -> str:
    """Classifies task type"""
    text = text.lower()
    if "exam" in text or "midterm" in text or "final" in text:
        return "exam"
    if "quiz" in text:
        return "quiz"
    if "assignment" in text or "homework" in text:
        return "assignment"
    return "event"

def process_raw_message(text: str) -> dict:
    """Wrapper to process a message and return structured data"""
    # Naive title extraction: first sentence
    doc = nlp(text)
    title = ""
    if doc.sents:
        title = next(doc.sents).text.strip()
    
    if len(title) > 50:
        title = title[:47] + "..."

    deadline = extract_deadline(text)
    task_type = extract_task_type(text)

    return {
        "title": title,
        "type": task_type,
        "deadline": deadline
    }
