import subprocess
import os
import threading
import time
import json
import argparse
import csv
import sys
from kubernetes import client, config
import git
import psutil
import shutil
from timeout_decorator import timeout
from pymongo import MongoClient
import src.build as build
import src.utils.file_helper as filehandler
import src.utils.logging_config as log
from datetime import datetime
import math
log = log.getLogger()
current_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
CLONE_DIR="/tmp"

url = os.getenv('SCP_MONGODB_URL')
client = MongoClient(url)
db = client['qa_benchmarking']

def endorctl_scan(collection_name):
    global endor_ctl_bin
    global rem_dir_cmd 
    branch="main"
    total_cpu, total_memory = ("NA","NA")
    CUR_DIR = os.getcwd()
    if os.name == 'posix':
        endor_ctl_bin = "$endorctl"
        rem_dir_cmd = "rm -rf "
    if os.name == 'nt':
        endor_ctl_bin = "endorctl.exe"  
        rem_dir_cmd = "rmdir /Q /S "
    cmd = endor_ctl_bin + " --version"
    total_cpu, total_memory = capture_total_memory_cpu()
    output, err = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, text=True).communicate() 
    endorctl_version = output.split(" ")[-1].rstrip('\n')
    log.info("############### Running scan on {} endorctl version ############".format(endorctl_version))
    results_collection = collection_name+"_results_"+endorctl_version
    failed_collection= "FAILED_REPOS"
    batch_size=100
    total_documents = db[collection_name].count_documents({})
    num_batches = math.ceil(total_documents / batch_size)

    try:
        for batch_num in range(num_batches):
            primary_data = db[collection_name].find({}).skip(batch_num * batch_size).limit(batch_size)
        # for batch_num in range(num_batches - 1, -1, -1):
        #     primary_data = db[collection_name].find({}).skip(batch_num * batch_size).limit(batch_size)
            # documents = list(primary_data)
            for row in primary_data:
                result = {}
                if "GitURL" not in row:
                    log.error("GitURL field not found in document.")
                    continue
                query = {
                    "GitURL": row["GitURL"],
                    "TotalCPUCores": total_cpu,
                    "TotalMemory": total_memory
                }
                existing_doc_results = db[results_collection].find_one(query)

                existing_doc_failed = db[failed_collection].find_one(query)

                if existing_doc_results or existing_doc_failed:
                    log.info("Existing document found in either results_collection or failed_collection.")
                    continue
                curl_cmd = "curl -LI " + row["GitURL"] + " -o /dev/null -w '%{http_code}\n' -s"
                output, err = subprocess.Popen(curl_cmd, stdout=subprocess.PIPE, shell=True, text=True).communicate() 
                if output.strip() and int(output) != 200:
                    log.error("Repo does not exist or failed access  = {}".format(row["GitURL"]))
                    continue
                pm, build_status, total_pkgs, total_deps, quick_scan_duration, full_scan_duration = clone_and_scan_repo(row["GitURL"], row["GitRef"], row["Language"], row["BuildTool"])
                if(build_status=="fail"):
                    result["Language"] = row["Language"]
                    result["GitURL"] = row["GitURL"]
                    result["GitRef"] = row["GitRef"]
                    result["BuildTool"] = pm
                    result["BuildStatus"] = build_status
                    result["TotalCPUCores"] = total_cpu
                    result["TotalMemory"] = total_memory        
                    db[failed_collection].insert_one(result)
                    continue
                if any(variable == 0 for variable in [total_pkgs,total_deps,quick_scan_duration, full_scan_duration, total_cpu, total_memory]):
                    continue
                if pm and build_status == "pass":
                    result["Language"] = row["Language"]
                    result["GitURL"] = row["GitURL"]
                    result["GitRef"] = row["GitRef"]
                    result["BuildTool"] = pm
                    result["BuildStatus"] = build_status
                    result["FileCount"] = row["FileCount"]
                    result["LinesofCode"] = row["LinesofCode"]
                    result["PackageCount"] = total_pkgs
                    result["DependencyCount"] = total_deps
                    result["QuickScanDuration"] = quick_scan_duration
                    result["FullScanDuration"] = full_scan_duration
                    result["TotalCPUCores"] = total_cpu
                    result["TotalMemory"] = total_memory
                    db[results_collection].insert_one(result)
            primary_data.close()
        log.info("FINISHED ALL SCANNING")

    except Exception as e:
        log.error("ERROR: Found following exception {} ".format(e))

