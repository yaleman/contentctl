#!/bin/bash

if [ ! -f contentctl.yml ]; then
    echo "Couldn't find contenctl.yml, creating a base contentctl file..."
    pause
    docker run --rm -it --mount "type=bind,src=$(pwd),target=/data" contentctl init --path /data
else
    # shellcheck disable=SC2068
    docker run --rm -it --mount "type=bind,src=$(pwd),target=/data" contentctl $@
fi


