# create dockerignore
touch .dockerignore
echo "output_model/*" >> .dockerignore
echo ".pylintrc" >> .dockerignore
echo "tests/*" >> .dockerignore
echo "assets/*" >> .dockerignore

DOCKER_IMAGE_CONTROLLER="nielsantosa/fastchat_controller:v1"

#docker build --platform linux/amd64 -t $DOCKER_IMAGE_CONTROLLER . -f deploy_lambda/Dockerfile.controller

#docker push $DOCKER_IMAGE_CONTROLLER

#docker run --restart unless-stopped -p 21001:21001 -d --name fastchat_controller $DOCKER_IMAGE_CONTROLLER

DOCKER_IMAGE_BACKEND="nielsantosa/fastchat_backend:v1"
#docker build --platform linux/amd64 -t $DOCKER_IMAGE_BACKEND . -f deploy_lambda/Dockerfile.backend_nat

#docker push $DOCKER_IMAGE_BACKEND

#docker run --restart unless-stopped -p 21010:21010 -d --name fastchat_backend $DOCKER_IMAGE_BACKEND

# remove dockerignore
rm .dockerignore
touch .dockerignore
echo ".pylintrc" >> .dockerignore
echo "tests/*" >> .dockerignore
echo "assets/*" >> .dockerignore

DOCKER_IMAGE_WORKER="nielsantosa/fastchat_backend:v1"
docker build --platform linux/amd64 -t $DOCKER_IMAGE_WORKER . -f deploy_lambda/Dockerfile.worker

docker push $DOCKER_IMAGE_WORKER

docker run --restart unless-stopped -p 21002:21002 -d --name fastchat_worker $DOCKER_IMAGE_WORKER
