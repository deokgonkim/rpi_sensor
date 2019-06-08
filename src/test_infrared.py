#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 적외선 인체 물체감시 센서 테스트

import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


PIN = 14

GPIO.setup(PIN, GPIO.IN)

while True:
    status = GPIO.input(PIN)
    print('Status - {}'.format(status))
    time.sleep(1)
