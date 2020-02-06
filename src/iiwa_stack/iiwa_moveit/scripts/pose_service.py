#!/usr/bin/env python

from iiwa_msgs.srv import CollectPose,CollectPoseResponse
import rospy
import socket


def handle_collect_pose(req):
  #print "Returning Coordinates pos_x: %s \n pos_y: %s \n pos_z: %s \n ori_w %s \n ori_x %s \n ori_y %s \n ori_z  %s \n" %(req.a, req.b, (req.a + req.b))
  print "returning coordinates"
  #TODO: change to recieve from TCP
  resp = CollectPoseResponse()
  resp.orientation_w = 1.57
  resp.orientation_x = 0
  resp.orientation_y = 0.71
  resp.orientation_z = 0
  resp.position_x = 0.28
  resp.position_y = 0.57
  resp.position_z = 1.17
  return resp

def collect_pose_server():
  rospy.init_node('collect_pose_server')
  s = rospy.Service('collect_pose', CollectPose, handle_collect_pose)
  print "Ready to send pose."
  rospy.spin()



if __name__ == "__main__":
  collect_pose_server() 