import serial, sys

port = "COM4"
print("Trying " + str(port) + "... ")

START = '128'
SAFE = '131'
FULL = '132'
LED = '139 4 255 255'

LED1  = '139' 
LED2  = '4'
LED3  = '255'

BEEP1 = '140 3 1'
BEEP2 = '3 1 64 16'
PLAY = '141 3'

try:
    connection = serial.Serial(port, baudrate=115200, timeout=1)
    print("Connected!")

    command = bytes(START, 'ascii')
    print(command)

    connection.write(command)
    
    command = bytes(FULL, 'ascii')
    print(command)

    connection.write(command)

    command = bytes(LED, 'ascii')
    print(command)

    connection.write(command)

    
except Exception as e:
    sys.stderr.write("COM connection error: {0}".format(e))

connection.close()
print("Success!")
