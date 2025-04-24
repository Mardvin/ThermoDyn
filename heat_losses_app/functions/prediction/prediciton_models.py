import os

import numpy as np
import tensorflow as tf
import joblib  # Для загрузки scaler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Получаем путь к текущему файлу
MODEL_PATH = os.path.join(BASE_DIR, "pipeline_replacement_modelv1.keras")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

# Загружаем обученную модель
model = tf.keras.models.load_model(MODEL_PATH)

# Загружаем сохраненный StandardScaler
scaler = joblib.load(SCALER_PATH)

# Кодировки категориальных признаков
installation_type_mapping = {
    "В канале": 0,
    "Подземная прокладка": 1,
    "Наземная прокладка": 2
}

insulation_material_mapping = {
    "Минеральная вата": 0,
    "Пенополиуретан": 1,
    "Пеностекло": 2
}

# Функция для предсказания
def predict_pipeline_replacement(length: float, diameter: int, installation_type: str, insulation_material: str,
                                 year_of_operation: int) -> str:
    # Кодируем категориальные переменные
    installation_type_encoded = installation_type_mapping.get(installation_type, -1)
    insulation_material_encoded = insulation_material_mapping.get(insulation_material, -1)

    if installation_type_encoded == -1 or insulation_material_encoded == -1:
        raise ValueError("Ошибка: Некорректный тип прокладки или материала изоляции!")

    # Создаем массив с входными данными
    input_data = np.array([[length, diameter, installation_type_encoded, insulation_material_encoded, year_of_operation]])

    # Применяем тот же StandardScaler, который использовался при обучении
    input_data = scaler.transform(input_data)

    # Делаем предсказание
    prediction = model.predict(input_data)[0][0]

    # Интерпретируем результат
    result = "Да" if prediction > 0.5 else "Нет"
    return result
