#!/usr/bin/bash

# This script is meant only to run on docker compose

# Create code directory as a parent directory
cd ~
mkdir code
cd code

# To download the LLM Repo
# git clone https means that need authorization everytime you push and pull
git clone https://github.com/nielsantosa/FastChat.git

# To run docker compose
cd ~/code/FastChat
NVIDIA_SMI=$(nvidia-smi)
if [ "command not found" == *"$NVIDIA_SMI"* ];
then
  # cpu machine
  sudo docker compose -f docker-compose.yml up;
else
  # nvidia gpu machine
  sudo docker compose -f docker-compose.gpu.yml up;
fi
