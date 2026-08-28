from flask import Flask, render_template, request, jsonify
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

app = Flask(__name__)

# --- LOGGING SETUP ---
# Logs will be saved to 'app.log' and also printed to the console
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
    sys.exit(1) # Stop the server if data is missing

@app.route('/')
def home():
    return render_template('index.html', symptoms=symptoms_list)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # 1. Save the exact dropdown choices
            user_choices = {
                1: request.form.get('symptom1', ''),
                2: request.form.get('symptom2', ''),
                3: request.form.get('symptom3', ''),
                4: request.form.get('symptom4', ''),
                5: request.form.get('symptom5', '')
            }
            
            # 2. Filter out empty selections
            selected_symptoms = [val for val in user_choices.values() if val != ""]
            
            # Input Validation: Did they select anything?
            if not selected_symptoms:
                logging.warning("User submitted form without selecting symptoms.")
                return render_template('index.html', 
                                       symptoms=symptoms_list, 
                                       prediction_text="Please select at least one symptom.",
                                       user_choices=user_choices)

            # 3. Process weights
            symptom_weights = []
            for sym in selected_symptoms:
                if sym in severity_dict:
                    symptom_weights.append(severity_dict[sym])
                else:
                    logging.warning(f"Unknown symptom received: {sym}")
                    # Skip or handle unknown symptom safely

            logging.info(f"Processing prediction for symptoms: {selected_symptoms}")

            model_file = os.path.join(BASE_DIR, 'models', 'random_forest_model.pkl')
            prediction = predict_disease(symptom_weights, model_path=model_file)
            
            logging.info(f"Prediction successful: {prediction}")

            # 4. Return to frontend
            return render_template('index.html', 
                                   symptoms=symptoms_list, 
                                   prediction_text=f'Most Likely Diagnosis: {prediction}',
                                   user_choices=user_choices)
                                   
        except Exception as e:
            # If ANYTHING fails, log the exact error and return a safe message to user
            error_msg = str(e)
            logging.error(f"Error during prediction: {error_msg}\n{traceback.format_exc()}")
            return render_template('index.html', 
                                   symptoms=symptoms_list, 
                                   prediction_text="An internal error occurred. Please try again.",
                                   user_choices=request.form)

if __name__ == '__main__':
    app.run(debug=True)