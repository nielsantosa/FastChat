# create dockerignore
touch .dockerignore
echo "output_model/*" >> .dockerignore
echo ".pylintrc" >> .dockerignore
echo "tests/*" >> .dockerignore
echo "assets/*" >> .dockerignore

DOCKER_IMAGE_CONTROLLER="nielsantosa/fastchat_controller:v1"

#docker build --platform linux/amd64 -t $DOCKER_IMAGE_CONTROLLER . -f deploy_app/Dockerfile.controller

#docker push $DOCKER_IMAGE_CONTROLLER

#docker run --restart unless-stopped -p 21001:21001 -d --name fastchat_controller $DOCKER_IMAGE_CONTROLLER

DOCKER_IMAGE_BACKEND="nielsantosa/fastchat_backend:v1"
#docker build --platform linux/amd64 -t $DOCKER_IMAGE_BACKEND . -f deploy_app/Dockerfile.backend_nat

#docker push $DOCKER_IMAGE_BACKEND

#docker run --restart unless-stopped -p 21010:21010 -d --name fastchat_backend $DOCKER_IMAGE_BACKEND

DOCKER_IMAGE_WORKER="nielsantosa/fastchat_worker:v1"
#docker build --platform linux/amd64 -t $DOCKER_IMAGE_WORKER . -f deploy_app/Dockerfile.worker

#docker push $DOCKER_IMAGE_WORKER

NVIDIA_SMI=$(nvidia-smi)
if [ "command not found" == *"$NVIDIA_SMI"* ];
then
  # for non cuda enabled aka cpu only
  echo "Creating non gpu worker"
  sudo docker run --restart unless-stopped -p 21002:21002 -d --name fastchat_worker $DOCKER_IMAGE_WORKER;
else
  # for gpu cuda enabled
  echo "Creating gpu worker"
  sudo docker run --gpus 1 --restart unless-stopped -p 21002:21002 -d --name fastchat_worker $DOCKER_IMAGE_WORKER;
fi
