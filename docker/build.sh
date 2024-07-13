#!/bin/bash

docker buildx build -t contentctl -f docker/Dockerfile  --load .