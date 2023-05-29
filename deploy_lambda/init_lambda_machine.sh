# start lambda instance
#python3 lambda_cli_commands.py --launch_lambda_instances True --SSH_KEY "nathaniel" --DESIRED_INSTANCES "gpu_1x_a10" --INSTANCE_NAME "trial_99"

# terminate lambda instance
#python3 lambda_cli_commands.py --terminate_lambda_instances True --INSTANCE_IDS a64ce9eedc25411b92913a73c7d4b3d2

# get running lambda instance
python3 lambda_cli_commands.py --check_running_lambda_instances True
