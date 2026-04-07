from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import joblib
import numpy as np

# create api app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# load model and scaler
model = joblib.load("../ML/artifacts/xgb_model.pkl")
scaler = joblib.load("../ML/artifacts/scaler.pkl")

# map numeric predictions to letter grades
GRADE_MAP = {4: "A", 3: "B", 2: "C", 1: "D", 0: "F"}

# define request model
class PredictRequest(BaseModel):
    attendance: Optional[float] = None
    midterm_score: Optional[float] = None
    assignments_avg: Optional[float] = None
    quizzes_avg: Optional[float] = None
    participation_score: Optional[float] = None
    projects_score: Optional[float] = None
    study_hours_per_week: float
    has_extracurriculars: bool
    stress_level: int
    sleep_hours_per_night: float

# define prediction endpoint
@app.post("/predict")
def predict(req: PredictRequest):
    # if any of the score fields are missing, use the average of the provided ones
    score_fields = [req.attendance, req.midterm_score, req.assignments_avg,
                    req.quizzes_avg, req.participation_score, req.projects_score]
    provided = [v for v in score_fields if v is not None]
    fallback = sum(provided) / len(provided) if provided else 75.0

    def val(v):
        return v if v is not None else fallback

    features = np.array([[
        val(req.attendance),
        val(req.midterm_score),
        val(req.assignments_avg),
        val(req.quizzes_avg),
        val(req.participation_score),
        val(req.projects_score),
        req.study_hours_per_week,
        1 if req.has_extracurriculars else 0,
        req.stress_level,
        req.sleep_hours_per_night,
    ]])
    scaled = scaler.transform(features)
    prediction = int(model.predict(scaled)[0])
    return {"grade": GRADE_MAP[prediction]}
