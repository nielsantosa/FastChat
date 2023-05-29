# Deploy Lambda Instance through Lambda CLI

```
export LAMBDALABS_API_KEY=<YOUR TOKEN>
bash init_lambda_instance.py
```
Token can be generated using Lambda Clouds.
It will run the script from lambda_cli_commands.py.
Kindly ensure that you are starting or terminating properly.
NOTE!
Once you run the machine, ensure that you are terminating it properly. Double check the machine instance on clouds.lambda.com to ensure the machine has been terminated. 
Or else, it will incur substantial amount of cost as lambda machines are charged hourly.


# Commands once you enter Lambda Machine
Once you are inside lambda machine (through SSH or Jupyter Notebook online), you can run the rest of the commands to set up the machine.

I observed that lambda machine are automatically installed with these package:
- docker (and docker compose)
- tmux
- python (a certain version of python)
- nvidia-smi (for nvidia gpu monitoring)
- nvidia-container-toolkit (for enabling nvidia gpu usage from docker container)


## [FOR DEBUGGING - application manually run on the machine - without docker] What to do:
Download dotfiles from nielsantosa (you can download your own dotfiles), to setup necessary tools for the debugging process

Create `code` directory as a parent directory
```
cd ~
mkdir code
cd code
```

To download the LLM Repo
git clone https means that need authorization everytime you push and pull
```
git clone https://github.com/nielsantosa/FastChat.git
```

Setup the model
To apply lambda to model
```
cd ~/code/FastChat
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Build the model
```
cd ~/code/FastChat
export PYTHONPATH=$HOME/code/FastChat
python3 fastchat/model/apply_delta.py \
    --base-model-path decapoda-research/llama-13b-hf \
    --target-model-path $HOME/code/FastChat/output_model \
    --delta-path lmsys/vicuna-13b-delta-v1.1
```

Run these applications altogether and in sequence
1. Controller
```
cd ~/code/FastChat
python fastchat/serve/controller.py
```
2. Worker
```
cd ~/code/FastChat
python fastchat/serve/worker.py
```
3. Backend Nat
```
cd ~/code/FastChat
python fastchat/serve/backend_nat.py
```

Note : Don't forget to setup nginx + service to expose the port to public internet.


## [[FOR RUNNING WITH DOCKER COMPOSE ONLY] What to do:
Create `code` directory as a parent directory
```
cd ~
mkdir code
cd code
```

To download the LLM Repo
git clone https means that need authorization everytime you push and pull
```
git clone https://github.com/nielsantosa/FastChat.git
```

Run the docker compose
```
cd ~/code/FastChat

# CHOOSE ONE!
# cpu machine
sudo docker compose -f docker-compose.yml up;

# nvidia gpu machine
sudo docker compose -f docker-compose.gpu.yml up;
```

Note : Don't forget to setup nginx + service to expose the port to public internet.
