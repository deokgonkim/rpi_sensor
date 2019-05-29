#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
import Queue

import datetime
import random
import threading
import time

import Adafruit_DHT



class TempChart(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Temp Chart')

        self.lbl_title = tk.Label(self, text='Temperature Chart')
        self.lbl_title.pack(expand='yes', fill='both')

        self.chart = Chart(self)
        self.chart.pack(expand='yes', fill='both')

        self.bind('<Control-q>', self.terminate)

        self.protocol('WM_DELETE_WINDOW', self.terminate)

        self.queue = Queue.Queue()

        self.measure = TemperatureMeasure()
        self.measure.set_queue(self.queue)
        self.measure.setDaemon(True)
        self.measure.start()

        self.after(100, self.process_queue)

    def terminate(self, event=None):
        print('Program terminating')
        self.measure.stop()
        self.destroy()

    def process_queue(self):

        try:
            item = self.queue.get_nowait()
            print('Got queue item : {}'.format(item))
            self.chart.chart_item(item)
        except Queue.Empty, e:
            #print('empty')
            pass

        self.after(100, self.process_queue)


class Chart(tk.Canvas):
    START_X = 40
    START_Y = 800 - 40
    
    WIDTH = 1024-40 # 984
    HEIGHT = 800-40 - 40# 720

    X_COUNT = 50
    Y_COUNT = 40

    X_DELTA = WIDTH / X_COUNT
    Y_DELTA = HEIGHT / Y_COUNT

    def __init__(self, parent):
        tk.Canvas.__init__(self, parent)

        self.configure(width=1024, height=800)

        
        self.x = 0

        self.items = [None] * Chart.X_COUNT

        self.draw_x_axes()

    def chart_item(self, y):
        if self.x == Chart.X_COUNT:
            self.x = 0

        print('{} - {}'.format(self.x, self.items[self.x]))

        if self.items[self.x]:
            line, lbl = self.items[self.x]
            self.delete(line)
            #self.delete(lbl)
            lbl.destroy()
            self.items[self.x] = (None, None)
            
        coord_x_begin, coord_y_begin = Chart.convert(self.x, 0)
        coord_x_end, coord_y_end = Chart.convert(self.x, y)
        line = self.create_line(coord_x_begin,
                                coord_y_begin,
                                coord_x_end,
                                coord_y_end, width=5)

        lbl = tk.Label(self, text='{:02}'.format(y))
        lbl.place(x=coord_x_end - 11, y=coord_y_end - 20)

        self.items[self.x] = (line, lbl)
        self.x += 1

    @staticmethod
    def convert(x, y):
        coord_x = Chart.START_X + (Chart.X_DELTA*x)
        coord_y = Chart.START_Y - (Chart.Y_DELTA*y)
        return (coord_x, coord_y)
        

    def draw_x_axes(self):
        lbl = tk.Label(self, text='0')
        lbl.place(x=10, y=10)
        pass


class TemperatureMeasure(threading.Thread):

    def __init__(self):
        super(TemperatureMeasure, self).__init__()
        self.sensor = Adafruit_DHT.DHT11
        self.pin = 4
        self.running = True

    def set_queue(self, queue):
        self.queue = queue

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            #print('running')
            now = datetime.datetime.now()
            invalid = True
            while invalid:
                humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

                if humidity is not None and temperature is not None:
                    print('{} Temp={:0.1f}*C  Humidity={:0.1f}%'.format(now, temperature, humidity))
                    invalid = False
                
            self.queue.put(int(temperature))
            time.sleep(30)


if __name__ == '__main__':
    app = TempChart()
    app.mainloop()
