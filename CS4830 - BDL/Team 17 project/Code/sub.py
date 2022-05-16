from pyspark import SparkContext, SQLContext
from itertools import chain
from pyspark.ml import PipelineModel, Pipeline
import pyspark
import pyspark.sql.functions as f
from pyspark.sql.types import *
from pyspark.ml.tuning import CrossValidatorModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, decode, substring
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql.functions import from_json, udf, split
from kafka import KafkaConsumer
import json
import pandas as pd
from sparknlp import *
print(pyspark.__version__)

myschema = StructType([StructField('id1', StringType(), True),
               StructField('ufc1', FloatType(), True),
               StructField('date', StringType(), True),
               StructField('ufc2', FloatType(), True),
               StructField('id2', StringType(), True),
               StructField('stars', FloatType(), True),
               StructField('text', StringType(), True),
               StructField('ufc3', FloatType(), True),
               StructField('id3', StringType(), True)])

def start_consuming():
    spark = SparkSession \
        .builder \
        .appName("YelpSub") \
        .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:3.4.4")\
        .getOrCreate()
    
    model = PipelineModel.load('LogReg_TFIDF_model_final')
    print('Done loading the model.')
    
    ctr = 0
    print('Spark session active.')
    consumer = KafkaConsumer('yelp-nlp', bootstrap_servers = ['localhost:9092'])
    for msg in consumer:
        message = json.loads(msg.value)
        df_line = pd.json_normalize(message)
        if ctr == 0:
            df = df_line.copy()
            df_line = spark.createDataFrame(df_line, schema = myschema)
            df = spark.createDataFrame(df, schema = myschema)
        else:
            df = df.toPandas()
            df = df.append(df_line, ignore_index= True)
            df_line = spark.createDataFrame(df_line, schema = myschema)
            df = spark.createDataFrame(df, schema = myschema)
        ctr += 1

        prediction = model.transform(df)
        prediction = prediction.select(['stars', 'prediction'])
        prediction.write.format("console").save()
        output_df = prediction.withColumn("correct", f.when((f.col('prediction')==1.0) & (f.col('stars')==1.0),1).when((f.col('prediction')==2.0) & (f.col('stars')==2.0),1).when((f.col('prediction')==3.0) & (f.col('stars')==3.0),1).when((f.col('prediction')==4.0) & (f.col('stars')==4.0),1).when((f.col('prediction')==5.0) & (f.col('stars')==5.0),1).otherwise(0))

        f1_eval = MulticlassClassificationEvaluator(labelCol="stars", predictionCol="prediction", metricName='f1')
        evaluator = MulticlassClassificationEvaluator(labelCol="stars", predictionCol="prediction", metricName="accuracy")
        acc = evaluator.evaluate(prediction) * 100
        f1 = f1_eval.evaluate(prediction)
        batch = ctr + 1
        print("Accuracy and F1-score for batch {}: ".format(batch), acc, f1)
        print("------------------------")

start_consuming()
