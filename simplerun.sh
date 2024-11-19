#!/usr/bin/env bash

input_image_path=$1
output_path=$2

# if no arguments are provided, show help
if [ -z "$input_image_path" ]; then
    echo "Usage: ./test.sh <input_image_path> <output_path>"
    exit 1
fi

# if no output path is provided, use the default output path
if [ -z "$output_path" ]; then
    output_path="output/"
fi
# if no input path show error
if [ -z "$input_image_path" ]; then
    echo "Please provide the input image path"
    exit 1
fi

docker run -i -t --gpus all \
    -v "./database:/workspace/instantmesh/database" \
    -v "/data/models/instantmesh:/workspace/instantmesh/ckpts" \
    instantmesh \
    "${input_image_path}" \
    --output_path="${output_path}"
