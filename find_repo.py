import argparse
import os
import src.validaterepo as validaterepo
import src.utils.file_helper as filehandler
import src.utils.logging_config as log
from datetime import datetime
from pymongo.mongo_client import MongoClient
log = log.getLogger()

def check_collection_exists(collection_name):
    return collection_name in db.list_collection_names()

def create_collection(collection_name):
    db.create_collection(collection_name)

def insert_data_into_collection(collection_name, data):
    db[collection_name].insert_one(data)


def get_args():
    parser = argparse.ArgumentParser(description="Enter language and build tool.")
    parser.add_argument("--language", "-l", type=str, help="language")
    parser.add_argument("--build_tool", "-b", type=str, help="build tool")
    parser.add_argument("--number_of_repos", "-r", type=int, help="Number of GitHub repos")
    args = parser.parse_args()
    pages = 1
    if args.number_of_repos < 101:
        pages = 1   
    else:
        pages = int(args.number_of_repos)//100
    return args.language.lower() , args.build_tool, args.number_of_repos, pages

def main():
    language, build_tool, number_of_repos, number_of_pages = get_args()
    log.info(f"Language: {language}")

    # Construct collection names
    collection_name = db[f"data_{language}_{build_tool}"]
    failed_collection_name = db[f"data_{language}_{build_tool}_failed_repos"]

    log.info(f"Results will be saved in MongoDB collection: {collection_name}")
    log.info(f"Failed repos details will be saved in MongoDB collection: {failed_collection_name}")

    # if not check_collection_exists(collection_name):
    #     log.info(f"Creating collection: {collection_name}")
    #     create_collection(collection_name)

    # if not check_collection_exists(failed_collection_name):
    #     log.info(f"Creating collection: {failed_collection_name}")
    #     create_collection(failed_collection_name)

    validaterepo.clone_and_validate_build(language, number_of_repos, build_tool, collection_name, number_of_pages, failed_collection_name)

    log.info(f"Results are written to MongoDB collection: {collection_name}")
    log.info(f"Failed repos details are written to MongoDB collection: {failed_collection_name}")

if __name__ == "__main__":
    url = os.getenv('SCP_MONGODB_URL')
    client = MongoClient(url)
    db = client['qa_benchmarking']
    main()