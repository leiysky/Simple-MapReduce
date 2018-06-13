#!/usr/local/bin python3
#coding: utf-8

import redis

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
if(r.get('myid') == None):
    r.set('myid', 0)


def set_c(id=1, data=[]):
    r.delete('c'+str(id))
    for i in data:
        r.rpush('c'+str(id), i)


def get_by_key(key):
    l = []
    for i in range(r.llen(key)):
        l.append(r.lindex(key, i))
    # l = list(map(float, l))
    return l


def get_c(id=1):
    l = []
    name = 'c' + str(id)
    for i in range(r.llen(name)):
        l.append(r.lindex(name, i))
    l = list(map(float, l))
    return l


def store_data_by_id(data=''):
    """ A function to bind an id with a set of data which could be a list

    Args:
        data: A string object
            for example "1,2,3,4"
    Returns:
        A string of generated id
    """
    id = generate_id()
    r.delete(id)
    r.set(id, data)
    return id


def get_data_by_id(id):
    """ A function to get a set of data by id from redis

    Args:
        id: A string
    Returns:
        A list stores the data set with the corresponding id
    """
    data = r.get(id)
    data = list(map(float, data.split(',')))
    return data


def generate_id():
    """ Generate an unique id

    Based on the atomicity
    
    Returns:
        A unique key
    """
    r.incr('myid')
    return r.get('myid')


