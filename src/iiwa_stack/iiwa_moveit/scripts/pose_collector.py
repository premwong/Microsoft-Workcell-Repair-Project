#!/usr/bin/env python
import socket
import sys
import logging
import time
import threading 
from iiwa_msgs.srv import CollectPose,CollectPoseResponse
import rospy
import transforms3d
import numpy as np 
import math

TCP_IP = '172.31.1.150'#'169.254.207.252' # from ipconfig - ethernet adapter
PORT_NUMBER = 69

# # Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Bind the socket to the port
server_address = (TCP_IP, PORT_NUMBER)
print("Starting up on ", server_address)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)
data = ''
rospy.init_node('collect_pose_server')


class Collect_Thread(threading.Thread):
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name

	def run(self):
		global data
	  while True:
    	# Wait for a connection
	    print('waiting for a connection...')
	    connection, client_address = sock.accept()
	    print('accepted!')
	    try:
	        print('connection from', client_address)

	        # Receive the data in small chunks and retransmit it
	        while True:
	            data = str(connection.recv(35))
	            if data:
	                print("Received: " + str(data))
	            else:
	                print("Waiting...")
	            
	    finally:
	        # Clean up the connection
	        connection.close()


class Server_Thread(threading.Thread):
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name

		def run(self):
			global data
		  s = rospy.Service('collect_pose', CollectPose, handle_collect_pose)
		  print "Ready to send pose."
		  rospy.spin()


def handle_collect_pose(req, data_string):
  #print "Returning Coordinates pos_x: %s \n pos_y: %s \n pos_z: %s \n ori_w %s \n ori_x %s \n ori_y %s \n ori_z  %s \n" %(req.a, req.b, (req.a + req.b))
  print "returning coordinates"
  print data_string
  pose = data_string.split(',')
  print pose
  #Convert from Euler to quaternion
  theta_rad = math.radians(pose[3])
  cos_angle = math.cos(theta_rad)
  sin_angle = math.sin(theta_rad)
  rotation_mat = [[-1 * cos_angle, sin_angle, 0], [sin_angle, cos_angle, 0], [0, 0, -1]]
  quat = mat2quat(rotation_mat)
  print quat
  resp = CollectPoseResponse()
  resp.orientation_w = quat[0]
  resp.orientation_x = quat[1]
  resp.orientation_y = quat[2]
  resp.orientation_z = quat[3]
  resp.position_x = pose[1] / 1000
  resp.position_y = pose[2] / 1000
  return resp
 

a = Collect_Thread("my_collect_thread")
b = Server_Thread("server_thread")


a.start()
b.start()

a.join()
b.join()