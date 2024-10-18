import os
import sys
import subprocess
import src.utils.logging_config as log
log = log.getLogger()

def build_pip_project(project_path,setup_file_name):
    build_status = "fail"
    exception_msg = ""
    os.chdir(project_path)
    try:
        venv_cmd = "python3 -m venv venv"
        subprocess.run(venv_cmd, timeout=1800, shell=True, check=True)
        log.info(f"Virtual environment 'venv' created successfully.")
        if setup_file_name == "requirements.txt":
            pip_install_cmd = "venv/bin/python3 -m pip install -r requirements.txt"
            subprocess.run(pip_install_cmd, timeout=1800, shell=True, check=True)
        if setup_file_name == "setup.py":
            pip_install_cmd = "venv/bin/python3 -m pip install ."
            subprocess.run(pip_install_cmd, timeout=1800, shell=True, check=True)
        log.info("Pip project built successfully.")
        build_status = "pass"
    except subprocess.CalledProcessError as e:
        log.error(f"Error building pip project: {e}")
        build_status = "fail"
        exception_msg = e
    except subprocess.TimeoutExpired as e:
        log.error(f"Command execution timed out: {e}")
        build_status = "fail"
        exception_msg = e
    except Exception as e:
        print(f"An error occurred: {e}")
        build_status = "fail"
        exception_msg = e
    
    return build_status, exception_msg

def build_poetry_project(project_path):
    build_status = "fail"
    exception_msg = ""
    os.chdir(project_path)
    poetry_build_command = "poetry install"  
    try:
        subprocess.run(poetry_build_command, timeout=1800, shell=True, check=True)
        log.info("Poetry project built successfully.")
        build_status = "pass"
    except subprocess.CalledProcessError as e:
        log.error(f"Error building Poetry project: {e}")
        build_status = "fail"
        exception_msg = e
    except subprocess.TimeoutExpired as e:
        log.error(f"Command execution timed out: {e}")
        build_status = "fail"
        exception_msg = e
    except Exception as e:
        print(f"An error occurred: {e}")
        build_status = "fail"
        exception_msg = e
    
    return build_status, exception_msg

def build_go_project(project_path):
    build_status = "fail"
    exception_msg = ""
    os.chdir(project_path)
    go_build_command = "go mod tidy -e"  
    try:
        subprocess.run(go_build_command, timeout=1800, shell=True, check=True)
        log.info("Go project built successfully.")
        build_status = "pass"
    except subprocess.CalledProcessError as e:
        log.error(f"Error building Go project: {e}")
        build_status = "fail"
        exception_msg = e
    except subprocess.TimeoutExpired as e:
        log.error(f"Command execution timed out: {e}")
        build_status = "fail"
        exception_msg = e
    except Exception as e:
        print(f"An error occurred: {e}")
        build_status = "fail"
        exception_msg = e
    
    return build_status, exception_msg

def build_npm_project(project_path):
    build_status = "fail"
    exception_msg = ""
    os.chdir(project_path)
    npm_build_command = "npm install"  
    try:
        subprocess.run(npm_build_command, timeout=1800, shell=True, check=True)
        log.info("NPM project built successfully.")
        build_status = "pass"
    except subprocess.CalledProcessError as e:
        log.error(f"Error building NPM project: {e}")
        build_status = "fail"
        exception_msg = e
    except subprocess.TimeoutExpired as e:
        log.error(f"Command execution timed out: {e}")
        build_status = "fail"
        exception_msg = e
    except Exception as e:
        print(f"An error occurred: {e}")
        build_status = "fail"
        exception_msg = e
    
    return build_status, exception_msg

def build_yarn_project(project_path):
    build_status = "fail"
    exception_msg = ""
    os.chdir(project_path)
    yarn_build_command = "yarn install"  
    try:
        subprocess.run(yarn_build_command, timeout=1800, shell=True, check=True)
        log.info("Yarn project built successfully.")
        build_status = "pass"
    except subprocess.CalledProcessError as e:
        log.error(f"Error building Yarn project: {e}")
        build_status = "fail"
        exception_msg = e
    except subprocess.TimeoutExpired as e:
        log.error(f"Command execution timed out: {e}")
        build_status = "fail"
        exception_msg = e
    except Exception as e:
        print(f"An error occurred: {e}")
        build_status = "fail"
        exception_msg = e
    
    return build_status, exception_msg

