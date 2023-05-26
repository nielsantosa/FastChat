#!/bin/bash

python3 fastchat/model/apply_delta.py \
    --base-model-path decapoda-research/llama-13b-hf \
    --target-model-path /output_model \
    --delta-path lmsys/vicuna-13b-delta-v1.1 && \
    rm -rf /.cache/huggingface

NVIDIA_SMI=$(nvidia-smi)
if [ "command not found" == *"$NVIDIA_SMI"* ];
then
  python3 fastchat/serve/model_worker.py --model-path /output_model --device cpu;
else
  python3 fastchat/serve/model_worker.py --model-path /output_model --load-8bit;
fi
