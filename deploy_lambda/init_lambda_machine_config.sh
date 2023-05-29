#!/usr/bin/bash

# Create code directory as a parent directory
cd ~
mkdir code
cd code

# To download the LLM Repo
# git clone https means that need authorization everytime you push and pull
git clone https://github.com/nielsantosa/FastChat.git

# To apply lambda to model
cd ~/code/FastChat
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

# Build the model
cd ~/code/FastChat
export PYTHONPATH=$HOME/code/FastChat
python3 fastchat/model/apply_delta.py \
    --base-model-path decapoda-research/llama-13b-hf \
    --target-model-path $HOME/code/FastChat/output_model \
    --delta-path lmsys/vicuna-13b-delta-v1.1

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
