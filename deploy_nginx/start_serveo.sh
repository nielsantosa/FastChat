#!/bin/bash

# To run serveo tunnel to expose localhost:21010 (backend_nat) to public internet
# To enable custom domain (in this case 99llmmodel.serveo.net), need to add ssh-key first
# ServerAliveInterval is to enable the max time (in seconds) the connection can be alive
# More info : https://serveo.net/

ssh -o ServerAliveInterval=60 -R 99llmmodel.serveo.net:80:localhost:21010 serveo.net
