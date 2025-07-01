import numpy as np
import tensorflow as tf
import joblib  # Для загрузки scaler

# Загружаем обученную модель
model = tf.keras.models.load_model("../old_models/pipeline_replacement_modelv1.keras")

# Загружаем сохраненный StandardScaler
scaler = joblib.load("scaler.pkl")

# Кодировки категориальных признаков
installation_type_mapping = {
    "in_channel": 0,
    "underground": 1,
    "above_ground": 2
}

insulation_material_mapping = {
    "mineral_wool": 0,
    "polyurethane_foam": 1,
    "foam_glass": 2
}

# Функция для предсказания
def predict_pipeline_replacement(length, diameter, installation_type, insulation_material, year_of_operation):
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
    result = "Замена требуется" if prediction > 0.5 else "Замена не требуется"
    return result

# Пример предсказания
length = 100  # Длина трубы, м
diameter = 150  # Диаметр трубы, мм
installation_type = "in_channel"  # Тип прокладки (in_channel, underground, above_ground)
insulation_material = "polyurethane_foam"  # Материал теплоизоляции (mineral_wool, polyurethane_foam, foam_glass)
year_of_operation = 2000  # Год ввода в эксплуатацию

result = predict_pipeline_replacement(length, diameter, installation_type, insulation_material, year_of_operation)
print(f"Результат предсказания: {result}")
