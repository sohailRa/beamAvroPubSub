#!/bin/bash
export PUBSUB_EMULATOR_HOST=localhost:8085

PUBSUB_PROJECT_ID=gcp-demo
python ../main.py \
	--input projects/${PUBSUB_PROJECT_ID}/subscriptions/avro_input_subs \
	--output projects/${PUBSUB_PROJECT_ID}/topics/avro_output \
	--runner Direct \
	--streaming