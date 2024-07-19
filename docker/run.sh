#!/bin/bash

mkdir -p ./dist/

if [ ! -f dist/contentctl.yml ]; then
    echo "Couldn't find contenctl.yml, creating a base contentctl file..."
    docker run --rm -it --mount "type=bind,src=$(pwd)/dist,target=/data" contentctl init --path /data
else
    # shellcheck disable=SC2068
    docker run --rm -it --mount "type=bind,src=$(pwd)/dist,target=/data" contentctl $@
fi


