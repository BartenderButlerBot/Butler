
from breezycreate2 import Robot
import time

# Create a Create2. This will automatically try to connect to your robot over serial
bot = Robot(port = '/dev/ttyUSB0')

# Play a note to let us know you're alive!
bot.playNote('A4', 100)

#Turn on MD
bot.motordriver(127)


# Wait
#time.sleep(30)

#Stop direct
#bot.direct(0, 0)
