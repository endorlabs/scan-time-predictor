import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
import numpy as np

# Read data from CSV
df = pd.read_csv('data/dataset.csv')

# Extract features and target variables
X = df.drop(['language', 'Quick_scan', 'Full_scan'], axis=1)
y_quick = df['Quick_scan']
y_full = df['Full_scan']

# Split the data into training and testing sets
X_train, X_test, y_quick_train, y_quick_test, y_full_train, y_full_test = train_test_split(
    X, y_quick, y_full, test_size=0.2, random_state=42)

# Train Random Forest models for Quick Scan and Full Scan
quick_scan_model = RandomForestRegressor(random_state=42).fit(X_train, y_quick_train)
full_scan_model = RandomForestRegressor(random_state=42).fit(X_train, y_full_train)

# Evaluate models
print("Quick Scan RMSE:", np.sqrt(mean_squared_error(y_quick_test, quick_scan_model.predict(X_test))))
print("Full Scan RMSE:", np.sqrt(mean_squared_error(y_full_test, full_scan_model.predict(X_test))))

# Save the trained models
joblib.dump(quick_scan_model, 'quick_scan_model.pkl')
joblib.dump(full_scan_model, 'full_scan_model.pkl')

# Load the trained models for prediction
loaded_quick_scan_model = joblib.load('quick_scan_model.pkl')
loaded_full_scan_model = joblib.load('full_scan_model.pkl')

# Example input data for prediction
input_data = {
    'File_count': [400],
    'Lines_of_code': [400000],
    'Package_count': [20],
    'Dependency_count': [200],
    'CPU': [4],
    'Memory': [16]
}

# Convert the input data to a DataFrame
input_df = pd.DataFrame(input_data)

# Make predictions using the loaded models
quick_scan_prediction = loaded_quick_scan_model.predict(input_df)
full_scan_prediction = loaded_full_scan_model.predict(input_df)

# Display the predictions
print(f"\nPredicted Quick Scan Duration: {quick_scan_prediction[0]} seconds")
print(f"Predicted Full Scan Duration: {full_scan_prediction[0]} seconds")
