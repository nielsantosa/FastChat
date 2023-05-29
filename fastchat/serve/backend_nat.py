import argparse
import json
import requests
import os

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.background import BackgroundTask

import uvicorn
from httpx import AsyncClient, Timeout

from fastchat.model.model_adapter import get_conversation_template

model_name = "output_model" # default
app = FastAPI()

class Logic:
    def __init__(self, options):
        self.options = options


@app.post("/v1/chat/completions")
async def api_get_chat_completions(request: Request):
    """
    Request Body:
        {
            "messages": [
                {"role": "system", "content": "..."},
                {"role": "user", "content": "..."},
                {"role": "assistant", "content": "..."},
                ...
            ]
        }
    """
    body = await request.json()
    messages = body.get("messages")
    temperature = body.get("temperature", 0.0)
    if not isinstance(temperature, (float, int)) and temperature <= 0.0 or temperature > 1:
        return JSONResponse(content="Temperature must be min 0.0 and max 1", status=400)

    max_new_tokens = body.get("max_new_tokens", 32)

    # process conv
    #conv = get_conversation_template(model_name)
    conv = get_conversation_template("vicuna-13b")
    for message in messages:
        if message.get("role") == "system":
            conv.system = message.get("content")
        elif message.get("role") in {"user"}:
            conv.append_message(conv.roles[0], message.get("content"))
        elif message.get("role") == "assistant":
            conv.append_message(conv.roles[1], message.get("content"))
    # template for AI to answer
    conv.append_message(conv.roles[1], None)
    prompt = conv.get_prompt()
    headers = {"User-Agent": "BackendNat"}

    # call and stream
    client = AsyncClient()
    #url = "http://localhost:21001/worker_generate_stream"
    url = f"{logic.options.controller_address}/worker_generate_stream"

    gen_params = {
        "model": model_name,
        "prompt": prompt,
        "temperature": temperature,
        "max_new_tokens": max_new_tokens,
        "stop": conv.stop_str,
        "stop_token_ids": conv.stop_token_ids,
        "echo": False,
    }
    print(f"Prompt: {prompt}")

    req = client.build_request(
        "POST",
        url,
        json=gen_params,
        headers=headers,
        timeout=Timeout(timeout=30),
    )


    import time
    async def _stream_response(response):
        output_memory = ""

        async for chunk in response.aiter_text():
            print(chunk)
            if chunk:
                data = json.loads(chunk.strip("\x00"))
                output = data["text"].strip()

                printed_output = output[len(output_memory):]
                output_memory = output

                """
                for letter in printed_output:
                    time.sleep(0.2)
                    yield letter.encode()
                    """

                yield printed_output.encode()

    print("Sending request and stream to worker")
    r = await client.send(req, stream=True)
    print("Returning the stream")
    return StreamingResponse(_stream_response(r), background=BackgroundTask(r.aclose))

    """
    response = requests.post(
        url,
        headers=headers,
        json=gen_params,
        stream=True,
    )

    print(f"{conv.roles[0]}: {message.get('content')}")
    print(f"{conv.roles[1]}: ", end="")
    prev = 0
    for chunk in response.iter_lines(decode_unicode=False, delimiter=b"\0"):
        if chunk:
            data = json.loads(chunk.decode())
            output = data["text"].strip()
            print(output[prev:], end="", flush=True)
            prev = len(output)
    print("")
    return output
    """


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=str, default=21010)
    parser.add_argument("--controller-address", type=str, default=os.environ.get("CONTROLLER_ADDRESS") or "http://localhost:21001")

    args = parser.parse_args()
    logging.info(f"Controller address: {args.controller_address}")
    logic = Logic(args)

    #uvicorn.run("backend_nat:app", host=args.host, port=args.port, log_level="info", reload=True)
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
