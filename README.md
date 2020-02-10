# beamAvroPubSub
This project demonstrated a simple Python Beam Streaming Pipeline for AVRO records. Details on the project can be found on the Medium Post "Apache Beam: AVRO streaming using Pub/Sub in Python".

The project uses Google Pub/Sub emulator with slight modification in the "cloud-client" library. The emulator can be started along with the required topic names and subscriptions by invoking the right scripts from the bin directory.

To start the Pub/Sub emulator cd to bin directory and run
```
./run.sh
```
To initialize the Pub/Sub run the following scripts
```
start_pubsub_emulator.sh
create_topics_subs.sh
custom_consumer.sh
custom_publisher.sh
```
And, once you are done. Kill the consumer and the streaming application by pressing CTRL+C and invoke the cleanup script from the bin directory
```
cleanup.sh
```