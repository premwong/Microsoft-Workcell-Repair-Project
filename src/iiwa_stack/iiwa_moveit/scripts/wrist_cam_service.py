#!/usr/bin/env python
import socket
import sys
import logging
import time
import thread
import rospy
import numpy as np 
import math
from std_msgs.msg import Float64MultiArray
from iiwa_msgs.srv import CollectWrist, CollectWristResponse

TCP_IP = '172.31.1.150' #server socket's IP
PORT_NUMBER = 420

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (TCP_IP, PORT_NUMBER)
print "Starting up on " + TCP_IP
sock.bind(server_address)
sock.listen(1)
data = ''
ready = False
rospy.init_node('wrist_cam_server')
wrist_cam_pub = rospy.Publisher('wrist_cam_feed', Float64MultiArray, queue_size=50)

def convert_data_string(data_string):
  recieved_buf = data[:-1].split(',')
  float_buf = [float(i) for i in recieved_buf]
  return float_buf

def collect_wrist(thread_name):
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
          print("Received_wrist: " + str(data))
          publish_data = Float64MultiArray()
          publish_data.data = convert_data_string(data)
          wrist_cam_pub.publish(publish_data)
        else:
          print("Waiting...")
    finally:
      connection.close()

def handle_collect_wrist(req):
  global data
  global ready

  if (ready and len(data) != 0):
    print("returning coordinates")
    float_buf = convert_data_string(data)
    print(float_buf)

    resp = CollectWristResponse()
    resp.wrist_x = float_buf[0] /1000
    resp.wrist_y = float_buf[1] /1000
    return resp
 
def collect_wrist_server(thread_name):
  global data
  s = rospy.Service('collect_wrist', CollectWrist, handle_collect_wrist)
  
  print "Service Connected."
  rospy.spin()


if __name__ == "__main__":
  try:
    thread.start_new_thread(collect_wrist, ( 'thread 1', ))
    thread.start_new_thread(collect_wrist_server, ('thread 2', ))

  except: 
    print('error')

  while 1:
    pass
