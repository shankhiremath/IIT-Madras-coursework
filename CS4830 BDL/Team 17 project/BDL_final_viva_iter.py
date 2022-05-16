# The below import statements allow us to access SparkML features specific to logistic
# regression as well as the Vectors types.
from __future__ import print_function
from pyspark.context import SparkContext
from pyspark.ml.linalg import Vectors
from pyspark.sql.session import SparkSession
from pyspark.sql.types import *
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from sparknlp.annotator import Lemmatizer, Stemmer, Tokenizer, Normalizer
from sparknlp.base import DocumentAssembler, Finisher
from pyspark.ml.feature import StopWordsRemover, CountVectorizer, IDF

sc = SparkContext()
spark = (SparkSession.builder.config("spark.jars.packages","com.johnsnowlabs:spark-nlp_2.12:3.0.3").getOrCreate())

# Read the data from BigQuery as a Spark Dataframe using the specified schema.
data_schema = StructType([StructField('id1', StringType(), True),
               StructField('ufc1', FloatType(), True),
               StructField('date', StringType(), True),
               StructField('ufc2', FloatType(), True),
               StructField('id2', StringType(), True),
               StructField('stars', FloatType(), True),
               StructField('text', StringType(), True),
               StructField('ufc3', FloatType(), True),
               StructField('id3', StringType(), True)])

yelp_dataset = spark.read.format("csv").schema(data_schema)\
.option("mode", "DROPMALFORMED")\
.option("quote", "\"")\
.option("multiline", "true")\
.option("escape", "\"")\
.load("gs://bdl2022/YELP_train.csv")

print('\n')
yelp_dataset = yelp_dataset.filter("ufc1 is NOT NULL AND ufc2 is NOT NULL AND ufc3 is NOT NULL AND stars is NOT NULL")
print('The final Yelp dataset has ' + str(yelp_dataset.count()) + ' rows.')
yelp_dataset.printSchema()

# Create a view so that Spark SQL queries can be run against the data.
yelp_dataset.createOrReplaceTempView("yelp")

# Define the train and test split on the data
training_data, test_data = yelp_dataset.randomSplit([0.85, 0.15], seed = 42)
print('Train test split (85 - 15) done.')

#Save the test dataset
# test_data.write.json("gs://shank_bdl/yelp-test-final/test_yelp_dataset")
# print('Test data saved.')

# Create the pipeline
document_assembler = DocumentAssembler().setInputCol("text").setOutputCol("document")
tokenizer = Tokenizer().setInputCols(["document"]).setOutputCol("token")
normalizer = Normalizer().setInputCols(["token"]).setOutputCol("normalizer")
stemmer = Stemmer().setInputCols(["normalizer"]).setOutputCol("stem")
finisher = Finisher().setInputCols(["stem"]).setOutputCols(["to_spark"]).setValueSplitSymbol(" ")
stopword_remover = StopWordsRemover(inputCol = "to_spark", outputCol = "filtered")
tf = CountVectorizer(inputCol = "filtered", outputCol = "raw_features")
idf = IDF(inputCol = "raw_features", outputCol = "features")

lr = LogisticRegression(featuresCol = 'features', labelCol = 'stars', maxIter = 15)

pipe = Pipeline(
	stages = [document_assembler, tokenizer, normalizer, stemmer, finisher, stopword_remover, tf, idf, lr]
)

print("Fitting the model to the data")
lr_model = pipe.fit(training_data)
print('Training done.')

# Saving the model
try:
	lr_model.save("gs://shank_bdl/LogReg_TFIDF_model_viva_iter")
except:
	model = lr_model.stages[2]
	print(model)
	model.save("gs://shank_bdl/LogReg_TFIDF_model_viva_iter")

print("Saving model done.")

# define the evaluators
lr_evaluator = MulticlassClassificationEvaluator(predictionCol = "prediction", 
                                  labelCol = "stars", metricName = "accuracy")

lr_evaluator_f1 = MulticlassClassificationEvaluator(predictionCol = "prediction", 
                                  labelCol = "stars", metricName = "f1")

# training prediction
prediction_train = lr_model.transform(training_data)
print('Transforming training data done.')
prediction_train.select("prediction", "stars", "features").show(5)
print("Evaluating on Training data to see accuracy:", lr_evaluator.evaluate(prediction_train))
print("Evaluating on Training data to see F1 score:", lr_evaluator_f1.evaluate(prediction_train))

# test prediction
prediction_test = lr_model.transform(test_data)
print('Transforming test data done.')

prediction_test.select("prediction", "stars", "features").show(5)

# evaluating the test score
print("Evaluating on Test data to see accuracy:", lr_evaluator.evaluate(prediction_test))
print("Evaluating on Test data to see F1 score:", lr_evaluator_f1.evaluate(prediction_test))
