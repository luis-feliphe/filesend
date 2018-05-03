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


from Controlo import Controlo
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
import datetime
####
from tf.transformations import euler_from_quaternion
import tf
import struct
from datetime import datetime
from sensor_msgs.msg import LaserScan
getTime = lambda: int(round(time.time() * 1000))

import math
RATE=6


global posicao
posicao = None


def degrees(value):
	return (value*180)/math.pi#math.degrees(value)#((value* 180.0)/math.pi)
def getpos(odom):
	global posicao
	posicao= odom

def hasDataToWalk():
	global posicao
	return posicao != None

def getDataFromRos():
	global posicao
	x, y, z = 0, 0 ,0
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

#############
# ROS SETUP #
#############
#Became a node, using the arg to decide what the number of robot
global myId





rospy.init_node("Controlador_experimento_I")
rospy.Subscriber("/odom", Odometry, getpos)
p = rospy.Publisher("/cmd_vel_mux/input/teleop", Twist)

r = rospy.Rate(RATE) # 5hz


u = 1.5
	
#################
#   Main Loop   #
#################
points = [(0.07, 1.79, 270.7), (0.5,1.51,31.55), (4.51,2.92,305), (4.71,0.26,359.96),(4.36,1.16,66.14),(2.08,2.55,91.25),(0,0,0)]
#points = [(0, -u)]
cont = 0
posInicialx=0
posInicialy=0







#### Iniciando o loop principal ######

try:
	algoritmo = Controlo()
	while not rospy.is_shutdown():
		if hasDataToWalk():
			x, y , mx, my, mz = getDataFromRos()
			t= Twist()
			x, y, z = points[cont]
			lin,ang  = algoritmo.start(x, y, z, mx, my, mz)
			if (lin == 0 and ang == 0):
				cont= (cont + 1)%len (points)
				print (str (cont) + " Imagem\n")
				file_name = "imagem"+str(cont)+".jpg"
				os.system("python take_photo.py " + str (file_name))
				os.system("python client.py " + str (file_name))
				if (cont == 0):
					print "CHEGAMOS NO PONTO FINAL"
					
			global saida
			t.angular.z = ang
			t.linear.x = lin
			p.publish(t)
		r.sleep()

except Exception :
	raise	
print ("Exception!\n")
