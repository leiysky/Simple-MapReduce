#!/usr/local/bin python3
#coding: utf-8
import pika
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import store
from random import randint

dataset = pd.read_csv('dataset/data.csv')
x = dataset.iloc[:, [0, 1, 2, 3]].values
store.r.set('maxnum', '150')

# initialize the center
for i in range(3):
    store.set_c(i, x[randint(0,49)])
count = 0

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='map')
channel.queue_declare(queue='result')

def publish():
    for i in x:
        i = list(map(str, i))
        i = ','.join(i)
        channel.publish(exchange='', routing_key='map', body=store.store_data_by_id(i))


def run_iterate(ch, method, properties, body):
    global count
    count+=1
    if (count > 10):
        return
    print('Iterate for %d times'%count)
    for i in range(3):
        idlist = store.get_by_key('type'+str(i))
        sum = np.array([0.0,0.0,0.0,0.0])
        for j in idlist:
            sum += np.array(store.get_data_by_id(j))
        if idlist.__len__() == 0:
            continue
        sum = sum / idlist.__len__()
        store.set_c(id=i, data=sum)
    publish()

publish()

channel.basic_consume(run_iterate, queue='result', no_ack=True)
channel.start_consuming()