def build_pnpm_project(project_path):
    build_status = "fail"
    exception_msg = ""
    os.chdir(project_path)
    pnpm_build_command = "pnpm install"  
    try:
        subprocess.run(pnpm_build_command, timeout=1800, shell=True, check=True)
        log.info("PNPM project built successfully.")
        build_status = "pass"
    except subprocess.CalledProcessError as e:
        log.error(f"Error building PNPM project: {e}")
        build_status = "fail"
        exception_msg = e
    except subprocess.TimeoutExpired as e:
        log.error(f"Command execution timed out: {e}")
        build_status = "fail"
        exception_msg = e
    except Exception as e:
        print(f"An error occurred: {e}")
        build_status = "fail"
        exception_msg = e
    
    return build_status, exception_msg

def build_ruby_project(project_path):
    build_status = "fail"
    exception_msg = ""
    os.chdir(project_path)
    ruby_build_command = "bundler install"  
    try:
        subprocess.run(ruby_build_command, timeout=1800, shell=True, check=True)
        log.info("Ruby project built successfully.")
        build_status = "pass"
    except subprocess.CalledProcessError as e:
        log.error(f"Error building Ruby project: {e}")
        build_status = "fail"
        exception_msg = e
    except subprocess.TimeoutExpired as e:
        log.error(f"Command execution timed out: {e}")
        build_status = "fail"
        exception_msg = e
    except Exception as e:
        print(f"An error occurred: {e}")
        build_status = "fail"
        exception_msg = e
    
    return build_status, exception_msg

def build_php_project(project_path):
    build_status = "fail"
    exception_msg = ""
    os.chdir(project_path)
    php_build_command = "composer install --no-interaction"  
    try:
        subprocess.run(php_build_command, timeout=1800, shell=True, check=True)
        log.info("PHP project built successfully.")
        build_status = "pass"
    except subprocess.CalledProcessError as e:
        log.error(f"Error building PHP project: {e}")
        build_status = "fail"
        exception_msg = e
    except subprocess.TimeoutExpired as e:
        log.error(f"Command execution timed out: {e}")
        build_status = "fail"
        exception_msg = e
    except Exception as e:
        print(f"An error occurred: {e}")
        build_status = "fail"
        exception_msg = e
    
    return build_status, exception_msg

def build_scala_project(project_path):
    build_status = "fail"
    exception_msg = ""
    os.chdir(project_path)
    sbt_build_command1 = "sbt compile -batch"
    sbt_build_command2 = "sbt projects"   
    try:
        subprocess.run(sbt_build_command1, timeout=1800, shell=True, check=True)
        subprocess.run(sbt_build_command2, timeout=1800, shell=True, check=True)
        log.info("Scala project built successfully.")
        build_status = "pass"
    except subprocess.CalledProcessError as e:
        log.error(f"Error building Scala project: {e}")
        build_status = "fail"
        exception_msg = e
    except subprocess.TimeoutExpired as e:
        log.error(f"Command execution timed out: {e}")
        build_status = "fail"
        exception_msg = e
    except Exception as e:
        print(f"An error occurred: {e}")
        build_status = "fail"
        exception_msg = e
    
    return build_status, exception_msg

def build_maven_project(project_path):
    build_status = "fail"
    exception_msg = ""
    os.chdir(project_path)
    maven_build_command = "mvn clean install"
    try:
        subprocess.run(maven_build_command, timeout=1800, shell=True, check=True)
        log.info("Maven project built successfully.")
        build_status = "pass"
    except subprocess.CalledProcessError as e:
        log.error(f"Error building Maven project: {e}")
        build_status = "fail"
        exception_msg = e
    except subprocess.TimeoutExpired as e:
        log.error(f"Command execution timed out: {e}")
        build_status = "fail"
        exception_msg = e
    except Exception as e:
        print(f"An error occurred: {e}")
        build_status = "fail"
        exception_msg = e

    return build_status, exception_msg    

def build_gradle_project(project_path):
    build_status = "fail"
    exception_msg = ""
    os.chdir(project_path)
    gradle_build_command = "gradle assemble"
    if os.path.exists("gradlew"):
        os.chmod("gradlew", 600)
        gradle_build_command = "./gradlew assemble"
    try:
        subprocess.run(gradle_build_command, timeout=1800, shell=True, check=True)
        log.info("Gradle project built successfully.")
        build_status = "pass"
    except subprocess.CalledProcessError as e:
        log.error(f"Error building Gradle project: {e}")
        build_status = "fail"
        exception_msg = e
    except subprocess.TimeoutExpired as e:
        log.error(f"Command execution timed out: {e}")
        build_status = "fail"
        exception_msg = e
    except Exception as e:
        print(f"An error occurred: {e}")
        build_status = "fail"
        exception_msg = e
    
    return build_status, exception_msg    

