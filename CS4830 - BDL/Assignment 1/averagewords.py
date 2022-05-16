import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions

input_file = 'gs://bdl2022/lines_big.txt'
outputpath = 'gs://shashankbe18b006/averagewords'

beam_options = PipelineOptions(runner='DataflowRunner', project='steady-service-340904', job_name='averagewordsjob2',
    temp_location='gs://shashankbe18b006/tmp', region='us-central1')

with beam.Pipeline(options=beam_options) as p:
    # Read the text file into a PCollection.
    class WordCount(beam.DoFn):
        def process(self, element):
            # returns a PCollection where each element is number of words in the line
            wordsarray = element.split(" ")
            return [len(wordsarray)]

    wordcounts = (p | ReadFromText(input_file) | 'Split Words and Count' >> beam.ParDo(WordCount()))

    word_mean = (wordcounts | 'Calculating the mean' >> beam.combiners.Mean.Globally())
    
    def formatresult(word_mean):
        return 'The average number of words per line in the input file is: %s' % word_mean

    output = word_mean | 'Format result' >> beam.Map(formatresult)
    output | WriteToText(outputpath)
