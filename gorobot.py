#! /usr/local/bin/python3
import zmq
import math
import time

TIMEOUT = 10000

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:12346")

def tick_simulation():
    socket.send_string("tick")
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    evt = dict(poller.poll(TIMEOUT))
    if evt:
        if evt.get(socket) == zmq.POLLIN:
            response = socket.recv()  # blocking req
            print(response)  # tick_ok

def request_sensor(sensor_name : str):
    socket.send_string("sensor_" + sensor_name)
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    evt = dict(poller.poll(TIMEOUT))
    if evt:
        if evt.get(socket) == zmq.POLLIN:
            response = socket.recv()  # blocking req
            return(response)

class MockSensor():
    ''' Returns periodic data based on sensor start time
    `get_data_sin` returns a float from -1 to 1 according to a sine wave
    `get_data_bool` returns a bool, toggles every half period
    '''
    def __init__(self, period=1):
        self.time_start = time.time()
        self.period = period

    def get_data_sin(self):
        time_elapsed = time.time() - self.time_start
        sensor_data = math.sin(time_elapsed * 2 * math.pi / self.period)
        return sensor_data

    def get_data_bool(self, start_true=True):
        time_elapsed = time.time() - self.time_start
        period_time = time_elapsed % self.period
        half_period = self.period / 2.0
        sensor_data = True if period_time < half_period else False
        if not start_true: sensor_data = not sensor_data
        return sensor_data
