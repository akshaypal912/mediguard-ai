"""
MediGuard AI - Starter training script for patient risk prediction.
Replace sample data with a real triage dataset before using in production.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# ---- 1. Load data ----
# TODO: replace with real dataset path, e.g. "../data/patients.csv"
df = pd.read_csv("../data/sample_patients.csv")

# ---- 2. Features & target ----
FEATURES = ["age", "heart_rate", "spo2", "systolic_bp", "respiratory_rate"]
TARGET = "risk_level"  # 0 = Stable, 1 = Urgent, 2 = Critical

X = df[FEATURES]
y = df[TARGET]

# ---- 3. Train/test split ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---- 4. Train model ----
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# ---- 5. Evaluate ----
preds = model.predict(X_test)
print(classification_report(y_test, preds))

# ---- 6. Save model ----
joblib.dump(model, "risk_model.pkl")
print("Model saved to risk_model.pkl")