def delete_projects(repo):
    try:
        log.info("\n\n\n############### Deleting {} repo ############".format(repo))
        scan_dir = os.path.basename(repo).split(".")[0]    
        endor_api =  endor_ctl_bin + " api list -r Project --filter=\"meta.name matches  '" + scan_dir + "'\" --field-mask=uuid"
        data = ""
        for i in range(3):
            output = subprocess.Popen(endor_api, stdout=subprocess.PIPE,shell=True,text=True).communicate() 
            data = json.loads(output[0]) 
            if ('uuid' in data):
                break
            else:
                time.sleep(5)            
     
        project_id = data['list']['objects'][0]['uuid']
        log.info("\n\n############ Deleting the {} : {} project details##############".format(scan_dir,project_id)) 
        endor_api =  endor_ctl_bin + " api delete  -r Project --uuid=" + project_id
        log.info("Endor ctl command  = {}".format(endor_api))
        data = ""
        for i in range(3):
            output = subprocess.Popen(endor_api, stdout=subprocess.PIPE,shell=True,text=True).communicate() 
            if ("Successfully deleted message" in output):
                break
            else:
                time.sleep(5)                   
        
    except Exception as e:
        log.error("ERROR: Found following exception {} ".format(e))

def clone_and_scan_repo(repo,gitref,lang,build_tool):
    pm,build_status,total_pkgs,total_deps,quick_scan_duration,full_scan_duration = (build_tool, "pass",0,0,0,0)
    CUR_DIR = os.getcwd()
    try:
        CLONE_PATH = os.path.join(CLONE_DIR,lang,current_date_time)
        log.info("\n\n\n############### Scanning {} repo ############".format(repo))
        repo_name = repo.split("/")[-1]
        repo_path = os.path.join(CLONE_PATH,repo_name)
        local_repo = clone_repo(repo, repo_path, gitref)
        log.info(f"{local_repo.working_dir} copied successfully")
        pm,build_status,exception_msg = build.determine_build_manager(repo_path,build_tool)
        os.chdir(CUR_DIR)
        if build_status == "fail":
            log.error(f"Build is failed: {exception_msg}")
            return pm,build_status,total_pkgs,total_deps,quick_scan_duration,full_scan_duration
        
        log.info("Initiating quick scan...")
        endor_ctl_cmd = endor_ctl_bin + " scan  --quick-scan --path=" + repo_path + " --log-level=info --languages=" + lang
        log.info("Endor ctl command  = {}".format(endor_ctl_cmd))
        start_time = time.time()
        output = subprocess.Popen(endor_ctl_cmd, stdout=subprocess.PIPE,shell=True,text=True).communicate() 
        end_time = time.time()
        total_time = int(end_time - start_time)
        quick_scan_duration = total_time 
        log.info(f"Quick scan duration: {quick_scan_duration} ")
        # Initiating full scan
        log.info("Initiating full scan...")
        endor_ctl_cmd = endor_ctl_bin + " scan --path=" + repo_path + " --log-level=info --languages=" + lang
        log.info("Endor ctl command  = {}".format(endor_ctl_cmd))
        start_time = time.time()
        output = subprocess.Popen(endor_ctl_cmd, stdout=subprocess.PIPE,shell=True,text=True).communicate() 
        end_time = time.time()
        total_time = int (end_time - start_time)
        full_scan_duration = total_time
        log.info("Full scan duration:  = {}".format(full_scan_duration))   
      
        endor_api =  endor_ctl_bin + " api list -r Project --filter=\"meta.name matches  '" + repo_name + "'\" --field-mask=uuid"
        data = ""
        for i in range(3):
            output = subprocess.Popen(endor_api, stdout=subprocess.PIPE,shell=True,text=True).communicate() 
            data = json.loads(output[0]) 
            if ('uuid' in data):
                break
            else:
                time.sleep(5)            
     
        project_id = data['list']['objects'][0]['uuid']
        log.info("\n\n############Capturing the {} : {} project details##############".format(repo_path,project_id))
        total_pkgs,total_deps = capture_package_dependency_count(repo,project_id) 
        # total_cpu, total_memory =  capture_total_memory_cpu()
        cmd = rem_dir_cmd + repo_path 
        log.info("Removing cloned repo: {}".format(repo_path))
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True,text=True).communicate() 
        return pm,build_status,total_pkgs,total_deps,quick_scan_duration,full_scan_duration              
        
    except Exception as e:
        log.error("ERROR: Found following exception {} ".format(e))
        return pm,build_status,total_pkgs,total_deps,quick_scan_duration,full_scan_duration

