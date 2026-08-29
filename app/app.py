from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import sys
import os
import logging
import traceback

# --- BULLETPROOF PATHS ---
# This finds project folder automatically
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from src.predict import predict_disease

# Initialize FastAPI
app = FastAPI(title="Disease Prediction API")

# Mount Static Files (CSS)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "app", "static")), name="static")

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, "app.log")),
        logging.StreamHandler(sys.stdout)
    ]
)

# Safely locate the CSV file and wrap in try/except
try:
    csv_path = os.path.join(BASE_DIR, 'data', 'Symptom-severity.csv')
    severity_df = pd.read_csv(csv_path)
    symptoms_list = severity_df['Symptom'].str.strip().tolist()
    severity_dict = dict(zip(severity_df['Symptom'].str.strip(), severity_df['weight']))
    logging.info("Successfully loaded symptom data.")
except Exception as e:
    logging.critical(f"Failed to load symptom data: {e}")
    sys.exit(1)

# ==========================================
# 🛡️ PYDANTIC DATA VALIDATION
# ==========================================
class SymptomsPayload(BaseModel):
    symptoms: list[str]

# ==========================================
# 🌐 STATIC FRONTEND (No Jinja!)
# ==========================================
@app.get('/', response_class=FileResponse)
async def home():
    """Serves the pure static HTML file directly."""
    html_path = os.path.join(BASE_DIR, "app", "templates", "index.html")
    return FileResponse(html_path)

# ==========================================
# 🚀 JSON API ENDPOINTS
# ==========================================

@app.get('/api/v1/symptoms')
async def get_symptoms():
    """Returns the list of valid symptoms for the frontend dropdowns."""
    return {"symptoms": symptoms_list}

@app.post('/api/v1/predict')
async def api_predict(payload: SymptomsPayload):
    """
    FastAPI automatically validates that the request JSON 
    matches the SymptomsPayload structure!
    """
    try:
        selected_symptoms = payload.symptoms
        
        if len(selected_symptoms) == 0:
            raise HTTPException(status_code=400, detail="Symptoms must be a non-empty array.")

        symptom_weights = []
        for sym in selected_symptoms:
            if sym in severity_dict:
                symptom_weights.append(severity_dict[sym])
            else:
                logging.warning(f"API Warning: Unknown symptom received: {sym}")

        model_file = os.path.join(BASE_DIR, 'models', 'random_forest_model.pkl')
        prediction = predict_disease(symptom_weights, model_path=model_file)
        
        logging.info(f"API Prediction successful: {prediction}")

        # FastAPI automatically converts dictionaries to JSON responses
        return {
            "status": "success",
            "prediction": prediction,
            "symptoms_analyzed_count": len(symptom_weights)
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"API Error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An internal server error occurred")

if __name__ == '__main__':
    import uvicorn
    # In FastAPI, we use Uvicorn as the ASGI server
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)