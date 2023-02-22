#!/bin/bash

source ./scripts/utils.sh
IMAGE_TAG=$(get_image_tag)
echo "Building image '$IMAGE_TAG'"

docker build -t $IMAGE_TAG .

