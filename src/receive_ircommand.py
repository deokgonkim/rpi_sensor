#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Receive ircommand from RabbitMQ 'ircommand'
and send IR signal to AC.
using irsend command.
"""

import logging
import pika
import threading


# Enable logging
logging.basicConfig(level=logging.INFO)


class IrCommand(threading.Thread):
    """
    Receive command form RabbitMQ
    """
    device = 'lgac.conf'

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
            result = self.irsend(self.device, 'power-on')
        elif body == 'ac-off':
            result = self.irsend(self.device, 'power-offs')
        elif body == 'temp-26':
            result = self.irsend(self.device, 'temperature-26')
        else:
            result = 'Not supported command'

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                         body=result)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def irsend(self, device, key):
        import subprocess
        result = None
        try:
            result = subprocess.check_output(['irsend', 'SEND_ONCE', device, key])
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
