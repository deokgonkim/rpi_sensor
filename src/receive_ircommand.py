#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Receive ircommand from RabbitMQ 'ircommand'
and send IR signal to AC.
using ir-ctl command.
"""

import logging
import pika
import threading
import os


# Enable logging
logging.basicConfig(level=logging.INFO)


class IrCommand(threading.Thread):
    """
    Receive command form RabbitMQ
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw_code', 'lgac')

    def __init__(self, *args, **kwargs):
        super(IrCommand, self).__init__(group=None, target=None, name=None, verbose=None, *args, **kwargs)
        self.setDaemon(False)

    def run(self):
        logging.info('Starting MQ consuming channel')
        self.conn = pika.BlockingConnection(pika.ConnectionParameters('server'))
        self.channel = self.conn.channel()

        self.channel.queue_declare(queue='ircommand')

        self.channel.basic_consume(queue='ircommand',
                                   auto_ack=False,
                                   on_message_callback=self.receive_mqmessage)

        self.channel.start_consuming()

    def receive_mqmessage(self, ch, method, props, body):
        logging.info(ch)
        logging.info(method)
        logging.info(props)
        logging.info(body)

        logging.info('reply_to - {}'.format(props.reply_to))
        logging.info('correlation_id - {}'.format(props.correlation_id))

        result = None
        if body == 'ac-on':
            result = self.irctl('power-on')
        elif body == 'ac-off':
            result = self.irctl('power-off')
        elif body == 'jet-on':
            result = self.irctl('jet-on')
        elif body == 'jet-off':
            result = self.irctl('jet-off')
        elif body == 'temp-18':
            result = self.irctl('temperature-18')
        elif body == 'temp-19':
            result = self.irctl('temperature-19')
        elif body == 'temp-20':
            result = self.irctl('temperature-20')
        elif body == 'temp-21':
            result = self.irctl('temperature-21')
        elif body == 'temp-22':
            result = self.irctl('temperature-22')
        elif body == 'temp-23':
            result = self.irctl('temperature-23')
        elif body == 'temp-24':
            result = self.irctl('temperature-24')
        elif body == 'temp-25':
            result = self.irctl('temperature-25')
        elif body == 'temp-26':
            result = self.irctl('temperature-26')
        elif body == 'temp-27':
            result = self.irctl('temperature-27')
        elif body == 'temp-28':
            result = self.irctl('temperature-28')
        elif body == 'temp-29':
            result = self.irctl('temperature-29')
        elif body == 'temp-30':
            result = self.irctl('temperature-30')
        else:
            result = 'Not supported command'

        if props.reply_to:
            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id = \
                                                             props.correlation_id),
                             body=result)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def irctl(self, key):
        import subprocess
        result = None
        try:
            result = subprocess.check_output(['ir-ctl', '-s', '{}/{}'.format(self.path, key)])
        except subprocess.CalledProcessError, e:
            result = 'error_code - {}\n{}'.format(e.returncode, e.output)
        except Exception, e:
            logging.error(e, exc_info=True)
            result = str(e)

        return 'Ok' if result == '' else result

if __name__ == '__main__':
    app = IrCommand()
    app.setDaemon(True)
    app.start()
    while True:
        import time
        time.sleep(1)
