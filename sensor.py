# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:05:38 2018

@author: fahad

@contributor: Lianxin Zhang
"""

import time
import xlsxwriter
import random
from collections import deque
import globalvar as gl
from ina219 import INA219
from ina219 import DeviceRangeError



def sensor():
    
    global heading
    global PWM1
    global PWM2
    Shunt_OHMS = 0.1 # For this sensor it is 0.1 ohm

    try:
        print('Starting Current Sensor')
        print('Collecting Sensor Values...')
        start = time.time() # Start Time
        
        #global DataPoints
        DataPoints = deque(maxlen=None) # Creating Array of datatype Deque to store values

        a = 0.9664 # Regression Fitting Parameter
        b = 0.0285 # Regression Fitting Parameter

        ina = INA219(Shunt_OHMS) # Auto Gain
            
        ina.configure()
        print('Current Sensor Configured Successfully')
        while True:            
            
            if gl.get_value('flag'):
                #print('Breaking loop')
                # Break when flag = True
                break
        
            
            #print('Bus Voltage: %.3f V' % ina.voltage())

            try:
                #print('Bus Current: %.3f mA' % ina.current())
                #print('Power: %.3f mW' % ina.power())
                currentvalue = round((a*ina.current())+b) # Rounding off values to nearest integer
                voltagevalue = float('{0:.1f}'.format(ina.voltage())) # Floating point up to one decimal point
                powervalue = round(currentvalue*voltagevalue)
                timevalue = float('{0:.1f}'.format(time.time()-start)) # Elapsed time in Seconds with 1 decimal point floating number 
                headingvalue = float('{0:.2f}'.format(gl.get_value('heading')))
                DataPoints.append([timevalue, currentvalue, voltagevalue, powervalue, gl.get_value('PWM1'), gl.get_value('PWM2'), headingvalue]) # Updating DataPoints Array
                #print('Current: ',currentvalue,'Voltage: ',voltagevalue,'Power: ',powervalue)
            except DeviceRangeError:
                print('Device Range Error')

            time.sleep(0.5) # Reading value after 0.5 second
        
    except:        
        print('Exception Occurred, Current Sensor Stopped \n')

    
    Wt = input('Do you want to store the sensor values Y/N? ')

    if Wt == 'y':
        writing(DataPoints)
    else:
        print('Ending without saving sensor data \n')

    print('Sensor Stopped!\n')
#------------------------------------------------
#sensor()

def writing(Data):

    rnd = random.randint(1,100)
    runDate = time.ctime() 
    workbook = xlsxwriter.Workbook('SensorValues(%d).xlsx'%rnd,{'constant_memory': True})  # Creating XLSX File for Data Keeping 
    worksheet = workbook.add_worksheet() # Generating worksheet

    bold = workbook.add_format({'bold':True}) # Formating for Bold text

    worksheet.write('A1', 'Time', bold) # Writing Column Titles
    worksheet.write('B1', 'Current (mA)', bold)
    worksheet.write('C1', 'Voltage (v)', bold)
    worksheet.write('D1', 'Power (mW)', bold)
    worksheet.write('E1', 'PWM1', bold)
    worksheet.write('F1', 'PWM2', bold)
    worksheet.write('G1', 'Heading Angle', bold)
    worksheet.write('H1', 'Start Time', bold)
    worksheet.write('H2', runDate)
    

    row = 1 # Starting Row (0 indexed)
    col = 0 # Starting Column (0 indexed) 
    

    n = len(Data) # Total number of rows
    print('Total number of rows: ',n)

    print('Writing Data into Worksheet')
        
    for Time, value1, value2, value3, value4, value5, value6 in (Data):
        # Writing Data in XLSX file
            
        worksheet.write(row, col, Time)
        worksheet.write(row, col+1, value1)
        worksheet.write(row, col+2, value2)
        worksheet.write(row, col+3, value3)
        worksheet.write(row, col+4, value4)
        worksheet.write(row, col+5, value5)
        worksheet.write(row, col+6, value6)
        row += 1

    chart1 = workbook.add_chart({'type': 'line'}) # adding chart of type 'Line' for Current values
    chart2 = workbook.add_chart({'type': 'line'}) # Chart for Voltage
    chart3 = workbook.add_chart({'type': 'line'}) # Chart for Power

        
    
    chart1.add_series({'name':['Sheet1',0,1],
                           'categories': ['Sheet1', 1,0,n,0],
                           'values': ['Sheet1', 1,1,n,1]
                           })
    chart2.add_series({'name':['Sheet1',0,2],
                           'categories': ['Sheet1', 1,0,n,0],
                           'values': ['Sheet1', 1,2,n,2]
                           })
    chart3.add_series({'name':['Sheet1',0,3],
                           'categories': ['Sheet1', 1,0,n,0],
                           'values': ['Sheet1', 1,3,n,3]
                           })
    
    chart1.set_title({'name': 'Current Chart'}) # Setting Title name
    chart1.set_x_axis({'name': 'Elapsed Time (s)'}) # Setting X-Axis name
    chart1.set_y_axis({'name': 'Value'}) # Setting Y-Axis name

    chart2.set_title({'name': 'Voltage Chart'})
    chart2.set_x_axis({'name': 'Elapsed Time (s)'})
    chart2.set_y_axis({'name': 'Value'})

    chart3.set_title({'name': 'Power Chart'})
    chart3.set_x_axis({'name': 'Elapsed Time (s)'})
    chart3.set_y_axis({'name': 'Value'})


    chart1.set_style(8) # Setting Chart Color
    chart2.set_style(5)
    chart2.set_style(9)

    worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10}) # Inserting Charts in the Worksheet
    worksheet.insert_chart('D2', chart2, {'x_offset': 25, 'y_offset': 10}) # //
    worksheet.insert_chart('D5', chart3, {'x_offset': 25, 'y_offset': 10}) # //
    

    workbook.close() # Closing Workbook 
    time.sleep(1)
    print('Sensor Writing successfull \n')
    
#-------------------------------------------------
