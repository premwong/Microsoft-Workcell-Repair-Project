#!/usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from iiwa_msgs.msg import WorkcellCartesian
from moveit_commander.conversions import pose_to_list
from iiwa_msgs.srv import *


def all_close(goal, actual, tolerance):
  all_equal = True
  if type(goal) is list:
    for index in range(len(goal)):
      if abs(actual[index] - goal[index]) > tolerance:
        return False

  elif type(goal) is geometry_msgs.msg.PoseStamped:
    return all_close(goal.pose, actual.pose, tolerance)

  elif type(goal) is geometry_msgs.msg.Pose:
    return all_close(pose_to_list(goal), pose_to_list(actual), tolerance)

  return True


def update_pose_callback(data):
  pose_goal = geometry_msgs.msg.Pose()
  pose_goal.orientation.w = data.orientation_w
  pose_goal.orientation.x = data.orientation_x
  pose_goal.orientation.y = data.orientation_y
  pose_goal.orientation.z = data.orientation_z
  pose_goal.position.x = data.position_x
  pose_goal.position.y = data.position_y
  pose_goal.position.z = data.position_z
  group.set_pose_target(pose_goal)

  ## Now, we call the planner to compute the plan and execute it.
  plan = group.go(wait=True)
  # Calling `stop()` ensures that there is no residual movement
  group.stop()
  # It is always good to clear your targets after planning with poses.
  # Note: there is no equivalent function for clear_joint_value_targets()
  group.clear_pose_targets()


  current_pose = group.get_current_pose().pose
  print '=========current_pose %s' % current_pose
  return all_close(pose_goal, current_pose, 0.01)

def plan_cartesian_path(scale=1):
  print 'waiting for service...'
  rospy.wait_for_service('collect_pose')
  try:
    print 'trying'
    collect_pose = rospy.ServiceProxy('collect_pose', CollectPose)
    print 'pose collected'
    response = collect_pose(1)
    waypoints = []
    origin = group.get_current_pose().pose
    pose_goal = geometry_msgs.msg.Pose()
    pose_goal.orientation.w = response.orientation_w
    pose_goal.orientation.x = response.orientation_x
    pose_goal.orientation.y = response.orientation_y
    pose_goal.orientation.z = response.orientation_z
    pose_goal.position.x = response.position_x
    pose_goal.position.y = response.position_y
    pose_goal.position.z = response.position_z

    group.set_pose_target(pose_goal)
    plan = group.go(wait=True)
    group.stop()
    group.clear_pose_targets()

    wpose = group.get_current_pose().pose
    wpose.position.z -= scale * 0.1  # First move up (z)
    wpose.position.y += scale * 0.2  # and sideways (y)
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.x += scale * 0.1  # Second move forward/backwards in (x)
    waypoints.append(copy.deepcopy(wpose))

    wpose.position.y -= scale * 0.1  # Third move sideways (y)
    waypoints.append(copy.deepcopy(wpose))
    waypoints.append(copy.deepcopy(origin))
   
    # We want the Cartesian path to be interpolated at a resolution of 1 cm
    # which is why we will specify 0.01 as the eef_step in Cartesian
    # translation.  We will disable the jump threshold by setting it to 0.0 disabling:
    (plan, fraction) = group.compute_cartesian_path(
                                       waypoints,   # waypoints to follow
                                       0.01,        # eef_step
                                       0.0)         # jump_threshold

    # Note: We are just planning, not asking move_group to actually move the robot yet:
    group.execute(plan, wait=True)
  except rospy.ServiceException, e:
    print "service call failed: %s"%e

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial',
                anonymous=True)

## Instantiate a `RobotCommander`_ object. This object is the outer-level interface to
## the robot:
robot = moveit_commander.RobotCommander()

## Instantiate a `PlanningSceneInterface`_ object.  This object is an interface
## to the world surrounding the robot:
scene = moveit_commander.PlanningSceneInterface()

group_name = "manipulator"
group = moveit_commander.MoveGroupCommander(group_name)

## We create a `DisplayTrajectory`_ publisher which is used later to publish
## trajectories for RViz to visualize:
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                               moveit_msgs.msg.DisplayTrajectory,
                                               queue_size=20)

## END_SUB_TUTORIAL
#rospy.Subscriber('server_pose_chatter', WorkcellCartesian, plan_cartesian_path) 
## BEGIN_SUB_TUTORIAL basic_info
##
## Getting Basic Information
## ^^^^^^^^^^^^^^^^^^^^^^^^^
# We can get the name of the reference frame for this robot:
planning_frame = group.get_planning_frame()
print "============ Reference frame: %s" % planning_frame

# We can also print the name of the end-effector link for this group:
eef_link = group.get_end_effector_link()
print "============ End effector: %s" % eef_link

# We can get a list of all the groups in the robot:
group_names = robot.get_group_names()
print "============ Robot Groups:", robot.get_group_names()

# Sometimes for debugging it is useful to print the entire state of the
# robot:
print "============ Printing robot state"
print robot.get_current_state()
print ""
# Misc variables
box_name = ''


def go_to_pose_goal():
  pose_goal = geometry_msgs.msg.Pose()
  pose_goal.orientation.w = 1.0
  pose_goal.position.x = 0.2
  pose_goal.position.y = 0.4
  pose_goal.position.z = 0.5
  group.set_pose_target(pose_goal)

  ## Now, we call the planner to compute the plan and execute it.
  plan = group.go(wait=True)
  # Calling `stop()` ensures that there is no residual movement
  group.stop()
  # It is always good to clear your targets after planning with poses.
  # Note: there is no equivalent function for clear_joint_value_targets()
  group.clear_pose_targets()


  # For testing:
  # Note that since this section of code will not be included in the tutorials
  # we use the class variable rather than the copied state variable
  current_pose = group.get_current_pose().pose
  return all_close(pose_goal, current_pose, 0.01)



def main():
  try:
    print " Press get pose from service..."
    raw_input()
    plan_cartesian_path()

    print "============ Python tutorial demo complete!"
  except rospy.ROSInterruptException:
    return
  except KeyboardInterrupt:
    return

if __name__ == '__main__':
  main()
