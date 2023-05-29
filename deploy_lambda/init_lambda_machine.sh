# start lambda instance
#python3 start_lambda_instances.py --launch_lambda_instances True --SSH_KEY "nathaniel" --DESIRED_INSTANCES "gpu_1x_a10" --INSTANCE_NAME "trial_99"

# terminate lambda instance
python3 start_lambda_instances.py --terminate_lambda_instances True --INSTANCE_IDS ab0f8d0b2fb04041b362d8531f6539c1

