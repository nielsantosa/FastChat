#!/usr/bin/bash

# This script is meant only to run on docker compose

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

# Run multiple applications at once.
# Use tmux or multiple terminals to run on multiple windows
