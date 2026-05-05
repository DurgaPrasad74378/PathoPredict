# 🏥 Disease Prediction System (Symptom2Diagnosis)

## 🚀 Project Overview
This project is an end-to-end Machine Learning web application that predicts probable diseases based on patient-reported symptoms. By mapping qualitative symptom descriptions to numerical severity weights, the system utilizes a **Random Forest Classifier** to provide real-time, highly accurate diagnostic predictions. 

It is designed to bridge the gap between symptom onset and initial diagnosis, acting as an automated triage tool.

## ✨ Key Features
* **Machine Learning Engine:** Compares a baseline Decision Tree with an optimized Random Forest model to prevent overfitting and ensure high accuracy.
* **Custom Preprocessing Pipeline:** Robust data cleaning that handles dataset inconsistencies (e.g., standardizing typographic errors like spaces vs. underscores).
* **Stateful Web Interface:** A modern, responsive Flask-powered frontend that dynamically remembers user selections after form submission.
* **Real-Time Inference:** Uses a serialized model (`.pkl`) for instant predictions without the overhead of retraining.

## 📂 Project Structure
```text
disease-prediction-system/
├── app/                   # Web Application
│   ├── static/            # CSS and UI assets
│   │   └── css/           
│   │       └── style.css  
│   ├── templates/         # HTML Jinja2 templates
│   │   └── index.html     
│   └── app.py             # Flask server & API routing
├── data/                  # Healthcare datasets
│   ├── dataset.csv        
│   └── Symptom-severity.csv
├── models/                # Serialized trained models
│   └── random_forest_model.pkl
├── src/                   # Core ML pipeline
│   ├── preprocess.py      # Data cleaning and feature mapping
│   ├── train.py           # Model training and evaluation
│   └── predict.py         # Inference logic
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation


🛠️ Technology Stack

Backend: Python, Flask

Machine Learning: Scikit-Learn, Pandas, NumPy

Frontend: HTML5, CSS3

📸 Screenshots

