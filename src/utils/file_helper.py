import csv
import src.utils.logging_config as log
log = log.getLogger()
def write_data(data,csv_file):
    try:
        with open(csv_file, 'a', newline='') as csvfile: 
            csv_writer = csv.writer(csvfile)

            # Append each row of data to the existing CSV file
            for row in data:
                csv_writer.writerow(row)
            log.info("Data has been appended to {}".format(csv_file))
    except Exception as e:
        log.error(f"Failed to open file: {e}")

def check_duplicate_data(git_url,csv_file):
    log.info("Checking duplicate for url:{} on file: {}".format(git_url,csv_file))
    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader) 
            for row in csv_reader:
                if git_url in row[1]:
                    log.info("The {} repo is already present in CSV {}".format(row[1],csv_file))
                    return True
            return False  
    except Exception as e:
        log.error(f"Failed to open file: {e}")
        return False          
