import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib

def load_data(filename):
    return pd.read_csv(filename)

def train_predict(df):
    # Split data into features and targets
    X = df.drop(['language', 'Quick_scan', 'Full_scan'], axis=1)
    y_quick = df['Quick_scan']
    y_full = df['Full_scan']

    # Split data into training and testing set
    X_train, X_test, y_quick_train, y_quick_test = train_test_split(X, y_quick, test_size=0.2, random_state=42)
    _, _, y_full_train, y_full_test = train_test_split(X, y_full, test_size=0.2, random_state=42)

    # Train Quick Scan model
    quick_scan_model = LinearRegression()
    quick_scan_model.fit(X_train, y_quick_train)
    y_quick_pred = quick_scan_model.predict(X_test)
    rmse_quick = mean_squared_error(y_quick_test, y_quick_pred, squared=False)
    print(f'RMSE for Quick Scan: {rmse_quick}')
    print(f'Quick Scan: {y_quick_pred}')
    # Save the Quick Scan model
    joblib.dump(quick_scan_model, 'quick_scan_model.pkl')
    print(f"Quick Scan Model Coefficients: {quick_scan_model.coef_}")
    print(f"Quick Scan Model Intercept: {quick_scan_model.intercept_}")

    # Train Full Scan model
    full_scan_model = LinearRegression()
    full_scan_model.fit(X_train, y_full_train)
    y_full_pred = full_scan_model.predict(X_test)
    rmse_full = mean_squared_error(y_full_test, y_full_pred, squared=False)
    print(f'RMSE for Full Scan: {rmse_full}')
    print(f'Full Scan: {y_full_pred}')
    # Save the Full Scan model
    joblib.dump(full_scan_model, 'full_scan_model.pkl')
    print(f"Full Scan Model Coefficients: {full_scan_model.coef_}")
    print(f"Full Scan Model Intercept: {full_scan_model.intercept_}")

def predict(input_data):
    # Load trained models
    loaded_quick_scan_model = joblib.load('quick_scan_model.pkl')
    loaded_full_scan_model = joblib.load('full_scan_model.pkl')

    # Convert the input data to a DataFrame
    input_df = pd.DataFrame([input_data])

    # Make predictions using the loaded models
    quick_scan_prediction = loaded_quick_scan_model.predict(input_df)
    full_scan_prediction = loaded_full_scan_model.predict(input_df)

    return quick_scan_prediction[0], full_scan_prediction[0]


if __name__ == "__main__":
    df = load_data("data/dataset.csv")
    train_predict(df)


    input_data = {
    'File_count': 400,
    'Lines_of_code': 400000,
    'Package_count': 20,
    'Dependency_count': 200,
    'CPU': 4,
    'Memory': 16
    }

    predicted_quick_scan, predicted_full_scan = predict(input_data)

    print(f"Predicted Quick Scan Duration: {predicted_quick_scan} seconds")
    print(f"Predicted Full Scan Duration: {predicted_full_scan} seconds")
    


    
