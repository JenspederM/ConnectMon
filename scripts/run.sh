#!/bin/bash

source ./scripts/utils.sh
IMAGE_TAG=$(get_image_tag)
echo "Running image '$IMAGE_TAG'"

docker run --network="host" --rm --env-file=.env.local -v /Users/jenspedermeldgaard/dev/ConnectMon/conf:/conf $IMAGE_TAG