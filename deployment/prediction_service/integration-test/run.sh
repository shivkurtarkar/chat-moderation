#!/usr/bin/env bash

cd "$(dirname "$0")"

# LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
# export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"
# docker build -t ${LOCAL_IMAGE_NAME} ..

# python -m pipenv run python test_deployment.py

python test_deployment.py
ERROR_CODE=$?

exit ${ERROR_CODE}
