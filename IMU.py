# -*- coding: utf-8 -*-
"""
Created on Tue May 15 10:43:44 2018

@author: fahad

@contributor: Lianxin Zhang
"""

import sys
import time
import logging
import globalvar as gl
# import numpy as np
from Adafruit_BNO055 import BNO055


def IMU():

    while True:
        if gl.get_value('flag'):
            break

        try:
            # Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
            bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

            # Enable verbose debug logging if -v is passed as a parameter.
            if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
                logging.basicConfig(level=logging.DEBUG)

            # Initialize the BNO055 and stop if something went wrong.
            if not bno.begin():
                raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

            # Print system status and self test result.
            status, self_test, error = bno.get_system_status()
            print('System status: {0}'.format(status))
            print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
            # Print out an error if system status is in error mode.
            if status == 0x01:
                print('System error: {0}'.format(error))
                print('See datasheet section 4.3.59 for the meaning.')

            #  Print BNO055 software revision and other diagnostic data.
#            sw, bl, accel, mag, gyro = bno.get_revision()
#            print('Software version:   {0}'.format(sw))
#            print('Bootloader version: {0}'.format(bl))
#            print('Accelerometer ID:   0x{0:02X}'.format(accel))
#            print('Magnetometer ID:    0x{0:02X}'.format(mag))
#            print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))


            print('Reading BNO055 data, press Ctrl-C to quit...')
            # stime = np.array([])
            # sHeading = np.array([])
            #CalibData = bno.get_calibration()
            CalibData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 232, 3, 0, 0] #Sensor Calibration data
            bno.set_calibration(CalibData) # Sensor Calibration

            # Print system calibration status
            system, gyr, accellro, magno = bno.get_calibration_status()
#            print('System Calibration Status = ',int(system)) # 0 for no calibration, and 3 for maximum calibration
            print('Gyro Calibration Status = ',int(gyr))
#            print('Accelerometer Calibration Status = ', int(accellro))
#            print('Magnetometer Calibration Status = ', int(magno))

            try:
                
                while True:

                    if gl.get_value('flag'):
                        break # End the loop when flag turned True
                    
                    # Read the Euler angles for heading, roll, pitch (all in degrees).
                    heading, roll, pitch = bno.read_euler()
                    gl.set_value('heading',heading) # Shared the heading information
                    
                    # Print everything out.
                    print('Heading={0:0.2F}'.format(heading-45))
                    
                    #newTime = time.clock()
                    #stime = np.append(stime,newTime)
                    #sHeading = np.append(sHeading,heading)
                    time.sleep(0.5)
                    
            except:
                print('IMU: An exception occured \n')
        except:
            print('IMU: An error occured \n')
            continue


    print('IMU Loop Ended \n')

#IMU()


#------------------------------------------------
