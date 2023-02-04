# System-Final-Project

Final Project Report
Purpose and Scope
	The purpose of the final project is to be able to create a system which are combination of all information about system and Python which we were learnt in class from the beginning of this semester
Material and Resource
~	Raspberry Pi with Raspbian operating system installed on a micro SD card
~	USB keyboard & mouse
~	HDMI monitor & cable
~	Breadboard
~	Pi ‘Wedge’ breadboard adapter
~	Ribbon cable to connect the Wedge to the Pi
~	Power supplies for the Pi and monitor
~	Resistors (220 ohm)
~	LED (red and green)
~	Push Button
~	Breadboard M-M wires for interconnects
~	Shift Register
~	Battery Pack
~	Motor (Mini DC GearBox)
~	MOSFETs
~	H-Bridge dual motor
~	Flashlight
~	Radio
~	Speaker
Background
	Our expectation for this project is to simulate a car interior system. We want to have a headlight and high beam control by first push button. Because high beam and low beam headlight on the car are separated bulb, so we choose to use the head of the flashlight for the high beam. We also want to have an emergency light which is the blinking LEDs on the right and left of the car. This light also controls by the second push button. We added turn signal by 2 more push buttons. Each button will control one side of the emergency blinking LEDs. We also want to have an engine can rotate forward and backward. Each rotating direction will be controlled by two more push button. In total we have 6 push buttons. We also have an LCD Display which is print what function in the system is working. 
Wiring 
 
	At the beginning, we started by wiring the LED and the push button first. Six LEDs must be placed at  the  top  of  the  circuit  area  (with  the 
positive/longer leads of the light towards the GPIO). The resistor should then be 
placed in the same row as the positive dock of each LED. The M-M wires also link 
the red positive power bus to the resistors in the same row. Finally, connect the 
M-M cable to the Wedge system (the red part on the left). On our system, two yellow LEDs will connect to the wedge and four LEDs left will connect to the shift register. We have to do this because we are out of pin number on the wedge. 
	Then we wired six push buttons. The buttons were placed on holes which are nearest to the center of the breadboard. Then we utilized an M-M connected 
to link a push buttons' positive dock to a power bus. The pushbutton connects between Ground and a GPIO pin that's set up as an input with the pullup resistor
 
	Next step, we worked on the LCD display. At the back of the display, here 
are 4 pins which are GND, VCC, SDA, and SCL. VCC is the power supply for nearly all the devices. The ground (GND) serves as a reference point against which the VCC is measured. When compared to GND, the VCC can be either positive or negative. The VCC for display will be plug in the positive bus on the breadboard and the GND will be plug in the negative bus. On the diagram, the red cable is VCC, and black cable is GND. When you check on figure 1, The red cable should be on positive bus and the black cable is going to be on the negative bus. SDA is a Serial Data pin which for transmit and receive data. The SCL is a Serial Clock pin which is used for timing signal. The wedge of the breadboard has a plug for SCL and SDA. Plug the pin to match the pin on the wedge of the breadboard. (The figure is not match with the color because I took this figure from lab report 4. Sorry for the confusion.)
	Then we started to work on the shift register. A shift register is a chip which is used to convert serial data into parallel data. It will take three GPIO pins and convert three to eight bits and it will be corresponded with eight more pins on the Wedge. From the shift register, connect serial shift clock to pin 6 and connect the parallel update output on pin 5 and the latch pin 13 to the shift register to control our eight outputs. Also connect the top right of the shift register to the 3V3 and the bottom left to the ground.   
	In our system, there are 2 MOSFET. they are intended to switch huge DC loads from a single microcontroller digital pin. Its primary use is to give a low-cost method of driving a DC motor for robotics applications, but it may also be used to operate most high-current DC loads. 
	On the left of the MOSFET. There are 2 pairs of screws cover by a blue plastic. On the left, it writes VIN and GND. These two screws will connect with the battery pack. As you can see on the image, the battery pack already has red and black wire. You just need to connect the black wire to the GND and the red wire to the VCC with the screwdriver. On the right of the MOSFET, it writes V+ and V-. On the fan and the head of the flashlight. There are a black cable and red cable again. Connect the red one to the V+ and the V- to the black cable. 
 
On this project, we destroyed a flashlight to take the lightbulb on the top. We have to solder the red cable and black cable to the flashlight. We do this to connect the lightbulb to the MOSFET and we will be able to control it. 
 
For the motor. I choose to use the motor drive board. It is an H-bridge and uses MOSFETs to be able to switch higher current. But it also has an ability to polarity which is reverse the direction of the current. So the motor can spin forward and backward. 









Coding
 
 Figure 1 
	In the beginning from line 3 to line 6, we will need to import some module to control the system. The GPIO on line 3 is import pin number and order port on the wedge. Import time so we can have some code take a current time or stop the code execution for the certain amounts of time. Than import smbus to use the i2c structure. From 13 to 16, we assigned pin 5, 6, 13 to data, clock and latch pin. Then from 17 to 21, we set up for the shift register. The line 
