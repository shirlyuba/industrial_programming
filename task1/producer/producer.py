#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='my_queue')

while True:
    var = input("Enter the string: ")
    channel.basic_publish(exchange='',
                          routing_key='my_queue',
                          body=var)

connection.close()
