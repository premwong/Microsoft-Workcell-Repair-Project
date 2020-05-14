#!/usr/bin/env python

import rospy
import bluetooth
from iiwa_msgs.srv import Bluetooth

def bluetooth_client():
    rospy.wait_for_service("bluetooth_service")
    bluetooth_service = rospy.ServiceProxy("bluetooth_service", Bluetooth)
    resp1 = bluetooth_service(True)
    return resp1.status

if __name__=="__main__":
    print("Starting bluetooth_client...")
    bl_ready = bluetooth_client()