‘GPIO.setmode()' sets the BCM number to match the Wedge. Line 23 and 24 will use later for shift register to send out signal. 


 
Figure 2: Yellow LED, fan, and flashlight set up
	On line 27 and 28, there are 2 pins for 2 yellow LEDs. To 
command the LED to light up or not, we need to construct code 
GPIO.output(GPIO.HIGH), the LED will be off because of two 3.3Volts on bot pins of the LED. So, the total Voltage will be 0 make the LED off. On line 30 is just set mode output for the LED. Do the same thing for fan and flashlight (“HighBeam” on line 37)
 
Figure 3: Set up for motor. 
	Again, assigning 2 pins number for the motor and the direction of the motor. Because the H-bridge use MOSFET to control the voltage and also the polarity to reverse the spinning direction, so we need one pin for the motor.  Then set output mode for the direction and the motor. So the same for the second motor. 

 
Figure 4: All the push button set up. 
	Again, we need to declare all push button with their corresponded pin number. When Python executes, the Pi will initialize the button as input internal pull up. it waits for a change in state of the Input pin, which happens only when the button is pressed


≈     figure 5: shift register sending signal for LEDs function

Next, we’ll create the shiftOut function to output the value to the shift register. We’ll will start with the binary value 0x01 or 0x80, depending on which direction it’s going. Next, we’ll use a for loop in conjunction with Python’s bitwise operator (<< and >>) to change the binary value. To put it simply, bitwise will shift the position of the 1 to the next position. On line 94 to line 100. That is the function to turn on the LED. 

 
Figure 6: Engine start
	PWM is a method to reduce the average power drive from an electrical signal. So, we can control the speed of the rotating. Then we start the motor by zero. Do the same for the second engine. 

 
Figure 7
	From line 202 to 206, I forget to delete it because these lines are intended for blinking LED. However, I do not need it anymore. From 209 to 217, This value is used later. On line 218, we start the LCD. 


 
Figure 8
	This function is used to turn on 2 red LED and 2 white LED. When the program is running, the white button is pressed on line 221. And it will check the condition if the LED_was_on == True. But on the previous figure, we set it equal True already, so it will passed on line 224, Then the 2 white and 2 red LEDs will turn on, the flashlight is off on this figure. Then on the LCD Display, it will print on line 1 “Headline On” and line 2 “  **  ” Then set LED_was_on and HighBeam_was_on equal false for further coding. From line 239 to 241, it will prevent switch bouncing issue.


 
Figure 9: 
	Then if we press the white push button again. And it will check for two conditions was set on the last figure, so it will pass. The only different down here is that the flashlight is on. At the end, LED_was_on set to be false and HighBeam_was_on set to be True for the next block. 
	So you pressed again, it will passed on line 262. All the LED and the flashlight will be off. The LCD will print “Headline Off” on line 1 and “Highbeam off” on line 2 for 1 second. Than the LCD will delete everything. At the end, LED_was_on equal true and HighBeam_was_on equal False. We did this in order to loop back on the previous figure.

 
Figure 10: Emergency light
	On line 285, if the emergency button is pressed and if EMER_was_on is true. It will be passed because we set this is true before. Then it will execute infinite loop that will blinking 2 yellow LED and on the LCD will also blinking woth two arrow head. It will look like on line 299. At the end, it will set the EMER_was_on is false. Than if we pressed the button again, the LEDs and the LCD will stop blinking and the code will escape the loop until we pressed the button again


 
	 
 
	For tailgate left and right. It nearly the same with the emergency light. On these two functions, there will be only one LED blinking. 








 
	
	For the engine/motor, it can rotate forward or backward. On line 380 and 381. There are a number at the end of the line. That number is representing the direction of the rotation. There are only zero (0) and one (1) for counterclockwise and clockwise. On line 410 and 411, the number is zero (0) compared to one (1) on line 380 and 381. When the forward or the backward button is pushed, it will check for the condition Backward is true, then it will execute the infinite loop. When the push button is pressed, we need to set the direction for the motor on line 380, 381, 410 and 411. Then it will print “running backward” or “running forward” on line 382 and 412. The LCD also print the previous sentence with the “fan on” on the second line of the LCD display. Then, the engine will start to rotate on line 385, 386, 415, and 416. And the fan is also start spinning, When the engine is rotating backward or forward, and you press a button you just pressed again. The engine will stop on line 367, 368, 396, and 397. Then the fan will stop spin on line 398 and 369. Then the LCD display will print “stop moving” for one second then the word is erased. 
Problem and Next Step
	The problem that we have in this final project is about the shift register. When we started to write the code, we did not think about the issue that we were out of GPIO pin, so when we aware the issue and replace 3 pins by a shift register which send parallel signal out to become eight pins. So we have to re-code the LED and the push button again 
	If we have more time on this project, I might try to make an LCD display print out the speed of the wheel. It is not the actual speed, but it will make our system better. We also have made a small radio system. We tried to connect the radio to our system, but it does not work well. So, we decided not to include it in our system. 
