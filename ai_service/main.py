from fastapi import FastAPI
from pydantic import BaseModel
from ml_utils import predict_threat, calculate_risk, get_escalation_status

app = FastAPI()

class ThreatRequest(BaseModel):
    description: str

@app.post("/predict")
def predict(request: ThreatRequest):
    prediction, probability = predict_threat(request.description)
    risk_score = calculate_risk(prediction, probability)
    status = get_escalation_status(risk_score)

    return {
        "threat_type": prediction,
        "confidence": probability,
        "risk_score": risk_score,
        "status": status
    }