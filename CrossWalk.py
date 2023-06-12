#Import Modules
import RPi.GPIO as GPIO
from time import sleep
#Import OS system Module
import sys
#Append the path to the location where the LCD1602.py is stored
sys.path.append('/home/es2800/Code')


#Import the LCD1602 module
import LCD1602 as lcd

#Initialize the two lists with the GPIO Pins of the two traffic lights
trl_west = [6,13,19]
trl_east = [16,20,21]
#Define two variable to store the GPIO Pin numbers of the two Pushbuttons
btn_south = 27
btn_north = 12

"""Boolean variable to indicate a Pedestrian
has requested crossing"""
ped_cross = False
"""Boolean variable to indicate a Normal Traffic Operation
(No Pedestrian Crossing)"""
norm_traffic = False

#Write a single statement to initialize the LCD with the I2C slave address and backlight
#init(address,backlight), default address = 0x27 for LCD screen, 1 => true=1=on false=0=off
lcd.init(0x27,1)
#Write a single statement to clear the message on the LCD
lcd.clear()
#Write two statements post message 'Starting Simulations' on two lines on the LCD
lcd.write(0,0,'Starting')
lcd.write(0,1,'Simulations')
#need  to display this for a few seconds and then clear the screen before moving on
sleep(2)
lcd.clear()

#A function to setup the GPIO Pins connected to Traffic Light
def trl_setup(pins):
    """Write a single line of statement to setup all three GPIO Pins
        connected to a Traffic Light"""
    GPIO.setup(pins, GPIO.OUT)


#A callback function to be called in response to hardware interrupt
def pedestrian_cross(channel):
    """Write a single statement to indicate to the function to use
    the global variable ped_cross instead of creating a local variable"""
    global ped_cross
    """Write a single statement to set the global boolean variable ped_cross
    to true to stop the normal traffic light operation"""
    ped_cross = True
    #A while loop to wait for the normal traffic operation to complete
    while norm_traffic:
        sleep(0.5)
    print('Pedestrian Pressed Push Button connected to GPIO ',channel)
    #Clearing the message display
    lcd.clear()
    """Using if and else statement with the parameter channel,determine which
        button is pressed and display the message 'Pedestrian at North: Walk-10'
        or 'Pedestrian at South: Walk-10' over two lines on the LCD"""
    if  channel == btn_north:
        lcd.write(0,0,'Pedestrian at')
        lcd.write(0,1,'North: Walk-10')
       
    else:    
        lcd.write(0,0,'Pedestrian at:')
        lcd.write(0,1,'South Walk-10')
       
    #Write two statements to turn on the red light on both traffic lights
    GPIO.output(trl_west[0], GPIO.HIGH)
    GPIO.output(trl_east[0], GPIO.HIGH)
    #Write a single statement to sleep for ten seconds allowing pedestrians to walk
    sleep(10.0)
    lcd.clear()
    """Write a single statement to set the global boolean variable ped_cross
    to false to resume the normal traffic light operation"""
    ped_cross = False
   
"""A function to setup the GPIO Pins connected to the Pedestrian Crossing button and with
    hardware interrupt"""
def cross_pb_setup(pin):
    """Write a single line of statement to setup a GPIO Pin connected to the pushbutton
    with appropriate pull up or down configuration"""
    GPIO.setup(pin,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
   
    """Write a single statement to setup the OS to detect appropriate rising or falling edge
    with the callback function - pedestrian_cross"""
    GPIO.add_event_detect(pin,GPIO.RISING,callback = pedestrian_cross, bouncetime = 200)
   
#A function to implement the normal traffic Operation
def norm_traf_oper():
    #Write two statements to turn on both Red lights
    GPIO.output(trl_west[0], True)
    GPIO.output(trl_east[0], True)
    #Write statements to display the message 'stop' and sleep for 5 seconds
    lcd.write(0,0,'stop')
    sleep(5.0)
    #Write four statements to turn off both Red lights and turn on both green lights
    GPIO.output(trl_west[0],False)
    GPIO.output(trl_east[0],False)
    GPIO.output(trl_west[2], True)
    GPIO.output(trl_east[2], True)
    #Write statements to display the message 'Drive' and sleep for 5 seconds
    lcd.write(0,0,'Drive')
    sleep(5.0)
    #Write four statements to turn off both Green lights and turn on both Yellow lights
    GPIO.output(trl_west[2],False)
    GPIO.output(trl_east[2],False)
    GPIO.output(trl_west[1], True)
    GPIO.output(trl_east[1], True)
    #Write statements to display the message 'Stop in 2 secs' and sleep for 2 seconds
    lcd.write(0,0,'Stop in 2 secs')
    sleep(2.0)
    #Write two statements to turn off both Yellow lights
    GPIO.output(trl_west[2],False)
    GPIO.output(trl_east[2],False)
   
#A function to turn off the traffic lights
def trl_reset():
    #Write two statements to turn off both traffic lights
    GPIO.output(trl_west,False)
    GPIO.output(trl_east,False)
    #Write a single statement to clear the message on the LCD
    lcd.clear()
#Entry point of the program
if __name__ == '__main__':
    #A single statement to setup the RPi for broadcom mode
    GPIO.setmode(GPIO.BCM)
    #Calling the function trl_setup to setup the west traffic lights using the list: trl_west
    trl_setup(trl_west)
    """Write a single statement to call the function trl_setup
        to setup the east traffic lights using the list: trl_east"""
    trl_setup(trl_east)
    #Calling the function cross_pb_setup to setup the North pushbutton with hardware interrupt
    cross_pb_setup(btn_north)
    """Write a single statement to call the function cross_pb_setup
        to setup the South pushbutton with hardware interrupt"""
    cross_pb_setup(btn_south)
    try:
        # create infiniate loop for the traffic light to continue constatnly when no one is walking and to continue when they are done walking
        while(True):
            if not ped_cross:
                norm_traffic = True
                #function call norm_traf_oper to operate both traffic lights
                norm_traf_oper()
                #function call trl_reset to turn off both traffic lights
                trl_reset()
            else:
                norm_traffic = False
    #something to end the while loop and the program when we want to          
    except KeyboardInterrupt:
        print('Stopping Simulations')
        #Call the function trl_reset to turn off the west traffic lights
        trl_reset()
        #Call the function trl_off to turn off the east traffic lights
        trl_reset()
        print('Cleaning')
        #Write a statement to clean up the GPIO Pins
        GPIO.cleanup()
