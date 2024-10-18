#!/bin/bash
set +x
shopt -s expand_aliases
# Update package lists
apt-get update

apt install git -y
apt install pip -y


# #Download Java

wget https://download.oracle.com/java/17/archive/jdk-17.0.10_linux-x64_bin.tar.gz
tar -xvf jdk-17.0.10_linux-x64_bin.tar.gz
mkdir /opt/java
mv jdk-* /opt/java
export JAVA_HOME="/opt/java/jdk-17.0.10"
export PATH="${JAVA_HOME}/bin:${PATH}"

# Download the latest Apache Maven version
wget https://dlcdn.apache.org/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.tar.gz
tar -xvf apache-maven-3.9.6-bin.tar.gz
mkdir /opt/maven
# Move Maven directory to /opt
mv apache-maven-* /opt/maven
# Add Maven bin directory to PATH
export M2_HOME="/opt/maven/apache-maven-3.9.6"
export PATH="${M2_HOME}/bin:${PATH}"

# Download Gradle
wget https://services.gradle.org/distributions/gradle-8.6-bin.zip
mkdir /opt/gradle
apt-get install unzip -y
unzip -d /opt/gradle gradle-8.6-bin.zip
export PATH=/opt/gradle/gradle-8.6/bin:$PATH

apt-get update
apt install cloc -y

#Downloading Go
wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
tar -xvf go1.22.0.linux-amd64.tar.gz
sudo mv go /opt
export PATH="/opt/go/bin:$PATH"

# Reload bashrc to apply changes
source ~/.bashrc

# Verify installations
mvn -version
java -version
gradle -v
cloc --version
go version

apt install python3-venv -y
python3 -m venv env
source env/bin/activate

mkdir /opt/endorctl

cd /opt/endorctl
curl https://api.endorlabs.com/download/latest/endorctl_linux_amd64 -o endorctl
# alias endorctl="$PWD/endorctl"
chmod +x ./endorctl
echo "export endorctl=$PWD/endorctl" >> ~/.bashrc

# alias endorctl=$endorctl
source ~/.bashrc

$endorctl --version

if [ -z "$GIT_TOKEN" ] || [ "$GIT_TOKEN" == "null" ]; then
  echo "GIT_TOKEN is not set or is null. Aborting script."
  exit 1
fi

# Clone the repository if GIT_TOKEN is valid
git clone https://shristi-mn:"$GIT_TOKEN"@github.com/endorlabs/qa-benchmarking.git
cd qa-benchmarking
$endorctl --version
pip3 install -r requirements.txt

export ENDOR_NAMESPACE=$ENDOR_NAMESPACE && export ENDOR_API_CREDENTIALS_KEY=$ENDOR_API_CREDENTIALS_KEY && export ENDOR_API_CREDENTIALS_SECRET=$ENDOR_API_CREDENTIALS_SECRET && export ENDOR_API=https://api.staging.endorlabs.com

# Check if LANGUAGE and BUILD_TOOL are provided
if [ -z "$LANGUAGE" ] || [ "$LANGUAGE" == "null" ] || [ -z "$BUILD_TOOL" ] || [ "$BUILD_TOOL" == "null" ]; then
    echo "Error: Please provide LANGUAGE and BUILD_TOOL as arguments."
    usage
    exit 1
fi

# Determine action based on 'type' environment variable
case "$type" in
    scan)
        # Install required packages and set up environment based on language and build tool
        case $LANGUAGE in
            java)
                case $BUILD_TOOL in
                    maven)
                        echo "Performing actions for Java with Maven..."
                        python3 endor_scan.py --repo_list data_java_maven
                        echo "FINISSHH - $LANGUAGE $BUILD_TOOL"
                        exit
                        ;;
                    gradle)
                        echo "Performing actions for Java with Gradle..."
                        python3 endor_scan.py --repo_list data_java_gradle
                        echo "FINISSHH - $LANGUAGE $BUILD_TOOL"
                        exit
                        ;;
                    *)
                        echo "Invalid BUILD_TOOL for Java: $BUILD_TOOL"
                        usage
                        exit 1
                        ;;
                esac
                ;;
            python)
                case $BUILD_TOOL in
                    pip)
                        echo "Performing actions for Python with Pip..."
                        python3 endor_scan.py --repo_list data_python_pip
                        echo "FINISSHH - $LANGUAGE $BUILD_TOOL"
                        exit
                        ;;
                    *)
                        echo "Invalid BUILD_TOOL for Python: $BUILD_TOOL"
                        usage
                        exit 1
                        ;;
                esac
                ;;
            go)
                case $BUILD_TOOL in
                    go)
                        echo "Performing actions for Go..."
                        python3 endor_scan.py --repo_list data_go_go
                        echo "FINISSHH - $LANGUAGE $BUILD_TOOL"
                        exit
                        ;;
                    *)
                        echo "Invalid BUILD_TOOL for Go: $BUILD_TOOL"
                        usage
                        exit 1
                        ;;
                esac
                ;;
            *)
                echo "Invalid LANGUAGE: $LANGUAGE"
                usage
                exit 1
                ;;
        esac
        ;;
    fetch)
        # Install required packages and set up environment based on language and build tool
        case $LANGUAGE in
            java)
                case $BUILD_TOOL in
                    maven)
                        echo "Performing actions for Java with Maven..."
                        python3 find_repo.py -l "$LANGUAGE" -b "$BUILD_TOOL" -r 10000
                        echo "FINISSHH - $LANGUAGE $BUILD_TOOL"
                        exit
                        ;;
                    gradle)
                        echo "Performing actions for Java with Gradle..."
                        python3 find_repo.py -l "$LANGUAGE" -b "$BUILD_TOOL" -r 10000
                        echo "FINISSHH - $LANGUAGE $BUILD_TOOL"
                        exit
                        ;;
                    *)
                        echo "Invalid BUILD_TOOL for Java: $BUILD_TOOL"
                        usage
                        exit 1
                        ;;
                esac
                ;;
            python)
                case $BUILD_TOOL in
                    pip)
                        echo "Performing actions for Python with Pip..."
                        python3 find_repo.py -l "$LANGUAGE" -b "$BUILD_TOOL" -r 10000
                        echo "FINISSHH - $LANGUAGE $BUILD_TOOL"
                        exit
                        ;;
                    *)
                        echo "Invalid BUILD_TOOL for Python: $BUILD_TOOL"
                        usage
                        exit 1
                        ;;
                esac
                ;;
            go)
                case $BUILD_TOOL in
                    go)
                        echo "Performing actions for Go..."
                        python3 find_repo.py -l "$LANGUAGE" -b "$BUILD_TOOL" -r 10000
                        echo "FINISSHH - $LANGUAGE $BUILD_TOOL"
                        exit
                        ;;
                    *)
                        echo "Invalid BUILD_TOOL for Go: $BUILD_TOOL"
                        usage
                        exit 1
                        ;;
                esac
                ;;
            *)
                echo "Invalid LANGUAGE: $LANGUAGE"
                usage
                exit 1
                ;;
        esac
        ;;
    *)
        echo "Invalid type: $type"
        exit 1
        ;;
esac

