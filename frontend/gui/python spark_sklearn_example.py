# spark_sklearn_example.py

from pyspark.sql import SparkSession
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

# ----------------------------
# 🔥 Crear sesión de Spark
# ----------------------------
spark = SparkSession.builder \
    .appName("Spark + scikit-learn Example") \
    .master("local[*]") \
    .getOrCreate()

print("✅ Spark iniciado correctamente")
print("Versión de Spark:", spark.version)

# ----------------------------
# 📊 Crear un pequeño DataFrame en Spark
# ----------------------------
data = [
    (1, 5.1, 3.5, 1.4, 0.2, "setosa"),
    (2, 4.9, 3.0, 1.4, 0.2, "setosa"),
    (3, 6.2, 3.4, 5.4, 2.3, "virginica"),
    (4, 5.9, 3.0, 5.1, 1.8, "virginica"),
    (5, 6.0, 2.2, 4.0, 1.0, "versicolor"),
    (6, 5.6, 2.9, 3.6, 1.3, "versicolor"),
]

columns = ["id", "sepal_length", "sepal_width", "petal_length", "petal_width", "species"]

df_spark = spark.createDataFrame(data, columns)
df_spark.show()

# ----------------------------
# 🔄 Convertir Spark DataFrame a pandas
# ----------------------------
df = df_spark.toPandas()

# Codificar etiquetas de texto (setosa, versicolor, virginica)
df["label"] = df["species"].astype("category").cat.codes

# Separar variables
X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
y = df["label"]

# ----------------------------
# ✂️ Dividir en entrenamiento y prueba
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ----------------------------
# 🌲 Entrenar modelo con scikit-learn
# ----------------------------
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# ----------------------------
# 📈 Evaluar modelo
# ----------------------------
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("\n✅ Precisión del modelo:", round(acc * 100, 2), "%")

# ----------------------------
# 🔍 Mostrar predicciones
# ----------------------------
results = pd.DataFrame({"Real": y_test.values, "Predicho": y_pred})
print("\nResultados:")
print(results)

# ----------------------------
# 🧹 Detener Spark
# ----------------------------
spark.stop()
