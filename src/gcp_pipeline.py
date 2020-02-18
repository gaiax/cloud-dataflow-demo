import apache_beam as beam
from apache_beam.options.pipeline_options import (
    PipelineOptions,
    GoogleCloudOptions,
    StandardOptions,
    WorkerOptions,
)

GCP_PROJECT_ID = "cloud-dataflow-demo-268509"
GCS_BUCKET_NAME = "cloud-dataflow-demo-268509"
JOB_NAME = "compute-word-length"


class CostomOptions(PipelineOptions):
    """カスタムオプション."""

    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            "--input",
            default="gs://{}/input.txt".format(GCS_BUCKET_NAME),
            help="Input path for the pipeline",
        )

        parser.add_argument(
            "--output",
            default="gs://{}/output.txt".format(GCS_BUCKET_NAME),
            help="Output path for the pipeline",
        )


class ComputeWordLength(beam.DoFn):
    """文字数を求める変換処理."""

    def __init__(self):
        pass

    def process(self, element):
        yield len(element)


def run():
    options = CostomOptions()
    # options.view_as(StandardOptions).runner = 'DirectRunner'

    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = GCP_PROJECT_ID
    google_cloud_options.job_name = JOB_NAME
    google_cloud_options.staging_location = "gs://{}/binaries".format(GCS_BUCKET_NAME)
    google_cloud_options.temp_location = "gs://{}/temp".format(GCS_BUCKET_NAME)
    google_cloud_options.region = "asia-northeast1"

    options.view_as(WorkerOptions).autoscaling_algorithm = "THROUGHPUT_BASED"
    options.view_as(StandardOptions).runner = "DataflowRunner"

    p = beam.Pipeline(options=options)

    (
        p
        | "ReadFromText" >> beam.io.ReadFromText(options.input)
        | "ComputeWordLength" >> beam.ParDo(ComputeWordLength())
        | "WriteToText" >> beam.io.WriteToText(options.output)
    )

    p.run()


if __name__ == "__main__":
    run()
