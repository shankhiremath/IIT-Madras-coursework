from time import sleep
from json import dumps
from kafka import KafkaProducer
import pandas as pd 
import json

df_test = pd.read_csv("gs://shashank_be18b006/lab7/iris.csv")
df_test['json'] = df_test.apply(lambda x: x.to_json(), axis = 1)
df_test = df_test.sample(frac = 1)
message = df_test.json.to_list()

def start_producing(message):
        producer = KafkaProducer(bootstrap_servers= ['localhost:9092'])
        for msg in message:
                producer.send('lab7-iris', json.dumps(msg).encode('utf-8'))
                producer.flush()
                print("message sent: ", msg)
                sleep(2)
start_producing(message)