import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions


class MyOptions(PipelineOptions):
    """カスタムオプション."""

    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            "--input",
            default="./src/files/input.txt",
            help="Input path for the pipeline",
        )

        parser.add_argument(
            "--output",
            default="./src/files/output.txt",
            help="Output path for the pipeline",
        )


class ComputeWordLength(beam.DoFn):
    """文字数を求める変換処理."""

    def __init__(self):
        pass

    def process(self, element):
        yield len(element)


def run():
    options = MyOptions()
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

