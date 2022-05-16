from kafka import KafkaConsumer
import json
import pandas as pd 
from pyspark.ml import Pipeline
from pyspark.ml.tuning import CrossValidatorModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SparkSession
from pyspark.sql.functions import split,decode,substring
from pyspark.sql.types import *
from pyspark.ml import PipelineModel

mySchema = StructType([StructField("sepal_length", FloatType(), True)\
        ,StructField("sepal_width", FloatType(), True)\
        ,StructField("petal_length", FloatType(), True)\
        ,StructField("petal_width", FloatType(), True)
        ,StructField("class", StringType(), True)])
                       
def start_consuming():
    model = PipelineModel.load('savedmodels/rf')
    print('Done loading the model.')
    
    ctr = 0
    spark = SparkSession \
        .builder \
        .appName("IrisSub") \
        .getOrCreate()

    consumer = KafkaConsumer('lab7-iris', bootstrap_servers = ['localhost:9092'])
    for msg in consumer:
        message = json.loads(msg.value)
        message = json.loads(message)
        df_line = pd.json_normalize(message)
        if ctr == 0:
            df = df_line.copy()
            df_line = spark.createDataFrame(df_line, schema=mySchema)
            df = spark.createDataFrame(df, schema=mySchema)
        else:
            df = df.toPandas()
            df = df.append(df_line, ignore_index= True)
            df_line = spark.createDataFrame(df_line, schema=mySchema)
            df = spark.createDataFrame(df, schema=mySchema)
        ctr += 1

        X = df_line[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
        prediction = model.transform(df)
        prediction = prediction.drop('sepal_length')
        prediction = prediction.drop('sepal_width')
        prediction = prediction.drop('petal_length')
        prediction = prediction.drop('petal_width')
        prediction = prediction.drop('rawPrediction')
        prediction = prediction.drop('features')
        prediction = prediction.drop('probability')
        prediction.write.format("console").save()
        
        evaluator = MulticlassClassificationEvaluator(labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
        acc = evaluator.evaluate(prediction) * 100
        batch = ctr + 1
        print("Accuracy for batch {}: ".format(batch), acc)
        print("------------------------")

start_consuming()