def determine_build_manager(directory,build_tool): 
    package_managers = ""
    build_status = "pass"
    exception_msg = ""
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name == "pom.xml" and build_tool == "maven":  
                build_path = os.path.dirname(os.path.join(root, name))
                if "maven" not in package_managers:
                    package_managers = "maven"
                bs,exception_msg = build_maven_project(build_path) 
                if bs == "fail":
                    build_status = "fail"
                    return package_managers, build_status, exception_msg

            # Gradle projects        
            if name == "build.gradle" and build_tool == "gradle":  
                build_path = os.path.dirname(os.path.join(root, name))
                if "gradle" not in package_managers:
                    package_managers = "gradle"
                bs,exception_msg = build_gradle_project(build_path) 
                if bs == "fail":
                    build_status = "fail"
                    return package_managers, build_status, exception_msg
                return package_managers, build_status, exception_msg

            # Python pip projects    
            if (name == "requirements.txt" or name == "setup.py")  and build_tool == "pip":  
                build_path = os.path.dirname(os.path.join(root, name))
                if "pip" not in package_managers:
                    package_managers = "pip"
                bs, exception_msg = build_pip_project(build_path,name) 
                if bs == "fail":
                    build_status = "fail"
                    return package_managers, build_status, exception_msg

            # Python poetry projects        
            if name == "poetry.lock" and build_tool == "poetry":  
                build_path = os.path.dirname(os.path.join(root, name))
                if "poetry" not in package_managers:
                    package_managers = "poetry"
                bs,exception_msg = build_poetry_project(build_path) 
                if bs == "fail":
                    build_status = "fail"
                    return package_managers, build_status, exception_msg  
                  
            # Go projects   
            if name == "go.mod" and build_tool == "go":  
                build_path = os.path.dirname(os.path.join(root, name))
                if "go" not in package_managers:
                    package_managers = "go"
                bs,exception_msg = build_go_project(build_path) 
                if bs == "fail":
                    build_status = "fail"
                    return package_managers, build_status, exception_msg  
                
            # NPM projects   
            if name == "package.json" and build_tool == "npm":  
                build_path = os.path.dirname(os.path.join(root, name))
                if "npm" not in package_managers:
                    package_managers = "npm"
                bs,exception_msg = build_npm_project(build_path) 
                if bs == "fail":
                    build_status = "fail"
                    return package_managers, build_status, exception_msg   
            
            # Yarn projects   
            if name == "yarn.lock" and build_tool == "yarn":  
                build_path = os.path.dirname(os.path.join(root, name))
                if "yarn" not in package_managers:
                    package_managers = "yarn"
                bs,exception_msg = build_yarn_project(build_path) 
                if bs == "fail":
                    build_status = "fail"
                    return package_managers, build_status, exception_msg 

            # PNPM projects   
            if name == "pnpm-lock.yaml" and build_tool == "pnpm":  
                build_path = os.path.dirname(os.path.join(root, name))
                if "yarn" not in package_managers:
                    package_managers = "yarn"
                bs,exception_msg = build_pnpm_project(build_path) 
                if bs == "fail":
                    build_status = "fail"
                    return package_managers, build_status, exception_msg  
            
            # Ruby projects   
            if name == "Gemfile" and build_tool == "bundler":  
                build_path = os.path.dirname(os.path.join(root, name))
                if "bundler" not in package_managers:
                    package_managers = "bundler"
                bs,exception_msg = build_ruby_project(build_path) 
                if bs == "fail":
                    build_status = "fail"
                    return package_managers, build_status, exception_msg              

            # PHP projects   
            if name == "composer.json" and build_tool == "composer":  
                build_path = os.path.dirname(os.path.join(root, name))
                if "composer" not in package_managers:
                    package_managers = "composer"
                bs,exception_msg = build_php_project(build_path) 
                if bs == "fail":
                    build_status = "fail"
                    return package_managers, build_status, exception_msg 

            # Scala projects   
            if name == "build.sbt" and build_tool == "sbt":  
                build_path = os.path.dirname(os.path.join(root, name))
                if "sbt" not in package_managers:
                    package_managers = "sbt"
                bs,exception_msg = build_scala_project(build_path) 
                if bs == "fail":
                    build_status = "fail"
                    return package_managers, build_status, exception_msg    
                                                             
    return package_managers, build_status, exception_msg