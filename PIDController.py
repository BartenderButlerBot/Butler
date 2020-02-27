from breezycreate2 import Robot
import time

# Create a Create2. This will automatically try to connect to your robot over serial
bot = Robot(port = '/dev/ttyUSB0')

# Play a note to let us know you're alive!
bot.playNote('A4', 100)

#time.sleep(7.13)
#bot.direct(30, 30)

#IR SENSOR SETUP
import RPi.GPIO as IO
import time
IO.setwarnings(False)
IO.setmode(IO.BCM)

array = [0,0,0,0,0]

IO.setup(5,IO.IN)  #GPIO 5 -> Z-ouput of IR Multiplexer
IO.setup(22,IO.OUT) #GPIO 22 -> S0
IO.setup(23,IO.OUT) #GPIO 23 -> S1
IO.setup(24,IO.OUT) #GPIO 24 -> S2

#LOAD SENSOR SETUP
import time
import sys

EMULATE_HX711=False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx = HX711(17, 18)

hx.set_reading_format("MSB", "MSB")

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

#PID Initialization
error = 0
preverror = 0
derivative = 0
integral = 0
motorchange = 0
leftms = 100
rightms = 100


#Reading Error
def readError(array):
    global error
    if array == [0, 0, 1, 0, 0]:
        error = 0
    elif array == [0, 1, 1, 0, 0]:
        error = 1
    elif array == [0, 0, 1, 1, 0]:
        error = -1
    elif array == [0, 1, 0, 0, 0]:
        error = 2
    elif array == [0, 0, 0, 1, 0]:
        error = -2
    elif array == [1, 1, 0, 0, 0]:
        error = 3
    elif array == [0, 0, 0, 1, 1]:
        error = -3
    elif array == [1, 0, 0, 0, 0]:
        error = 4
    elif array == [0, 0, 0, 0, 1]:
        error = -4
    elif array == [0, 0, 0, 0, 0]:
        if preverror == -4 or preverror == -5:
            error = -5
        elif preverror == 4 or preverror == 5:
            error = 5
    return error

def PIDCalc():
    global error
    global preverror
    global derivative
    global integral
    global motorchange
    global leftms
    global rightms
    derivative = error-preverror
    integral += error
    motorchange = (1*error) + (30*derivative) + (0.01*integral)
    leftms -= motorchange
    rightms += motorchange
    if leftms >= 500:
        leftms=500
    if leftms <= -500:
        leftms=-500
    if rightms >= 500:
        rightms=500
    if rightms <= -500:
        rightms=-500
    preverror = error

while True:
    try:
        val = hx.get_weight(17)
        if val >= 100000:
            time.sleep(1)
            if val >= 100000:
                break
        else:
            print("Waiting...")

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

bot.safe()
bot.direct(-100,-100)
time.sleep(0.5)
bot.direct(0,0)
time.sleep(0.25)

while True:

    IO.output(22,0)
    IO.output(23,0)
    IO.output(24,0)
    if(IO.input(5)==True): #LL IR senses tape
        array[0] = 1
    if(IO.input(5)==False): #LL IR does not sense tape
        array[0] = 0
        
    IO.output(22,1)
    if(IO.input(5)==True): #LM IR senses tape
        array[1] = 1
    if(IO.input(5)==False): #LM IR does not sense tape
        array[1] = 0
        
    IO.output(22,0)
    IO.output(23,1)
    if(IO.input(5)==True): #M IR senses tape
        array[2] = 1
    if(IO.input(5)==False): #M IR does not sense tape
        array[2] = 0
        
    IO.output(22,1)
    if(IO.input(5)==True): #RM IR senses tape
        array[3] = 1
    if(IO.input(5)==False): #RM IR does not sense tape
        array[3] = 0

    IO.output(22,0)
    IO.output(23,0)
    IO.output(24,1)   
    if(IO.input(5)==True): #RR IR senses tape
        array[4] = 1
    if(IO.input(5)==False): #RR IR does not sense tape
        array[4] = 0

    if array == [1,1,1,1,1]:
        bot.direct(0,0)
        time.sleep(1)
        bot.playNote('A4', 100)
        bot.direct(100, -100)
        time.sleep(1)
        bot.dock()
        break
    
    readError(array)
    PIDCalc()
    rightms = round(rightms)
    leftms = round(leftms)
    bot.direct(-leftms, -rightms)
    print(array)
    print(rightms, leftms)
