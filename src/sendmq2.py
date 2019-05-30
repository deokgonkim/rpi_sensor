#!/usr/bin/python
import datetime
import time

import pika

from subprocess import check_output

connection = pika.BlockingConnection(pika.ConnectionParameters('server'))
channel = connection.channel()
channel.queue_declare(queue='temperature')
channel.queue_declare(queue='humidity')

while True:
    now = datetime.datetime.now()

    line = check_output(['./test_dht11'])
    if len(line) > 0 and len(line.split('\n')) > 0:
        values = line.split('\n')[1]
        humidity, temperature = [ float(value) for value in values.split(',') ]
    else:
        humidity, temperature = (None, None)

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    if humidity is not None and temperature is not None:
        print('{} Temp={:0.1f}*C  Humidity={:0.1f}%'.format(now, temperature, humidity))
        channel.basic_publish(exchange='',
                              routing_key='temperature',
                              body='{:0.1f}'.format(temperature))
        channel.basic_publish(exchange='',
                              routing_key='humidity',
                              body='{:0.1f}'.format(humidity))
    else:
        print('Failed to get reading. Try again!')
    time.sleep(5)

connection.close()
