# -*- coding: utf-8 -*-
"""
Created on Thu May 17 15:14:09 2018

@author: Lianxin Zhang
"""
"""This is the controller of autocruise mode with split-zone strategy
"""
import math
import time
#import numpy as np
#from PID import PID
import globalvar as gl

ESC1 = 4 # Motor1
ESC2 = 17 # Motor2
ESC3 = 24 # Rudders
ESC4 = 25 # Sails

STBY = 23
AIN2 = 21 # For motor direction
AIN1 = 20 # For motor direction
BIN1 = 27 # For motor direction
BIN2 = 22 # For motor direction

#tacking_degree = 30
#cur_state = 'right' # the heading direction before tacking


def controller(pi):
    cur_state = 'right'
    tacking_degree = 30
    while True:
        # quit signal
        if gl.get_value('CruiseStatus') == 'H': 
            break
        
        # get pixel position
        cur_pos = gl.get_value('Cur_Loc')
        #print('Current position: ', cur_pos)
        x = cur_pos[0]   # x,y coordinates
        y = cur_pos[1]
        if x == 0 and y == 0:
            continue
        # get heading angle
        cur_angle = gl.get_value('heading')-55 # already set the x-positive as zero
        if cur_angle < 0:
            cur_angle = cur_angle + 360
        print('Current position: ', cur_pos, '  Current heading angle: ', cur_angle)
        
        # boundary
        if x < 50 or x > 800 or y < 100 or y > 1100:
            state_rudder,state_sail,PWM1,PWM2 = boundary(x,y,cur_angle)
        
        # forward channel
        elif x > 50 and x < 600 and y > 400 and y < 1100:
            state_sail = 'tight'
            # tacking(pi)
            print('in the zone of forward channel')
            if y > 700 and y < 1000:
                state_sail = 'tight'
                PWM1 = 0
                PWM2 = 0
                if cur_state == 'left':
                    if cur_angle > 330 and cur_angle < 360:
                        state_rudder = 'left'
                    elif cur_angle > 0 and cur_angle < 300:
                        state_rudder = 'right'
                    else:
                        state_rudder = 'forward'
                elif cur_state == 'right':
                    if cur_angle > 60 and cur_angle < 360:
                        state_rudder = 'left'
                    elif cur_angle > 0 and cur_angle < 30:
                        state_rudder = 'right'
                    else:
                        state_rudder = 'forward'
            elif y < 700 and y > 400: # tacking to right
                if (cur_angle > 0 and cur_angle < 25) or (cur_angle > 180 and cur_angle < 360):
                    #state_sail = 'loose'
                    state_rudder = 'right'
                    PWM1 = 220
                    PWM2 = 255
                elif cur_angle > 50 and cur_angle < 180:
                    #state_sail = 'loose'
                    state_rudder = 'left'
                    PWM1 = 255
                    PWM2 = 220
                else:
                    state_rudder = 'forward'
                    PWM1 = 0
                    PWM2 = 0
                print('tack to right')
                if cur_state == 'left':
                    cur_state = 'right'
            elif y > 1000 and y < 1100: # tacking to left
                if (cur_angle > 0 and cur_angle < 180) or (cur_angle > 335 and cur_angle < 360):
                    state_sail = 'loose'
                    state_rudder = 'left'
                    PWM1 = 255
                    PWM2 = 200
                elif cur_angle > 180 and cur_angle < 310:
                    state_sail = 'loose'
                    state_rudder = 'right'
                    PWM1 = 200
                    PWM2 = 255
                else:
                    state_rudder = 'forward'
                    PWM1 = 0
                    PWM2 = 0
                print('tack to left')
                if cur_state == 'right':
                    cur_state = 'left'
        # transfer channel
        elif x > 600 and x < 800 and y > 400 and y < 1100:
            print('in the zone of transfer channel')
            state_sail = 'loose'
            if (cur_angle > 0 and cur_angle < 90) or (cur_angle > 290 and cur_angle < 360):
                state_rudder,PWM1,PWM2 = turn('left')
            elif cur_angle > 90 and cur_angle < 250:
                state_rudder,PWM1,PWM2 = turn('right')
            elif x < 650:
                state_rudder,PWM1,PWM2 = turn('right')
            elif x > 750:
                state_rudder,PWM1,PWM2 = turn('left')
            else:
                state_rudder = 'forward'
                PWM1 = 0
                PWM2 = 0
        # backward channel
        elif x > 100 and x < 800 and y > 100 and y < 400:
            print('in the zone of backward channel')
            state_sail = 'loose'
            PWM1 = 150
            PWM2 = 150
            if cur_angle > 0 and cur_angle < 160:
                state_rudder = 'right'
            elif cur_angle > 200 and cur_angle < 360:
                state_rudder = 'left'
            elif y < 200:
                state_rudder = 'left'
            elif y > 250:
                state_rudder = 'right'
            else:
                state_rudder = 'forward'
                #PWM1 = 0
                #PWM2 = 0
        elif x > 50 and x < 100 and y > 100 and y < 400:
            print('in the zone of backward channel 2')
            state_sail = 'tight'
            if cur_angle > 65 and cur_angle < 360:
                state_rudder = 'left'
                PWM1 = 255
                PWM2 = 0
            elif cur_angle > 0 and cur_angle < 45:
                state_rudder = 'right'
                PWM1 = 0
                PWM2 = 255
            else:
                state_rudder = 'forward'
                PWM1 = 0
                PWM2 = 0
            if cur_state == 'left':
                cur_state = 'right'
        
        # assign to the boat FSM
        try:
            actuator(pi, state_rudder, state_sail, PWM1, PWM2)
        except:
            print('Fail to take a action!')
            continue
    # end of the program
