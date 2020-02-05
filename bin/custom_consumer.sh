#!/bin/bash

export PUBSUB_EMULATOR_HOST=localhost:8085

PUBSUB_PROJECT_ID=gcp-demo
python ../cloud-client/subscriber.py ${PUBSUB_PROJECT_ID} receive-avro avro_output_subs