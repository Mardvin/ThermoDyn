import joblib
import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Загружаем датасет
file_path = "pipeline_replacement_extra_2000.csv"
df = pd.read_csv(file_path)

# Кодируем категориальные признаки
label_encoders = {}

for col in ["installation_type", "insulation_material"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Кодируем целевую переменную (да/нет -> 1/0)
df["pipeline_replacement"] = df["pipeline_replacement"].map({"yes": 1, "no": 0})

# Выбираем признаки (X) и целевую переменную (y)
X = df.drop(columns=["pipeline_replacement"])  # Исключаем ID и целевую переменную
y = df["pipeline_replacement"]

# Разделяем данные на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Нормализация числовых данных
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
joblib.dump(scaler, "scaler.pkl")
X_test = scaler.transform(X_test)

# Создаем модель нейросети
model = keras.Sequential([
    keras.layers.Dense(128, activation="relu", input_shape=(X_train.shape[1],)),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(1, activation="sigmoid")
])

# Компилируем модель
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Обучаем модель
model.fit(X_train, y_train, epochs=150, batch_size=16, validation_data=(X_test, y_test))

# Оцениваем качество модели
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_acc:.4f}")
model.save("ready_models/pipeline_replacement_modelv1.keras")