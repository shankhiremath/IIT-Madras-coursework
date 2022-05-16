import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions

input_file = 'gs://bdl2022/lines_big.txt'
outputpath = 'gs://shashankbe18b006/linecounts'

beam_options = PipelineOptions(runner='DataflowRunner', project='steady-service-340904', job_name='linecountjob2',
    temp_location='gs://shashankbe18b006/tmp', region='us-central1')

with beam.Pipeline(options=beam_options) as p:
    # Read the text file into a PCollection.
    lines = p | ReadFromText(input_file)

    # Count the number of elements in the PCollection.
    countarray = (lines | 'Count the elements in PCollection' >> beam.combiners.Count.Globally())

    def formatresult(numlines):
        return 'Number of lines in the given input file is: %s' % (numlines)
    
    output = countarray | 'Format result' >> beam.Map(formatresult)
    output | WriteToText(outputpath)
