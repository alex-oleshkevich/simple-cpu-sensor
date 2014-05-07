from __future__ import print_function

class Logger:
    def __init__(self):
        self.handler = open('/tmp/simple-cpu-sensor.log', 'w+')
    
    def log(self, message):
        self.handler.write(message + "\n")
        