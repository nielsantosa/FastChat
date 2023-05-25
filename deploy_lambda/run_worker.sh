#!/bin/bash

NVIDIA_SMI=$(nvidia-smi)
if [ "command not found" == *"$NVIDIA_SMI"* ];
then
  python3 fastchat/serve/model_worker.py --model-path /output_model --device cpu;
else
  python3 fastchat/serve/model_worker.py --model-path /output_model --load-8bit;
fi
