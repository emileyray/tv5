#!/usr/bin/env python
from time import sleep
import pika
import string
import random

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

letters = string.ascii_letters
curr_type = 1

while True:
    sleep(1)
    next_str = ''.join(random.choice(letters) for i in range(5))
    if (curr_type == 1):
        next_str = 'type1:' + next_str
        curr_type = 2
    else:
        next_str = 'type2' + next_str
        curr_type = 1

    channel.basic_publish(
        exchange='', routing_key='hello', body=next_str)
