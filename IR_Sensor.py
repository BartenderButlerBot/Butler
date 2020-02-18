import RPi.GPIO as IO
import time
IO.setwarnings(False)
IO.setmode(IO.BCM)

IO.setup(17,IO.OUT) #GPIO 17 -> Blue LED as output
IO.setup(18,IO.IN)  #GPIO 18 -> LL IR sensor as input

IO.setup(22,IO.OUT) #GPIO 22 -> Yellow LED as output
IO.setup(27,IO.IN)  #GPIO 27 -> LM IR sensor as input

IO.setup(24,IO.OUT) #GPIO 24 -> Red LED as output
IO.setup(23,IO.IN)  #GPIO 23 -> RM IR sensor as input

IO.setup(25,IO.OUT) #GPIO 25 -> Green LED as output
IO.setup(4,IO.IN)   #GPIO 4  -> RR IR sensor as input

while 1:

    if(IO.input(18)==True): #LL IR senses tape
        IO.output(17,True)  #Blue led ON
        
    
    if(IO.input(18)==False): #LL IR does not sense tape
        IO.output(17,False)  #Blue led OFF


    if(IO.input(27)==True): #LM IR senses tape
        IO.output(22,True)  #Yellow led ON

    
    if(IO.input(27)==False): #LM IR does not sense tape
        IO.output(22,False)  #Yellow led OFF



    if(IO.input(23)==True): #RM IR senses tape
        IO.output(24,True)  #Red led ON

    
    if(IO.input(23)==False): #RM IR does not sense tape
        IO.output(24,False)  #Red led OFF


    if(IO.input(4)==True): #RR IR senses tape
        IO.output(25,True) #Green led ON

    
    if(IO.input(4)==False): #RR IR does not sense tape
        IO.output(25,False) #Green led OFF
