#!/usr/bin/env python
import pika
import postgresql
import time

time.sleep(25)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

db = postgresql.open('pq://docker:docker@db:5432/docker')
db.execute("DROP TABLE IF EXISTS messages;")
db.execute("CREATE TABLE messages (id SERIAL PRIMARY KEY, msg CHAR(256));")
base = db.prepare("INSERT INTO messages (msg) VALUES ($1)")

channel.queue_declare(queue='my_queue')

def callback(ch, method, properties, body):
    base(str(body))

channel.basic_consume(callback,
                      queue='my_queue',
		      no_ack=True)

channel.start_consuming()