@timeout(900)
def clone_repo( repo_url, directory, git_refs):
    repo = ""
    try:
        shutil.rmtree(directory, ignore_errors=True)
        repo = git.Repo.clone_from(repo_url, directory)
        repo.git.checkout(git_refs)
        log.info(f"Switched to branch: {git_refs}")
        log.info(f"Repository cloned to {directory} and git ref is : {git_refs}")
        return repo
    except Exception as e:
        log.error(f"Failed to clone repo: {e}")
        return repo

def capture_package_dependency_count(repo,project_id):
    total_pkgs = 0
    total_deps = 0
    try:
        log.info("\n======Capturing Total packages=========")
        endor_api = endor_ctl_bin + " api list -r PackageVersion --filter='spec.project_uuid==" + project_id + " and context.type==CONTEXT_TYPE_MAIN' --field-mask meta.name -t 200s --count"
        log.info("Endor api = {}".format(endor_api))
        data = ""
        for i in range(3):
            output = subprocess.Popen(endor_api, stdout=subprocess.PIPE,shell=True,text=True).communicate() 
            data = json.loads(output[0]) 
            if ('count_response' in data):
                break
            else:
                time.sleep(5)   
        if 'count' in data['count_response']:
            total_pkgs = data['count_response']['count']                 
            log.info("Total packages: {}" .format(total_pkgs)) 
        else:
            log.info("PACKAGES = 0")
            total_pkgs=0

        log.info("\n======Capturing total dependencies=========")
        #endor_api = endor_ctl_bin + " api list -r PackageVersion --group-aggregation-paths=spec.resolved_dependencies.dependencies.name --filter=spec.project_uuid==" + project_id + " --field-mask=spec.resolved_dependencies.dependencies -t 200s"
        endor_api = endor_ctl_bin + " api list -r DependencyMetadata --filter=spec.importer_data.project_uuid==" + project_id + " -o json -t 200s --group-aggregation-paths=meta.name --group-unique-value-paths=spec.dependency_data.direct,spec.dependency_data.reachable"
        log.info("Endor api = {}".format(endor_api))
        for i in range(3):
            output = subprocess.Popen(endor_api, stdout=subprocess.PIPE,shell=True,text=True).communicate() 
            data = json.loads(output[0]) 
            if ('group_response' in data):
                break
            else:
                time.sleep(5) 
        deplist = {}
        resolved_dependencies = []
        
        if 'groups' in data['group_response'].keys():
            for depname in data['group_response']['groups']:
                deplist = json.loads(depname)
                if deplist[0]['value'] is not None:
                    resolved_dependencies.append(deplist[0]['value'])
            resolved_dependencies = list(set(resolved_dependencies))
            total_deps = len(resolved_dependencies)
            log.info("Total dependencies : {} " .format(total_deps)) 
        else:
            log.info("DEPENDENCIES = 0")
            total_deps=0
        return  total_pkgs,total_deps  
                   
    except Exception as e:
        log.error("ERROR: Found following exception {} ".format(e))  
        return  total_pkgs,total_deps 

def capture_total_memory_cpu():
    try:
        resources_env = os.environ.get("RESOURCES")
        if resources_env!="null:null":
            # Split the string into individual components
            cpu, memory = resources_env.split(":")
            cpu=int(cpu)
                #only the numeric part of the memory it looks like ""9Gi or 100Gi""
            memory=int(memory)[0:-2]
            log.info("CPU Request: {} ".format(cpu))
            log.info("Memory Request: {} ".format(memory))
        return cpu, memory
    except Exception as e:
        log.error("ERROR: Found following exception {} ".format(e))
        return  cpu,memory       
    

''' Main function 
Decalred command line arg parser '''
def main():
    parser = argparse.ArgumentParser(description="Enter the buildable repository collection name")
    parser.add_argument("--repo_list", "-r", type=str, help="Collection of buildable repos")
    args = parser.parse_args()
    cfg_file = args.repo_list
    log.info("Using config-file  = {}".format(cfg_file))
    if "SCP_ENDOR_NAMESPACE" not in os.environ or "SCP_ENDOR_API_CREDENTIALS_KEY" not in os.environ or "SCP_ENDOR_API_CREDENTIALS_SECRET" not in os.environ or "SCP_ENDOR_API" not in os.environ:
        log.error(f"The environment variable SCP_ENDOR_NAMESPACE or SCP_ENDOR_API_CREDENTIALS_KEY or SCP_ENDOR_API_CREDENTIALS_SECRET or SCP_ENDOR_API is not set.")  
        sys.exit(1)
    endorctl_scan(cfg_file)

if __name__ == "__main__":
    main()
    
