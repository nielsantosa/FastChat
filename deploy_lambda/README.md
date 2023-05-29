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

What to do:
- download dotfiles from nielsantosa (you can download your own dotfiles), to setup necessary tools for the debugging process
- some setup regarding the dotfiles
- create proper directory
- git clone the Repo to run the self-hosted LLM
- run the docker-compose to run the self-hosted LLM
