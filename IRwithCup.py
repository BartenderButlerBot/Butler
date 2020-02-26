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

    try:
        val = hx.get_weight(17)
        if val >= 100000:
            print(array)
        else:
            print("Waiting...")

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
