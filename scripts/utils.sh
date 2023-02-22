#/bin/bash

# A function to get the current version from pyproject.toml
function get_image_tag() {
    IMAGE_NAME=$(cat ./pyproject.toml | grep name | cut -d '"' -f 2)
    IMAGE_VERSION=$(cat ./pyproject.toml | grep version | cut -d '"' -f 2)
    echo "$IMAGE_NAME:$IMAGE_VERSION"
}