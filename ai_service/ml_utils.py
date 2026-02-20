import os
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb"))

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def get_escalation_status(risk_score):
    if risk_score >= 75:
        return "ESCALATED"
    elif risk_score >= 40:
        return "REVIEW"
    else:
        return "LOW"

def predict_threat(text):

    text_vectorized = vectorizer.transform([text])

    prediction = model.predict(text_vectorized)[0]

    probability = max(model.predict_proba(text_vectorized)[0])

    return prediction, probability


def calculate_risk(prediction, probability):
    severity = {
        "Phishing": 1.2,
        "Malware": 1.5,
        "Ransomware": 1.4,
        "DDoS": 1.3,
        "Safe": 0.2
    }


    risk_score = probability * severity.get(prediction, 0.5) * 100

    return round(risk_score, 2)