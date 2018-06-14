#!/usr/local/bin python3
#coding: utf-8
import store
import pika
import logging
import os

# initialize logger
logger = logging.getLogger('mapreduce')
logger.addHandler(logging.FileHandler('/var/log/result', 'a'))
logger.setLevel(logging.INFO)
# initialize RabbitMQ
mq_host = os.environ['MQ_HOST']
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=mq_host))
channel = connection.channel()
channel.queue_declare(queue='reduce')
channel.queue_declare(queue='result')

# initialize reducer
# {'0': ['1'] } means that type 0 has a member 1
result = {}
for i in range(3):
    result[str(i)] = []
count = 0


def run_reducing(ch, method, properties, body):
    """ Callback of MQ reduce
    """
    global result
    global count
    pair = body.decode('utf-8').split(',')
    result[pair[0]].append(pair[1])
    append_by_type(pair[0], pair[1])
    count+=1
    mod = int(store.r.get('maxnum'))
    if ((count+1)%mod==0):
        count = 0
        logger.info('Classify result is:')
        logger.info('C0: ' + str(store.get_c(0)))
        logger.info('C1: ' + str(store.get_c(1)))
        logger.info('C2: ' + str(store.get_c(2)))
        logger.info('type0: %d' % result['0'].__len__())
        logger.info('type1: %d' % result['1'].__len__())
        logger.info('type2: %d' % result['2'].__len__())
        result = {}
        for i in range(3):
            result[str(i)] = []
        channel.publish(exchange='', routing_key='result', body='complete')
    


def append_by_type(type, value):
    st = store.r
    st.rpush('type'+type, value)

channel.basic_consume(run_reducing, queue='reduce', no_ack=True)

channel.start_consuming()
