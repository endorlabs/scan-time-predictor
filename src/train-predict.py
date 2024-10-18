import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
import numpy as np


def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Scan script for training or predicting.')

    # Add command-line arguments
    parser.add_argument('--mode', choices=['train', 'predict'], help='Mode of operation (e.g., train or predict)')

    # Common options for both train and predict modes
    parser.add_argument('--language', help='Language for prediction or training')
    parser.add_argument('--build_tool', help='Build tool for prediction or training')

    # Options specific to training mode
    parser.add_argument('--dataset_path', help='Path to the training dataset (required for train mode)')

    # Options specific to prediction mode
    #parser.add_argument('--file_count', type=int, help='Number of files for prediction')
    parser.add_argument('--lines_of_code', type=int, help='Lines of code for prediction')
    parser.add_argument('--package_count', type=int, help='Number of packages for prediction')
    parser.add_argument('--dependency_count', type=int, help='Number of dependencies for prediction')
    parser.add_argument('--no_of_cpu_cores', type=int, help='Number of CPU cores for prediction')
    parser.add_argument('--memory', type=int, help='Amount of memory for prediction')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check if required arguments are provided based on the mode
    if args.mode is None:
        parser.error("--mode is required.")

    if args.mode == 'train':
        # Check required options for train mode
        if args.language is None or args.build_tool is None or args.dataset_path is None:
            parser.error("--language, --build_tool, and --dataset_path are required in train mode.")
    elif args.mode == 'predict':
        # Check required options for predict mode
        # if args.language is None or args.build_tool is None or args.file_count is None or args.lines_of_code is None \
        #         or args.package_count is None or args.dependency_count is None or args.no_of_cpu_cores is None \
        #         or args.memory is None:
            #parser.error("--language, --build_tool, --file_count, --lines_of_code, --package_count, --dependency_count, --no_of_cpu_cores , --memory are required in predict mode.")
            if args.language is None or args.build_tool is None or args.lines_of_code is None \
            or args.package_count is None or args.dependency_count is None or args.no_of_cpu_cores is None \
            or args.memory is None:
                parser.error("--language, --build_tool, --lines_of_code, --package_count, --dependency_count, --no_of_cpu_cores , --memory are required in predict mode.")

    # Your program logic here using the provided arguments
    print("Mode:", args.mode)
    print("Language:", args.language)
    print("Build Tool:", args.build_tool)

    if args.mode == 'train':
        print("Dataset Path:", args.dataset_path)
        print("Language:", args.language)
        print("Build Tool:", args.build_tool)
        train_predict(load_data(args.dataset_path,args.language,args.build_tool),args.language,args.build_tool)

    if args.mode == 'predict':
        #print("File Count:", args.file_count)
        print("Lines of Code:", args.lines_of_code)
        print("Package Count:", args.package_count)
        print("Dependency Count:", args.dependency_count)
        print("Number of CPU Cores:", args.no_of_cpu_cores)
        print("Memory:", args.memory)
        #predict(args.language,args.build_tool,args.file_count,args.lines_of_code,args.package_count,args.dependency_count,args.no_of_cpu_cores,args.memory)
        predict(args.language,args.build_tool,args.lines_of_code,args.package_count,args.dependency_count,args.no_of_cpu_cores,args.memory)


def load_data(dataset_path,language,build_tool):
    file_path= dataset_path+"/data_"+language+"_"+build_tool+"_scan_result.csv"
    return pd.read_csv(file_path)

def train_predict(df,language,build_tool):
    # Extract features and target variables
    X = df.drop(['Language', 'GitURL','GitRef','BuildTool','FileCount','BuildStatus','QuickScanDuration', 'FullScanDuration'], axis=1)
    y_quick = df['QuickScanDuration']
    y_full = df['FullScanDuration']

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
    joblib.dump(quick_scan_model, 'quick_scan_model'+'_'+language+'_'+build_tool+'.pkl')
    joblib.dump(full_scan_model, 'full_scan_model'+'_'+language+'_'+build_tool+'.pkl')

#def predict(language,build_tool,file_count,lines_of_code,package_count,dependency_count,no_of_cpu_cores,memory):
def predict(language,build_tool,lines_of_code,package_count,dependency_count,no_of_cpu_cores,memory):
    try:
        # Valid combinations of language and build_tool
        valid_combinations = {
            'java': ['maven', 'gradle'],
            'python': ['pip']
        }
    
        if language.lower() in valid_combinations and build_tool.lower() not in valid_combinations[language.lower()]:
            raise ValueError(f"The combination of language '{language}' and build_tool '{build_tool}' is not correct.")
    


        # Load the trained models for prediction
        loaded_quick_scan_model = joblib.load('quick_scan_model'+'_'+language+'_'+build_tool+'.pkl')
        loaded_full_scan_model = joblib.load('full_scan_model'+'_'+language+'_'+build_tool+'.pkl')

        # Example input data for prediction
        input_data = {
        # 'FileCount': [file_count],
            'LinesofCode': [lines_of_code],
            'PackageCount': [package_count],
            'DependencyCount': [dependency_count],
            'TotalCPUCores': [no_of_cpu_cores],
            'TotalMemory': [memory]
        }

        # Convert the input data to a DataFrame
        input_df = pd.DataFrame(input_data)

        # Make predictions using the loaded models
        quick_scan_prediction = loaded_quick_scan_model.predict(input_df)
        full_scan_prediction = loaded_full_scan_model.predict(input_df)

        # Display the predictions
        print(f"\nPredicted Quick Scan Duration: {quick_scan_prediction[0]} seconds")
        print(f"Predicted Full Scan Duration: {full_scan_prediction[0]} seconds")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
