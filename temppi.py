#!/usr/bin/env python
#
# GrovePi Example for using the Grove - Temperature&Humidity Sensor (High-Accuracy & Mini)(http://www.seeedstudio.com/depot/Grove-TemperatureHumidity-Sensor-HighAccuracy-Mini-p-1921.html
#		
# This example prints the gesture on the screen when a user does an action over the sensor
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

#################################################################################################################################################
# NOTE:
# The software for this sensor is still in development and might make your GrovePi unuable as long as this sensor is connected with the GrovePi
#################################################################################################################################################
from grove_rgb_lcd import *
import grove_i2c_temp_hum_mini
import time
import random
import comms

# init temp sensor
t = grove_i2c_temp_hum_mini.th02()

# init comms system
comms_system = comms.Comms()
comms_system.log('comms started')
comms_system.aio_create_feed("SC03temp")
send_to_comms = False

## MAIN APP LOOP
while True:
	# read the temp
	try:
		temp = (t.getTemperature() * 1.8) + 32
	except Exception as ee:
		setText(ee.__str__())

	# random color for LCD screen
	setRGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
	setText('Temp: %.2fF' % temp)

	# stagger AIO to reduce cloud data store
	if send_to_comms:
		try:
			comms_system.aio_send("SC03temp", temp)
		except Exception as ee:
			setText(ee.__str__())
		send_to_comms = False
	else:
		send_to_comms = True

	# TEN SECOND CYCLE
	time.sleep(10)
