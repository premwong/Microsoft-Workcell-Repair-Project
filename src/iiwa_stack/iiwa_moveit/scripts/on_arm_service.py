#!/usr/bin/env python
import socket
import sys
import logging
import time
import thread
from iiwa_msgs.srv import CollectWrist, CollectWristResponse
import rospy
import numpy as np 
import math
from std_msgs.msg import Float64MultiArray
from config import *

TCP_IP = '172.31.1.150'#'169.254.207.252' 
PORT_NUMBER = 420

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (TCP_IP, PORT_NUMBER)
print "Starting up on " + TCP_IP
sock.bind(server_address)
sock.listen(1)
data = ''
ready = False
rospy.init_node('wrist_cam_server')

def collect(thread_name):
  global data
  global ready
  while True:
    print('waiting for a connection...')
    connection, client_address = sock.accept()
    ready = True
    print('accepted!')
    try:
      print('connection from', client_address)
      while True:
        data = str(connection.recv(400))
        if data:
          data_array_printout = convert_data_string(str(data))
          print("Received: " + str(data_array_printout))
        else:
          print("Waiting...")
    finally:
      connection.close()

def convert_data_string(data_string):
  recieved_buf = data[:-1].split(',')
  float_buf = [float(i) for i in recieved_buf]
  return float_buf

def handle_collect_wrist(req):
  global data
  global ready
  #print "Returning Coordinates pos_x: %s \n pos_y: %s \n pos_z: %s \n ori_w %s \n ori_x %s \n ori_y %s \n ori_z  %s \n" %(req.a, req.b, (req.a + req.b))
  if (ready and len(data) != 0):
    print "returning coordinates"
    float_buf = convert_data_string(data)
    print float_buf
    resp = CollectPoseResponse()
    resp.wrist_x = cpu_pos[0] /1000
    resp.wrist_y = cpu_pos[1] /1000
    return resp
 
def collect_pose_server(thread_name):
  global data
  s = rospy.Service('collect_wrist', CollectWrist, handle_collect_wrist)

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
