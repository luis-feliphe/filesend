# -*- coding: utf-8 -*-
#goAtoB
#cmd_vel,odom 
#Robot move from A to B
#turlebot
#./know/movaAparaB.py
#name
#controlo, findme
#active


######################################
# This file simulate a robot on ROS. #
# To use, you need to pass like      #
# argument the numnber of robot,     #
# like "./movingRobot 1"             #
######################################


#ROS  imports
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Quaternion
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool
from std_msgs.msg import String
import os
import random
import sys
import time
####
from tf.transformations import euler_from_quaternion
import tf
import struct
from datetime import datetime
from sensor_msgs.msg import LaserScan
getTime = lambda: int(round(time.time() * 1000))
from pynput.keyboard import Key, Listener

import math
RATE=1


global posicao
posicao = None

lista = []
global primeiro
primeiro = True

def on_press(key):
	global posicao
	if (key == Key.space):
		x, y, z = getxy(posicao)
		lista.append("["+str(x)+","+str(y)+","+str(z)+"]")
	elif( key == Key.esc):
#		print('{0} pressed'.format(key))
		print "["
		for i in lista:
			print str(i)
		print "]"
		return False
#	sys.exit()

def degrees(value):
	return (value*180)/math.pi#math.degrees(value)#((value* 180.0)/math.pi)
def getpos(odom):
	global primeiro
	if primeiro:
		print "Primeiro dado recebido"
		primeiro = False
	global posicao
	posicao = odom
	x, y, z = getxy (odom)
#	print "X = "+ str(x) + "\tY =" + str(y) + "\tZ = " + str(z)
def getDataFromRos():
	global posicao
	mx, my, mz = getxy (posicao)
	return x, y , mx, my, mz

def getDegreesFromOdom(w):
	#TODO: HOW CONVERT DATA TO ANGLES
	q = [w.pose.pose.orientation.x,	w.pose.pose.orientation.y, w.pose.pose.orientation.z, w.pose.pose.orientation.w]       
        euler_angles = euler_from_quaternion(q, axes='sxyz')
	current_angle = euler_angles[2]
	if current_angle < 0:
		current_angle = 2 * math.pi + current_angle
	return degrees(current_angle)
		

def getxy (odom):
#	return round (odom.pose.pose.position.x), round ( odom.pose.pose.position.y), round (getDegreesFromOdom (odom))#degrees(yall)
	return odom.pose.pose.position.x,  odom.pose.pose.position.y, getDegreesFromOdom (odom)#degrees(yall)

global myId
rospy.init_node("path_generator")
rospy.Subscriber("/odom", Odometry, getpos)

r = rospy.Rate(RATE)



with Listener(
        on_press=on_press,
        ) as listener:
    listener.join()
	
try:
	while not rospy.is_shutdown():
		r.sleep()

except Exception :
	raise	
print ("Exception!\n")