#


def turn(side):
    if side == 'right':
        PWM1 = 220
        PWM2 = 255
    elif side == 'left':
        PWM1 = 220
        PWM2 = 250
    elif side == 'forward':
        PWM1 = 255
        PWM2 = 200
    state_rudder = side
    return state_rudder,PWM1,PWM2

def boundary(x,y,cur_angle):
    if x < 50:
        #boundary_x_l(pi)
        print('in the boundary_x_l')
        if cur_angle > 60 and cur_angle < 180: # wrong orientation
            state_rudder,PWM1,PWM2 = turn('left')
            state_sail = 'tight'
        elif (cur_angle > 180 and cur_angle < 360) or (cur_angle > 0 and cur_angle < 30):
            state_rudder,PWM1,PWM2 = turn('right')
            state_sail = 'tight'
        else: # right orientation
            state_rudder,PWM1,PWM2 = turn('forward')
            state_sail = 'tight'
    elif x > 800:
        #boundary_x_h(pi)
        print('in the boundary_x_h')
        if (cur_angle > 240 and cur_angle < 360):
            state_rudder = 'left'
            state_sail = 'loose'
            PWM1 = 0
            PWM2 = 0
        elif cur_angle > 0 and cur_angle < 210:
            state_rudder = 'right'
            state_sail = 'loose'
            PWM1 = 0
            PWM2 = 0
        else: # right orientation
            state_rudder = 'forward'
            state_sail = 'loose'
            PWM1 = 0
            PWM2 = 0
    elif y < 100:
        #boundary_y_l(pi)
        print('in the boundary_y_l')
        if (cur_angle > 0 and cur_angle < 120) or (cur_angle > 270 and cur_angle < 360) :
            state_rudder,PWM1,PWM2 = turn('right')
            state_sail = 'loose'
        elif cur_angle > 150 and cur_angle < 270:
            state_rudder,PWM1,PWM2 = turn('left')
            state_sail = 'loose'
        else: # right orientation
            state_rudder,PWM1,PWM2 = turn('forward')
            state_sail = 'loose'
    elif y > 1100:
        #boundary_y_h(pi)
        print('in the boundary_y_r')
        if cur_angle > 180 and cur_angle < 300:
            state_rudder,PWM1,PWM2 = turn('right')
            state_sail = 'tight'
        elif (cur_angle > 330 and cur_angle < 360) or (cur_angle > 0 and cur_angle < 180):
            state_rudder,PWM1,PWM2 = turn('left')
            state_sail = 'tight'
        else: # right orientation
            state_rudder,PWM1,PWM2 = turn('forward')
            state_sail = 'tight'
    return state_rudder,state_sail,PWM1,PWM2


def actuator(pi, state_rudder, state_sail, PWM1, PWM2):
    # rudder
    if state_rudder == 'forward':
        pi.set_servo_pulsewidth(ESC3,1250)
        pi.write(AIN1,1)
        pi.write(AIN2,0)
        pi.write(BIN1,1)
        pi.write(BIN2,0)
    elif state_rudder == 'left':
        pi.set_servo_pulsewidth(ESC3,800)
        pi.write(AIN1,1)
        pi.write(AIN2,0)
        pi.write(BIN1,0)
        pi.write(BIN2,1)
    elif state_rudder == 'right':
        pi.set_servo_pulsewidth(ESC3,1700)
        pi.write(AIN1,0)
        pi.write(AIN2,1)
        pi.write(BIN1,1)
        pi.write(BIN2,0)
    # sails
    if state_sail == 'loose':
        pi.set_servo_pulsewidth(ESC4,1600) # Sails Lossen
    elif state_sail == 'tight':
        pi.set_servo_pulsewidth(ESC4,900) # Sails Tighten
    # motor
    pi.set_PWM_dutycycle(ESC1, PWM1)
    pi.set_PWM_dutycycle(ESC2, PWM2)
    time.sleep(0.05)
    
