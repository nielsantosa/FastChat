"""
Launching Lambda Instance from Lambda Cloud API
https://cloud.lambdalabs.com/api/v1/docs#operation/launchInstance
"""

import os
import argparse
import requests
import logging
import time

from typing import Optional


logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class Script():
    def __init__(self, options):
        self.options = options
        self.api_key = options.LAMBDALABS_API_KEY

    def _check_available_lambda_instances(self) -> Optional[dict]:
        URL = "https://cloud.lambdalabs.com/api/v1/instance-types"

        res = requests.get(URL, auth=(self.api_key, ""))

        if res.status_code != 200:
            logging.warning(f"{res.status_code}: {URL} - Unable to get lambdalabs instances")
            return

        return res.json()

    def _check_running_lambda_instances(self):
        URL = "https://cloud.lambdalabs.com/api/v1/instances"

        res = requests.get(URL, auth=(self.api_key, ""))
        if res.status_code != 200:
            logging.warning(f"{res.status_code}: {URL} - Unable to get lambdalabs instances")
            return

        return res.json()

    def _terminate_lambda_instances(self) -> None:
        instance_ids = self.options.INSTANCE_IDS
        if not instance_ids:
            logging.warning("Please insert instance_ids to be terminated")
            return

        if isinstance(instance_ids, str):
            instance_ids = instance_ids.split(",")

        URL = "https://cloud.lambdalabs.com/api/v1/instance-operations/terminate"
        params = {
            "instance_ids": instance_ids,
        }
        headers = {
            "Content-Type": "application/json",
        }

        res = requests.post(URL, auth=(self.api_key, ""), headers=headers, json=params)

        if res.status_code != 200:
            logging.warning(f"{res.status_code}: {URL} - Unable to terminate lambdalabs instances")
            return

        logging.info(f"Successfully terminate {instance_ids}")

    def _start_lambda_instance(self) -> None:
        res = self._check_available_lambda_instances()
        if not res:
            return

        lambda_instances = res.get("data", {})
        desired_instances = self.options.DESIRED_INSTANCES
        if desired_instances not in lambda_instances:
            logging.warning(f"{desired_instances} format is wrong")
            return

        capacity = lambda_instances.get(desired_instances, {}).get("regions_with_capacity_available")
        if not capacity:
            logging.warning(f"{desired_instances} is not available")
            return

        first_region_available = capacity[0]
        region_name = first_region_available.get("name")
        params = {
            "region_name": region_name,
            "instance_type_name": desired_instances,
            "ssh_key_names": [ # name of the SSH_KEY, not the SSH_KEY
                self.options.SSH_KEY,
            ],
            "file_system_names": [],
            "quantity": 1,
            "name": self.options.INSTANCE_NAME,
        }

        LAUNCH_URL = "https://cloud.lambdalabs.com/api/v1/instance-operations/launch"
        headers = {
            "Content-Type": "application/json",
        }
        launch_res = requests.post(
            LAUNCH_URL,
            auth=(self.api_key, ""),
            headers=headers,
            json=params,
        )

        if launch_res.status_code != 200:
            logging.warning(f"{launch_res.status_code}: {LAUNCH_URL} - Unable to get lambdalabs instances: {launch_res.text}")
            return

        instance_ids = launch_res.json().get("data", {}).get("instance_ids")
        logging.info(f"Launching {desired_instances} success: Instance_IDS: {instance_ids}")

        # get IP Address
        instance_id = instance_ids[0]
        ip_address = None
        while ip_address is None:
            time.sleep(10) # wait for reboot

            running_res = self._check_running_lambda_instances()

            if not running_res:
                return

            running_instances = running_res.get("data")
            instance_info = [i for i in running_instances if i.get("id") == instance_id][0]
            ip_address = instance_info.get("ip")

        logging.info(f"ip_address is {ip_address}")


    def run(self) -> None:
        logging.info("Running script...")
        if self.options.launch_lambda_instances == "True":
            self._start_lambda_instance()
            return

        if self.options.terminate_lambda_instances == "True":
            self._terminate_lambda_instances()
            return

        logging.info("Terminating script...")


def init_parser():
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help'
    )

    return parser


def main():
    parser = init_parser()
    # Process Options
    parser.add_argument("--launch_lambda_instances", type=str, choices=["True", "False"], help="Bool value to launch lambda instances")
    parser.add_argument("--terminate_lambda_instances", type=str, choices=["True", "False"], help="Bool value to terminate lambda instances")

    # General Options
    parser.add_argument("--LAMBDALABS_API_KEY", default=os.environ.get("LAMBDALABS_API_KEY"), help="Get from Cloud API")

    # launch_instances
    parser.add_argument("--SSH_KEY", default=os.environ.get("SSH_KEY"), help="Name of the SSH_KEY, e.g.'nathaniel'. NOT the PUBLIC SSH_KEY")
    parser.add_argument("--DESIRED_INSTANCES", default=os.environ.get("DESIRED_INSTANCES"), help="List of lambda instances. Check https://cloud.lambdalabs.com/api/v1/docs#operation/launchInstance")
    parser.add_argument("--INSTANCE_NAME", default="test-instance", help="Manual Name of the created lambda instances.")

    # terminate_instances
    parser.add_argument("--INSTANCE_IDS", default="test-instance", help="Manual Name of the created lambda instances.")

    options = parser.parse_args()
    script = Script(options)
    script.run()

if __name__ == "__main__":
    main()

