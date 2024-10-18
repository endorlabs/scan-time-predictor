import os
import git
import shutil
import requests
import json
import pygount
import subprocess
import src.build as build
import src.utils.file_helper as filehandler
from datetime import datetime
import find_repo
from timeout_decorator import timeout
import src.utils.logging_config as log
log = log.getLogger()

current_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
CLONE_DIR="/tmp"

def clone_and_validate_build(language,number_of_repos,build_tools,CSV_FILE,number_of_pages,FAIL_CSV_FILE):
    CLONE_PATH = os.path.join(CLONE_DIR,language,current_date_time)
    repo_dirs = []
    CUR_DIR = os.getcwd()
    for page in range(1,number_of_pages+1):
        GITHUB_API="https://api.github.com/search/repositories?q=language:"+language+"&sort=updated&per_page="+str(number_of_repos)+"&p="+str(page)
        log.info("getting "+language+"  "+str(number_of_repos)+ " repos from: "+GITHUB_API)
        # Send the GET request
        response = requests.get(GITHUB_API)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            resp_data = response.json()
            log.debug(f"total items {resp_data['total_count']}")
            log.info(f"Results are saving into {CSV_FILE} file")
            for item in resp_data["items"]:
                repoDetails = []
                row = []
                git_url = item["html_url"]
                #git_url = "https://github.com/williamfiset/Algorithms"
                os.chdir(CUR_DIR)
                if (filehandler.check_duplicate_data(git_url,CSV_FILE)):
                    continue
                if (filehandler.check_duplicate_data(git_url,FAIL_CSV_FILE)):
                    continue
                curl_cmd = "curl -LI " + git_url + " -o /dev/null -w '%{http_code}\n' -s"
                output,err = subprocess.Popen(curl_cmd, stdout=subprocess.PIPE,shell=True,text=True).communicate() 
                if int(output) != 200:
                    log.error("Repo does not exists or failed access  = {}".format(git_url))
                    continue
                repo_name = git_url.split("/")[-1]
                repo_path = os.path.join(CLONE_PATH,repo_name)
                local_repo,git_reference = clone_repo(git_url, repo_path)
                if local_repo == "" or git_reference == "" :
                    continue
                log.info(f"{local_repo.working_dir} copied successfully")
                pm,build_status,exception_msg = build.determine_build_manager(repo_path,build_tools)
                row.append(language)
                row.append(git_url)
                row.append(git_reference)
                row.append(pm)
                row.append(build_status)
                os.chdir(CUR_DIR)
                if pm and build_status == "pass":
                    linesofCode,totalFiles = get_lines_of_code_and_file_count(repo_path,language)
                    row.append(linesofCode)
                    row.append(totalFiles)
                    repoDetails.append(row)
                    if linesofCode != 0 and totalFiles != 0:
                        filehandler.write_data(repoDetails,CSV_FILE)
                    else:
                        exception_msg = "Failed to calculate lines of code for " + language
                        row.append(exception_msg)  
                        repoDetails.append(row)  
                        filehandler.write_data(repoDetails,FAIL_CSV_FILE)
                elif pm and build_status == "fail":
                    row.append(exception_msg)
                    repoDetails.append(row)
                    filehandler.write_data(repoDetails,FAIL_CSV_FILE)  
                cmd = "rm -rf " + repo_path 
                log.info("Removing cloned repo: {}".format(repo_path))
                try:
                    output = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True,text=True).communicate() 
                except Exception as e:
                    log.error ("ERROR: Found following exception ",e)                       
        else:
            log.error(f"Failed to retrieve Github data. Status code: {response.status_code}")

def clone_repo( repo_url, directory,git_refs=None):
    repo,git_reference = ("","")
    try:
        shutil.rmtree(directory, ignore_errors=True)
        repo,git_reference = clone_repo_with_timeout(repo_url, directory, git_refs)
        return repo,git_reference
    except Exception as e:
        log.error(f"Failed to clone repo: {e}")
        return repo,git_reference
    
@timeout(900)    
def clone_repo_with_timeout(repo_url, directory, git_refs):
    repo = git.Repo.clone_from(repo_url, directory)
    git_reference = repo.head.commit
    if git_refs:
        repo.git.checkout(git_refs)
        log.info(f"Switched to branch: {git_refs}")
    log.info(f"Repository cloned to {directory} and git ref is : {git_reference}")
    return repo,git_reference

def get_lines_of_code_and_file_count(repo_path,language):
    try:
        # Commented due to json error with pygount module
        # output = subprocess.Popen('pygount --format=json '+ repo_path, stdout=subprocess.PIPE,shell=True,text=True).communicate() 
        # data = json.loads(output[0])
        # for lang in data['languages']:
        #     if lang['language'] == language.capitalize():
        #         return lang['fileCount'],lang['sourceCount']
        # return 0,0    
        language_map = {'java':'Java','javascript':'JavaScript','go':'Go','python':'Python','ruby':'Ruby','php':'PHP','scala':'Scala'}
        output = subprocess.Popen('cloc --json '+ repo_path, stdout=subprocess.PIPE, shell=True,text=True).communicate() 
        data = json.loads(output[0])
        return data[language_map[language]]['nFiles'],data[language_map[language]]['code']
    except Exception as e:
        log.error(f"Failed perform code analysis: {e}")
        return 0,0
