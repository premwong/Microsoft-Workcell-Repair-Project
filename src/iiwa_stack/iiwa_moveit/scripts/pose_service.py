#!/usr/bin/env python
import socket
import sys
import logging
import time
import thread
from iiwa_msgs.srv import CollectPose,CollectPoseResponse
import rospy
import numpy as np 
import math

TCP_IP = '172.31.1.150'#'169.254.207.252' # from ipconfig - ethernet adapter
PORT_NUMBER = 69

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (TCP_IP, PORT_NUMBER)
print "Starting up on " + TCP_IP
sock.bind(server_address)
sock.listen(1)
data = ''
ready = False
rospy.init_node('collect_pose_server')

def collect(thread_name):
  global data
  global ready
  while True:
      # Wait for a connection
      print('waiting for a connection...')
      connection, client_address = sock.accept()
      ready = True
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

def handle_collect_pose(req):
  global data
  global ready
  #print "Returning Coordinates pos_x: %s \n pos_y: %s \n pos_z: %s \n ori_w %s \n ori_x %s \n ori_y %s \n ori_z  %s \n" %(req.a, req.b, (req.a + req.b))
  if (ready and len(data) != 0):
    print "returning coordinates"

    pose = data[:-1].split(',')
    print pose
    float_pose = [float(i) for i in pose]
    #Convert from Euler to quaternion
    resp = CollectPoseResponse()
    resp.position_x = float_pose[1] / 1000
    resp.position_y = float_pose[2] / 1000
    resp.orientation_theta = math.radians(float_pose[3])
    return resp
 
def collect_pose_server(thread_name):
  global data
  s = rospy.Service('collect_pose', CollectPose, handle_collect_pose)

  print "Service Connected."
  rospy.spin()

if __name__ == "__main__":
  try:
    print 'hello'
    thread.start_new_thread(collect, ( 'thread 1', ))
    thread.start_new_thread(collect_pose_server, ('thread 2', ))

  except: 
    print 'error'

  while 1:
    pass
