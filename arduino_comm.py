import serial
import serial.tools.list_ports
import struct


class ArduinoComm:
    def __init__(self, portName=None):
        if portName is not None:
            self.portName = portName
        else:
            self.portName = getDefaultPortName()

        print('Using serial communcation port: '  + self.portName)
        self.initComm()

    def initComm(self):
        try:
            self.connection = serial.Serial(self.portName)
        except serial.serialutil.SerialException:
            print('Problems connecting to the serial port - is there another connection talking '
                    'to the arduino (e.g. Serial Monitor)?')
            raise

    def sendShaftSetting(self, shaft, setting):
        print('Setting shaft %i to setting %i.' % (shaft, setting))
        self.connection.write(struct.pack('>BB', shaft, setting))

def getDefaultPortName():
    ports = list(serial.tools.list_ports.comports())
    arduinos = [port for port in ports if 'Arduino' in port[1]]

    if not arduinos:
        # hacky fall-back for my mac because names are showing as 'n/a'
        arduinos = [port for port in ports if 'usbmodem' in port[0]]

    assert arduinos, "No arduino found to connect to"
    return arduinos[0][0]


if __name__ == '__main__':
    serialComm = ArduinoComm()
    while(1):
        try:
            shaft, setting = map(int, raw_input('Shaft and setting pair (e.g. "2 0"):').split())
            serialComm.sendShaftSetting(shaft, setting)

        except ValueError:
            print 'Not a number'
