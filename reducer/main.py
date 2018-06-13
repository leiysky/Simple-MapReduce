#!/usr/local/bin python3
#coding: utf-8
import store
import pika

# initialize RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
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
        result = {}
        for i in range(3):
            result[str(i)] = []
        channel.publish(exchange='', routing_key='result', body='complete')
    print('0: %d' % result['0'].__len__())
    print('1: %d' % result['1'].__len__())
    print('2: %d' % result['2'].__len__())


def append_by_type(type, value):
    st = store.r
    st.rpush('type'+type, value)

channel.basic_consume(run_reducing, queue='reduce', no_ack=True)

channel.start_consuming()
