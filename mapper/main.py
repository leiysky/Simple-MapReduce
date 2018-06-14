import numpy as np
import pika
import store as st
import os

env_dict = os.environ
worker_name = 'Mapper1'
# host = env_dict['HOST']
host = 'rabbit'

# initialize RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=host))
channel = connection.channel()
channel.queue_declare('map')
channel.queue_declare('reduce')


def run_mapping(ch, method, properties, body):
    """Callback of MQ map
    """
    id = body.decode('utf-8')
    data = st.get_data_by_id(id)
    type = kmeans_iterate(data)
    pair = str(type) + ',' + str(id)
    print('%s: %s' % (worker_name, pair))
    channel.publish(exchange='', routing_key='reduce', body=pair)


def kmeans_iterate(data):
    """Iterate kmeasn algorithm

    Args:
        data: A list of target data

    Returns:
        A number of type
    """
    vec1 = np.array(data)
    c = st.get_c(0)
    distance = np.linalg.norm(vec1 - np.array(c))
    type = 0
    for i in range(3):
        arr = st.get_c(id=i)
        vec2 = np.array(arr)
        temp = np.linalg.norm(vec2 - vec1)
        if (distance > temp):
            distance = temp
            type = i
    return type


channel.basic_consume(run_mapping, queue='map', no_ack=True)
channel.start_consuming()
