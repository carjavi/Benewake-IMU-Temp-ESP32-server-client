import serial.tools.list_ports
import time
import numpy as np

ser = serial.Serial()
ser.port = '/dev/ttyUSB1'
ser.baudrate = 115200

def getTFminiData():
    while True:
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)
            #print('get data from serial port:',recv)
            ser.reset_input_buffer()
            if recv[0] == 0x59 and recv[1] == 0x59: #python3
                distance = np.int16(recv[2] + np.int16(recv[3]<<8))
                print('distance = %5d' % (distance))
                ser.reset_input_buffer()
        else:
            time.sleep(0.050) # 50ms

if __name__ == "__main__":
    try:
        if ser.is_open == False:
            try:
                ser.open()
            except:
                print('Open COM failed')
        getTFminiData()
    except KeyboardInterrupt: # Ctrl + C
        print('Interrupted, pressed ctrl-c button')
        if ser != None:
            ser.close()