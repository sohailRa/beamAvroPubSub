#!/bin/bash

export PUBSUB_EMULATOR_HOST=localhost:8085

PUBSUB_PROJECT_ID=gcp-demo
python ../cloud-client/publisher.py ${PUBSUB_PROJECT_ID} publish-avro avro_input
