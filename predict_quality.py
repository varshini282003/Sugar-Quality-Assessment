import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
import joblib

# Load dataset
df = pd.read_csv('sugar_quality_dataset.csv')

# Split features and target
X = df.drop('Quality', axis=1)
y = df['Quality']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models
models = {
    'LinearRegression': LinearRegression(),
    'DecisionTree': DecisionTreeRegressor(random_state=42),
    'RandomForest': RandomForestRegressor(random_state=42),
    'SVR': SVR(kernel='linear')
}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    joblib.dump(model, f'{name.lower()}_model.pkl')

joblib.dump(scaler, 'scaler.pkl')

print("Models trained and saved successfully.")



def predict_quality(model_name, input_features):
    try:

        model = joblib.load(f'{model_name.lower()}_model.pkl')
        scaler = joblib.load('scaler.pkl')


        for value in input_features:
            if not isinstance(value, (int, float)):
                raise ValueError("Please enter valid numeric values for all fields.")

        # Prepare features
        features_df = pd.DataFrame([input_features], columns=X.columns)
        features_scaled = scaler.transform(features_df)

        # Make prediction
        quality = model.predict(features_scaled)[0]

        return quality

    except ValueError as ve:
        return str(ve)
    except Exception as e:
        return str(e)


if __name__ == "__main__":

    example_features = [5.5, 6.7, 2.3, 8.9, 3.4, 250.0, 75.0, 5.0, 80.0, 1.5, 7.2, 85.0]
    model_name = 'RandomForest'
    # Predict quality
    predicted_quality = predict_quality(model_name, example_features)
    print(f"Predicted quality: {predicted_quality:.2f}")
