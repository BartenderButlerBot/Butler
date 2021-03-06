import RPi.GPIO as IO
import time
IO.setwarnings(False)
IO.setmode(IO.BCM)

array = [0,0,0,0]

IO.setup(5,IO.IN)  #GPIO 5 -> Z-ouput of IR Multiplexer
IO.setup(22,IO.OUT) #GPIO 22 -> S0
IO.setup(23,IO.OUT) #GPIO 23 -> S1

while 1:

    IO.output(22,0)
    IO.output(23,0)
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
    if(IO.input(5)==True): #RM IR senses tape
        array[2] = 1
    if(IO.input(5)==False): #RM IR does not sense tape
        array[2] = 0
        
    IO.output(22,1)
    if(IO.input(5)==True): #RR IR senses tape
        array[3] = 1
    if(IO.input(5)==False): #RR IR does not sense tape
        array[3] = 0
        
    print(array)
