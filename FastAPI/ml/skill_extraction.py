import spacy

nlp = spacy.load("en_core_web_sm")

known_skills = ["Python", "Java", "SQL", "Project Management", "Data Analysis", "FastAPI", "mySQL", "NoSQL"]

def extract_skills(text):
    doc = nlp(text)
    extracted_skills = [token.text for token in doc if token.text in known_skills]
    return extracted_skills
