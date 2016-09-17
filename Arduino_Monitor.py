"""
Listen to serial, return most recent numeric values
Lots of help from here:
http://stackoverflow.com/questions/1093598/pyserial-how-to-read-last-line-sent-from-serial-device
"""
from threading import Thread
import time
import serial

last_received = ''


def receiving(ser):
    global last_received
    buffer = ''
    while True:
        buffer = buffer + ser.read(ser.inWaiting())
        if '\n' in buffer:
            lines = buffer.split('\n')  # Guaranteed to have at least 2 entries
            last_received = lines[-2]
            # If the Arduino sends lots of empty lines, you'll lose the last
            # filled line, so you could make the above statement conditional
            # like so: if lines[-2]: last_received = lines[-2]
            buffer = lines[-1]


class SerialData(object):
    def __init__(self, port, **kwargs):

        baudrate = kwargs.get('baudrate', 9600)
        timeout = kwargs.get('timeout', 0.1)

        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=timeout,
                xonxoff=0,
                rtscts=0,
                interCharTimeout=None
            )
        except serial.serialutil.SerialException:
            # no serial connection
            self.ser = None
        else:
            Thread(target=receiving, args=(self.ser,)).start()

    def next(self):
        if not self.ser:
            # return anything so we can test when Arduino isn't connected
            return 100
        # return a float value or try a few times until we get one
        for i in range(40):
            raw_line = last_received
            try:
                return float(raw_line.strip())
            except ValueError:
                print 'bogus data', raw_line
                time.sleep(.005)
        return 0.

    def __del__(self):
        if self.ser:
            self.ser.close()


if __name__ == '__main__':
    s = SerialData('com4')
    for i in range(500):
        time.sleep(.015)
        print s.next()
