# QA Benchmarking Repo

Read RFC [here](https://endorlabs.atlassian.net/l/cp/oUPgPJCA)

## Steps to run 

- `source myenv/bin/activate`

To list down the buildable repos:
-   `python3 find_repo.py -l java -b maven -r 5` or `python3 find_Repo.py -language python -build_tools poetry  -number_of_repos 5`

    Where, 

       -l, -language (strings) : Set programming language to search repo (java|python). 

       -b, -build_tool: build tool to verify the build status (maven|gradle|pip|poetry). 

       -r, -number_of_repos (int): Set the number of repos to search.

This wil store the result in .csv file under data/ directory. File name will be like data_<language>_<build-toll>.csv. The CSV file will be further used during endotctl scan.

To run the endorctl scan on the listed buildable repos:
-   `python3 endor_scan.py --repo_list data/data_java_maven.csv` or `python3 endor_scan.py -r data/data_java_maven.csv`

    Where, 

     -r, -repo_list (string): Input CSV file which contains list of buildable repos. 


To generate model files to for scan duration prediction for a language/build_tool combination:
    Note: Run below command from root of the project.
-   `python3 src/train-predict.py --mode=train --language=python --build_tool=pip --dataset_path=data`

    Where, 

     --mode (string): Mode of operation (e.g., train or predict). 

     --language (string): language for which models needs to be generated.

     --build_tool (string): Build tool of a language for which models needs to be generated.

     --dataset_path (string) : Path (folder) where the scan result csv file for a lanuage/build_tool combination is present. The file name needs to be of `data_<language>_<build_tool>_scan_result.csv` format , example: `data_java_maven_scan_result.csv` 

    output: 
      This command will generate two .pkl files for a language/build_tool combination, example `full_scan_model_python_pip.pkl` and `quick_scan_model_python_pip.pkl`

To predict quick scan and full scan duration for a language/build_tool combination :
     Note: Run below command from root of the project.
-   `python3  src/train-predict.py --mode=predict --language=java --build_tool=gradle --lines_of_code=200000 --package_count=10 --dependency_count=150 --no_of_cpu_cores=16 --memory=62`

    Where, 

     --mode (string): Mode of operation (e.g., train or predict). 

     --language (string): language for which models needs to be generated.

     --build_tool (string): Build tool of a language for which models needs to be generated.

     --lines_of_code (int): Number of lines of code.

     --package_count (int): Approx number of packages present in the repo.

     --dependency_count (int): Approx number of dependencies present in the repo.

     --no_of_cpu_cores (int): Number of CPUs on which the endorctl scan would be run.

     --memory (int): System Memory in GB on which the endorctl scan would be run.

    output:

      This command will generate below predictions:

        Predicted Quick Scan Duration: 131.85 seconds

        Predicted Full Scan Duration: 433.44 seconds
