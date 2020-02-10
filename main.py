import apache_beam as beam
from apache_beam.io import ReadFromPubSub
from apache_beam.io import WriteToPubSub
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from fastavro import parse_schema, schemaless_reader, schemaless_writer
import argparse
import io
import datetime
import logging

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(name)s : %(message)s", level=logging.INFO
)
logging = logging.getLogger(__name__)

raw_schema = {
        "type": "record",
        "namespace": "AvroPubSubDemo",
        "name": "Entity",
        "fields": [
            {"name": "id", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "dob", "type": "string"},
        ],
    }
    

class avroReadWrite:
    def __init__(self, schema):
        self.schema = schema

    def deserialize(self, record):
        bytes_reader = io.BytesIO(record)
        dict_record = schemaless_reader(bytes_reader, self.schema)
        return dict_record

    def serialize(self, record):
        bytes_writer = io.BytesIO()
        schemaless_writer(bytes_writer, self.schema, record)
        bytes_array = bytes_writer.getvalue()
        return bytes_array


class JobOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument("--input", required=True, help="pubsub input topic")
        parser.add_argument("--output", required=True, help="pubsub outut topic")
        

class TransformerDoFn(beam.DoFn):
    def __init__(self, _schema):
        self.schema = _schema

    def process(self, record):
        try:
            logging.info("-----------------------------------------------------------")
            logging.info("Input Record: {}".format(record))
            record["dob"] = str(
                datetime.datetime.strptime(record["dob"], "%d/%m/%Y").date()
            )
            logging.info("Output Record: {}".format(record))
            logging.info("-----------------------------------------------------------")
            return [record]
        except Exception as e:
            logging.error("Got Exceptons {}", format(e), exc_info=True)
            return [record]


def run(argv=None, save_main_session=True):

    parser = argparse.ArgumentParser()
    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session
    job_options = pipeline_options.view_as(JobOptions)

    p = beam.Pipeline(options=pipeline_options)

    
    schema = parse_schema(raw_schema)

    logging.info("-----------------------------------------------------------")
    logging.info("          Dataflow AVRO Streaming with Pub/Sub             ")
    logging.info("-----------------------------------------------------------")

    avroRW = avroReadWrite(schema)
    source = ReadFromPubSub(subscription=str(job_options.input))
    sink = WriteToPubSub(str(job_options.output))
    lines = (
        p
        | "read" >> source
        | "deserialize" >> beam.Map(lambda x: avroRW.deserialize(x))
        | "process" >> (beam.ParDo(TransformerDoFn(_schema=schema)))
        | "serialize" >> beam.Map(lambda x: avroRW.serialize(x))
        | "write" >> sink
    )
    result = p.run()
    result.wait_until_finish()


if __name__ == "__main__":
    run()
