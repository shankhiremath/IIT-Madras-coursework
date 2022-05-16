from __future__ import print_function
from pyspark.context import SparkContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql.session import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import PCA
from pyspark.ml.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.util import MLUtils
import numpy as np
from pyspark.ml.feature import StandardScaler
import pyspark.sql.functions as f
import pyspark.sql.types
from pyspark.sql import Row
from pyspark.sql.types import DoubleType
from pyspark.ml import Pipeline
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import PCA

sc = SparkContext()
spark = SparkSession(sc)

spark_df = spark.read.format("bigquery").option("table", "iris.irisdata").load().toDF("sepal_length", "sepal_width", "petal_length", "petal_width", "class")
clean_data = spark_df.withColumn("label", spark_df["class"])

cols = spark_df.drop('class').columns
assembler = VectorAssembler(inputCols=cols, outputCol = 'features')
labelIndexer = StringIndexer(inputCol="class", outputCol="indexedLabel").fit(spark_df)

(trainingData, testData) = spark_df.randomSplit([0.8, 0.2])

##########################################################################################################
# scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures", withStd=False, withMean=True)

## Principal component analysis
# pca = PCA(k=3, inputCol='scaledFeatures', outputCol='pcaFeature')
#########################################################################################################3

## Training a RandomForest model
# rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="features", numTrees=10 )
#########################################################################################################3

## Training a Logistic Regression model
# lr = LogisticRegression(labelCol="indexedLabel", featuresCol="scaledFeatures", maxIter=10, regParam=0.3, elasticNetParam=0.8)
#########################################################################################################3

## Training a Multilayer Perceptron model
# layers = [4, 10, 10, 3]
# trainer = MultilayerPerceptronClassifier(labelCol="indexedLabel", featuresCol="features",maxIter=100, layers=layers, blockSize=128, seed=1234)

# In the case of scaler:
# trainer = MultilayerPerceptronClassifier(labelCol="indexedLabel", featuresCol="scaledFeatures",maxIter=100, layers=layers, blockSize=128, seed=1234)

# In the case of scaler and PCA:
# trainer = MultilayerPerceptronClassifier(labelCol="indexedLabel", featuresCol="pcaFeature",maxIter=100, layers=layers, blockSize=128, seed=1234)

## Retrieve orginal labels from indexed labels
labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
                               labels=labelIndexer.labels)

## Creating a Pipeline for training the data
pipeline = Pipeline(stages=[labelIndexer, assembler, rf, labelConverter])
#pipeline = Pipeline(stages=[labelIndexer, assembler, lr, labelConverter])
#pipeline = Pipeline(stages=[labelIndexer, assembler, trainer, labelConverter])
#pipeline = Pipeline(stages=[labelIndexer, assembler, scaler, trainer, labelConverter])
#pipeline = Pipeline(stages=[labelIndexer, assembler, scaler, pca, trainer, labelConverter])

## Train the ML model

model = pipeline.fit(trainingData)

## Predictions

predictions = model.transform(testData)
evaluator = MulticlassClassificationEvaluator(
    labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test set accuracy = %g" % (accuracy))
