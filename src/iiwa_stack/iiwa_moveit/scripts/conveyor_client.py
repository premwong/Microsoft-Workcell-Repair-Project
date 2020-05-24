#!/usr/bin/env python

import rospy
import sys
from iiwa_tool_moveit.srv import MoveConveyor

def move_conveyor_client(bl_ready):
    status = 0
    rospy.wait_for_service('move_conveyor')
    try:
        move_conveyor = rospy.ServiceProxy('move_conveyor', MoveConveyor)
        if bl_ready:
            status = move_conveyor("F")
        else:
            status = move_conveyor("R")
    except rospy.ServiceException as e:
        print(e)
    return status

if __name__ == "__main__":
    move_conveyor_client()