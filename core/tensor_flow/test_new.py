import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Загружаем модель и scaler
model = tf.keras.models.load_model("../ready_models/pipeline_replacement_modelv1.keras")
scaler = joblib.load("scaler.pkl")

df = pd.read_csv("../pipeline_replacement_dataset_en.csv")

# Перекодировка категориальных признаков
installation_type_mapping = {"in_channel": 0, "underground": 1, "above_ground": 2}
insulation_material_mapping = {"mineral_wool": 0, "polyurethane_foam": 1, "foam_glass": 2}

df['installation_type_encoded'] = df['installation_type'].map(installation_type_mapping)
df['insulation_material_encoded'] = df['insulation_material'].map(insulation_material_mapping)

# Перекодировка целевой переменной
df['target'] = df['pipeline_replacement'].map({'no': 0, 'yes': 1})

# Собираем X и y
X = df[['length_m', 'diameter_mm', 'installation_type_encoded', 'insulation_material_encoded',
        'year_of_operation']].values
y_true = df['target'].values

# Масштабируем
X_scaled = scaler.transform(X)

# Предсказываем
y_pred_proba = model.predict(X_scaled)
y_pred = (y_pred_proba > 0.5).astype(int).flatten()

# Оцениваем качество модели
print("Accuracy:", accuracy_score(y_true, y_pred))
print("\nОтчет:\n", classification_report(y_true, y_pred))
print("\nМатрица ошибок:\n", confusion_matrix(y_true, y_pred))