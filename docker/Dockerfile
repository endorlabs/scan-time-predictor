FROM amd64/ubuntu:22.04

# Install necessary packages
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    unzip \
    openjdk-17-jdk \
    sudo \
    unzip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy your script into the container
COPY script_amd.sh /usr/local/bin/setup_environment.sh

ENV type=null
ENV LANGUAGE=null
ENV BUILD_TOOL=null
ENV GIT_TOKEN=null
ENV RESOURCES="null:null"
# COPY id_rsa /usr/local/bin/id_rsa
# # Give execute permissions to the script
RUN chmod +x /usr/local/bin/setup_environment.sh

# Run the script when the container starts
CMD ["/bin/bash", "/usr/local/bin/setup_environment.sh"]
