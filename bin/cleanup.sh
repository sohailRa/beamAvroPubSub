#!/bin/bash

export PUBSUB_EMULATOR_HOST=localhost:8085

PUBSUB_PROJECT_ID=gcp-demo
python ../cloud-client/publisher.py ${PUBSUB_PROJECT_ID} delete avro_input
python ../cloud-client/publisher.py ${PUBSUB_PROJECT_ID} delete avro_output

python ../cloud-client/subscriber.py ${PUBSUB_PROJECT_ID} delete avro_input_subs
python ../cloud-client/subscriber.py ${PUBSUB_PROJECT_ID} delete avro_output_subs

