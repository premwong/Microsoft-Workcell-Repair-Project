#!/usr/bin/env python
# Accepts the bluetooth connection

import rospy
import bluetooth
from std_msgs.msg import Bool
from iiwa_msgs.srv import Bluetooth

def handle_bluetooth(req):
    print("Handling bluetooth...")
    # Connect to computer
    # Check if the the computer says that the server is in place
    # If yes, then return 1
    # If not yet, keep waiting
    # if error, return 0
    server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    not_connected = True
    port = 1
    try:
        server_sock.bind(("",port))
        server_sock.listen(1)
        client_sock,address = server_sock.accept()
        print("Accepted connection from ",address)
        not_connected = True
    except: 
        print("Can't connect.")
    
    data = client_sock.recv(1024)
    print("received [%s]" % data)

    client_sock.close()
    server_sock.close()
    return 1

# Need to make a Bluetooth.srv
# mkdir srv (if you dont have a srv dir)
# In the file:
# bool True
# ---
# int32 status
def bluetooth_server():
	rospy.init_node('bluetooth_server')
	service = rospy.Service('bluetooth_service', Bluetooth, handle_bluetooth)
	rospy.spin()