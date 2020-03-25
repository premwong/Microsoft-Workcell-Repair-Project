#!/usr/bin/env python
import PyKDL
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from iiwa_msgs.msg import WorkcellCartesian
from iiwa_msgs.msg import GripperState
from moveit_commander.conversions import pose_to_list
from iiwa_msgs.srv import *
from moveit_msgs.msg import RobotState, Constraints, OrientationConstraint
from trajectory_msgs.msg import JointTrajectoryPoint
import transforms3d
import numpy as np 
import math
from urdf_parser_py.urdf import URDF
from pykdl_utils.kdl_parser import kdl_tree_from_urdf_model

# X_OFFSET = 0.047
# Y_OFFSET = 0.112

# X_OFFSET = -0.004
# Y_OFFSET = 0.0105
# Z_OFFSET = 0.18

X_OFFSET = 0.005
Y_OFFSET = -0.005
Z_OFFSET = 0.18
THETA_OFFSET = 0

HEATSINK_Z_OFFSET = 0.3
# A_OFFSET = 0.155
# B_OFFSET = -0.026
NIC_A = 0.113
NIC_B = -0.08

# NIC_A = -0.1033
# NIC_B = -0.0733



HEATSINK_A = -0.106
HEATSINK_B = -0.04

DIP_LENGTH = 0.085
RATE_LONG = 0.4
NUM_JOINTS = 7
MIN_JOINT_LIMITS_DEG = [-169, -119, -169, -119, -169, -119, -174]
MAX_JOINT_LIMITS_DEG = [169, 119, 169, 119, 169, 119, 174]
NIC_SEED_STATE = [1.987323522567749, 1.4358184337615967, -1.9114866256713867, -1.036642074584961, 1.578827142715454, 1.9280040264129639, -1.9716582298278809]
HDD_SEED_STATE = [0.4520516097545624, 0.9477099180221558, -2.3023149967193604, 2.0533716678619385, 2.569415330886841, -0.9975131750106812, 1.196797490119934]
# HEATSINK_SEED_STATE = [2.3536217212677, 1.9468990564346313, -1.464873194694519, -1.863680362701416, 0.37379294633865356, -1.1138713359832764, 0.020486973226070404]
#HEATSINK_SEED_STATE = [0.6797158718109131, 1.03727126121521, 0.2674739360809326, -1.6521695852279663, 1.8096520900726318, 1.2138895988464355, 1.9531116485595703] #march 14
# HEATSINK_SEED_STATE = [-1.1050864458084106, -1.9127799272537231, 1.4396296739578247, -1.8199113607406616, 0.30834999680519104, -1.5842403173446655, 0.20372463762760162]
HEATSINK_SEED_STATE = [-0.7379921078681946, -0.9803051352500916, -0.8230272531509399, 1.9625877141952515, 0.2715606093406677, 1.0199774503707886, 2.101893186569214]


#NIC card rotation matrix: [[sin_angle, -1 * cos_angle, 0], [-1 * cos_angle, -1 * sin_angle, 0], [0, 0, -1]]
#Heat sink rotation matrix: 
heat_sink_rotation = [[1, 0, 0], [0, 0, 1], [0, -1, 0]]

MANUAL_STEP = 0.002

PLANNER_ID = 'RRTConnectkConfigDefault'

current_theta = 0

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
  pose_goal.position.z = data.position_zoveit_msgs.Constraints()
  group.set_pose_target(pose_goal)
  plan = group.go(wait=True)
  group.stop()
  group.clear_pose_targets()
  current_pose = group.get_current_pose().pose
  print '=========current_pose %s' % current_pose
  return all_close(pose_goal, current_pose, 0.01)

def relative_position(a, b, theta):
  x = (math.cos(theta) * a) + (-1 * math.sin(theta) * b)
  y = (math.sin(theta) * a) + (math.cos(theta) * b)
  return x, y

def nic_convert_to_quaternion_orientation(theta):
  cos_angle = math.cos(theta)
  sin_angle = math.sin(theta)
  rotation_mat = np.array([[sin_angle, -1 * cos_angle, 0], [-1 * cos_angle, -1 * sin_angle, 0], [0, 0, -1]])
  quat = transforms3d.quaternions.mat2quat(rotation_mat)
  return quat

def heatsink_convert_to_quaternion_orientation(theta):
  cos_angle = math.cos(theta)
  sin_angle = math.sin(theta)
  rotation_mat = np.array([[cos_angle, 0, sin_angle], [sin_angle, 0, -1 * cos_angle], [0, 1, 0]])
  quat = transforms3d.quaternions.mat2quat(np.array(heat_sink_rotation))
  return quat

def goto_nic_position(query=True, scale=1):
  global current_theta
  print 'plan 1'
  print 'waiting for service...'
  rospy.wait_for_service('collect_pose')
  if (query):
    try:
      print 'trying'
      collect_pose = rospy.ServiceProxy('collect_pose', CollectPose)
      response = collect_pose(1)
      print 'pose collected'
      print response
      theta_rad = response.orientation_theta
      print theta_rad
      current_theta = math.degrees(theta_rad) + THETA_OFFSET
      coord_offset = relative_position(NIC_A, NIC_B, theta_rad + math.radians(THETA_OFFSET))
      return goto_cartesian_state((response.position_x + X_OFFSET) + coord_offset[0], (response.position_y + Y_OFFSET) + coord_offset[1], Z_OFFSET, theta_rad + math.radians(THETA_OFFSET), 'nic', True)
    except rospy.ServiceException, e:
      print "service call failed: %s"%e

def goto_heatsink_position(query=True, scale=1):
  global current_theta
  print 'plan 1'
  print 'waiting for service...'
  rospy.wait_for_service('collect_pose')
  if (query):
    try:
      print 'trying'
      collect_pose = rospy.ServiceProxy('collect_pose', CollectPose)
      response = collect_pose(1)
      print 'pose collected'
      print response
      theta_rad = response.orientation_theta
      current_theta = math.degrees(theta_rad) + THETA_OFFSET
      coord_offset = relative_position(HEATSINK_A, HEATSINK_B, theta_rad + math.radians(THETA_OFFSET))
      print response.position_x + X_OFFSET + coord_offset[0]
      print response.position_y + Y_OFFSET + coord_offset[1]
      return goto_cartesian_state((response.position_x + X_OFFSET) + coord_offset[0], (response.position_y + Y_OFFSET) + coord_offset[1] , HEATSINK_Z_OFFSET, theta_rad + math.radians(THETA_OFFSET), 'heatsink', True)
    except rospy.ServiceException, e:
      print "service call failed: %s"%e

def goto_joint_state(joint_vals):
  joint_goal = group.get_current_joint_values()
  for idx, joint in enumerate(joint_vals):
    joint_goal[idx] = joint
  print joint_goal
  plan = group.go(joint_goal, wait=True)
  group.stop()
  return plan

def goto_cartesian_state(x, y, z, theta, type='nic', radians=False):
  if type == 'nic':
    if radians:
      quat = nic_convert_to_quaternion_orientation(theta).tolist()
    else:
      quat = nic_convert_to_quaternion_orientation(math.radians(theta)).tolist()
    joint_goal = inverse_kinematics([x, y, z], [ quat[1], quat[2], quat[3], quat[0]], NIC_SEED_STATE)
    return goto_joint_state(joint_goal)
  elif type == 'heatsink':
    if radians:
      quat = heatsink_convert_to_quaternion_orientation(theta).tolist()
    else:
      quat = heatsink_convert_to_quaternion_orientation(math.radians(theta)).tolist()
    joint_goal = inverse_kinematics([x, y, z], [ quat[1], quat[2], quat[3], quat[0]], HEATSINK_SEED_STATE)
    return goto_joint_state(joint_goal)


def set_gripper(state):
  rospy.sleep(0.5)
  gripper_state = GripperState()
  gripper_state.open = state
  rate = rospy.Rate(10)
  gripper_io_publisher.publish(gripper_state)
  rate.sleep()
  gripper_io_publisher.publish(gripper_state)
  rospy.sleep(0.5)

def display_trajectory(plan):
  my_display = DisplayTrajectory()
  my_display.trajectory = plan.joint_trajectory

  display_trajectory_publisher.publish()

#------control init begin-------------------------------------------------------------------------
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('iiwa_move_to_ee_pose', anonymous=True)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group_name = "manipulator"
group = moveit_commander.MoveGroupCommander(group_name)
#group.set_max_velocity_scaling_factor(0.15)
group.set_max_acceleration_scaling_factor(0.1)
print group.set_planner_id(PLANNER_ID)
group.set_num_planning_attempts(100)
group.set_planning_time(3)
group.set_start_state_to_current_state()
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)
gripper_io_publisher = rospy.Publisher('command/GripperState', iiwa_msgs.msg.GripperState, queue_size=10)
rate_long = rospy.Rate(RATE_LONG)
upright_constraints = Constraints()
try:
  rospy.wait_for_service('configuration/setSmartServoLimits', 1)
except:
  print 'timeout'
try:
  print 'trying'
  set_speed_limits = rospy.ServiceProxy('configuration/setSmartServoLimits', SetSmartServoJointSpeedLimits)
  response = set_speed_limits(0.3, 0.2, -1)
  print 'speed limit set'
  print response
except rospy.ServiceException, e:
  print "service call failed: %s"%e
#-------control init end-------------------------------------------------------------------------

#-------inverse kinematics init begin -----------------------------------------------------------
iiwa_URDF = URDF.from_parameter_server(key='robot_description')
iiwa_kdl_tree = kdl_tree_from_urdf_model(iiwa_URDF)
iiwa_base_link = iiwa_URDF.get_root()
iiwa_chain = iiwa_kdl_tree.getChain(iiwa_base_link, 'tool_link_ee')

_forward_kin_position_kdl = PyKDL.ChainFkSolverPos_recursive(iiwa_chain)
_forward_kin_velocity_kdl = PyKDL.ChainFkSolverVel_recursive(iiwa_chain)  
_inverse_kin_velocity_kdl = PyKDL.ChainIkSolverVel_pinv(iiwa_chain)
min_limits = PyKDL.JntArray(NUM_JOINTS)
max_limits = PyKDL.JntArray(NUM_JOINTS)
for idx, jnt in enumerate(MIN_JOINT_LIMITS_DEG):
  min_limits[idx] = math.radians(jnt)
for idx, jnt in enumerate(MAX_JOINT_LIMITS_DEG):
  max_limits[idx] = math.radians(jnt)
_inverse_kin_position_kdl = PyKDL.ChainIkSolverPos_NR_JL(iiwa_chain, min_limits, max_limits, _forward_kin_position_kdl, _inverse_kin_velocity_kdl)

#-------inverse kinematics init end ----------------------------------------------------------------

def print_state():
  planning_frame = group.get_planning_frame()
  print "Reference frame: %s" % planning_frame
  eef_link = group.get_end_effector_link()
  print "End effector: %s" % eef_link
  group_names = robot.get_group_names()
  print "Robot Groups:", robot.get_group_names()
  print "Printing robot state"
  print robot.get_current_state()
  print "Robot Joint values"
  print group.get_current_joint_values()
  print ""

# def interpolated_path_down(travel_distance):
#   cur_pose = group.get_current_pose().pose
#   z_state = cur_pose.position.z
#   waypoints = []
#   for i in range(0, int(travel_distance / 0.005)):
#     wpose = copy.deepcopy(cur_pose)
#     wpose.position.z = z_state - 0.005
#     waypoints.append(wpose)
#     z_state -= 0.005
#   print waypoints
#   (plan, fraction) = group.compute_cartesian_path(waypoints, 0.0001, 0.0)
#   new_plan = extend_trajectory(plan, group.get_current_pose().pose)
#   group.execute(new_plan, wait=True)
#   return plan


def extended_trajectory(travel_distance):
  cur_pose = group.get_current_pose().pose
  z_state = cur_pose.position.z
  waypoints = []
  wpose = copy.deepcopy(cur_pose)
  wpose.position.z += 0.0001
  waypoints.append(wpose)
  print waypoints
  (plan, fraction) = group.compute_cartesian_path(waypoints, 0.03, 0.0)
  extend_trajectory(plan, copy.deepcopy(wpose), travel_distance)
  print plan
  group.execute(plan, wait=True)
  return plan

def manually_interpolated_down(count=13, theta=None):
  global current_theta
  new_theta = theta
  if new_theta == None:
    new_theta = current_theta
  cur_pose = group.get_current_pose().pose
  cur_z = cur_pose.position.z
  for i in range(0, count):
    goto_cartesian_state(cur_pose.position.x, cur_pose.position.y, cur_z - MANUAL_STEP, new_theta)
    cur_z -= 0.002
    rospy.sleep(0.01)
  return True;

def heatsink_manually_interpolated_down(count=13, theta=None):
  global current_theta
  new_theta = theta
  if new_theta == None:
    new_theta = current_theta
  cur_pose = group.get_current_pose().pose
  cur_z = cur_pose.position.z
  for i in range(0, count):
    goto_cartesian_state(cur_pose.position.x, cur_pose.position.y, cur_z - MANUAL_STEP, 'heatsink', new_theta)
    cur_z -= 0.002
    rospy.sleep(0.01)
  return True;


def remove_path_constraints():
  print 'Constraint removed: ' + str(upright_constraints.orientation_constraints.pop())
  group.set_path_constraints(upright_constraints)

def init_path_constraints():
  upright_constraints.name = 'upright'
  orientation_constraint = OrientationConstraint()    # goto_cartesian_state(0.1, 0.8, 0.3, 0, 'heatsink')
    # rospy.sleep(2)
  current_pose = group.get_current_pose().pose
  planning_frame = group.get_planning_frame()
  orientation_constraint.header.frame_id = planning_frame
  orientation_constraint.link_name = group.get_end_effector_link()
  print 'Constraint initialized: ' + str(orientation_constraint.link_name)
  orientation_constraint.orientation = current_pose.orientation    
  orientation_constraint.absolute_x_axis_tolerance = 0.001
  orientation_constraint.absolute_y_axis_tolerance = 0.001
  orientation_constraint.absolute_z_axis_tolerance = 0.001
  orientation_constraint.weight = 0.01
  upright_constraints.orientation_constraints.append(orientation_constraint)
  group.set_path_constraints(upright_constraints)


def inverse_kinematics(position, orientation=None, seed=None):
  ik = PyKDL.ChainIkSolverVel_pinv(iiwa_chain)
  pos = PyKDL.Vector(position[0], position[1], position[2])
  if orientation != None:
    rot = PyKDL.Rotation()
    rot = rot.Quaternion(orientation[0], orientation[1],
                         orientation[2], orientation[3])
  # Populate seed with current angles if not provided
  seed_array = PyKDL.JntArray(NUM_JOINTS)
  if seed != None:
    seed_array.resize(len(seed))
    for idx, jnt in enumerate(seed):
      seed_array[idx] = jnt
  else:
    joint_vals = group.get_current_joint_values()
    for idx, jnt in enumerate(joint_vals):
      seed_array[idx] = joint_vals[idx]
  # Make IK Call
  if orientation:
    goal_pose = PyKDL.Frame(rot, pos)
  else:
    goal_pose = PyKDL.Frame(pos)
  result_angles = PyKDL.JntArray(NUM_JOINTS)
  if _inverse_kin_position_kdl.CartToJnt(seed_array, goal_pose, result_angles) >= 0:
    result = np.array(result_angles).tolist()
    return result
  else:
    print 'No IK Solution Found'
    return None

def extend_trajectory(plan, start_pose, travel_distance, step=0.005, time_step=0.04):
  traj = plan.joint_trajectory.points
  cur_pose_z = start_pose.position.z 
  start_time = plan.joint_trajectory.points[-1].time_from_start
  if (direction == 'down'):
    for i in range(0, int(abs(travel_distance) / step)):
      point = JointTrajectoryPoint()
      print i
      joint_goal = inverse_kinematics([start_pose.position.x, start_pose.position.y, cur_pose_z + (numpy.sign(travel_distance) * step)], 
        [start_pose.orientation.x, start_pose.orientation.y, start_pose.orientation.z, start_pose.orientation.w], NIC_SEED_STATE)
      joint_list = []
      for idx, jnt in enumerate(joint_goal):
        joint_list.append(jnt)
      point.positions = joint_list
      print joint_list
      point.velocities = [0.0, 0.01, 0.01, 0.01, 0.01, 0.01, 0.0]
      point.accelerations = [0,0,0,0,0,0,0]
      time = rospy.Duration.from_sec(start_time.to_sec() + (numpy.sign(travel_distance) * time_step))
      start_time += rospy.Duration.from_sec(time_step)
      point.time_from_start = time
      traj.append(point)
      cur_pose_z += step
  return plan


def main():
  print_state()
  try:
    print " Press to start sequence"
    raw_input()
    # init_path_constraints()
    # interpolated_path_up(0.13)
    # set_gripper(True)
    # if goto_nic_position():
    #   set_gripper(True)
    #   rospy.sleep(1)
    #   if interpolated_path_down(0.06):
    #     rospy.sleep(1)
    #     if manually_interpolated_down():
    #       set_gripper(False)
    #       if manually_interpolated_up():
    #         rospy.sleep(1)
    #         if goto_cartesian_state(0.4, 0.3, 0.11, 270):
    #           rospy.sleep(2)
    #           interpolated_path_down(0.4)
    #           rospy.sleep(1)
    #           set_gripper(True)
    # goto_cartesian_state(0.01, 0.8, 0.3, 0, 'heatsink')
    # rospy.sleep(3)
    # interpolated_path_down(0.129)
    # rospy.sleep(1)
    # set_gripper(False)
    # interpolated_path_up(0.13)
    # rospy.sleep(1)
    # goto_cartesian_state(0.3, 0.4, 0.11, 270)
    # rospy.sleep(2)
    # interpolated_path_down(0.4)
    # rospy.sleep(1)
    # set_gripper(True)



    #-------------------------pick up ----------------------
    if goto_nic_position():
      set_gripper(True)
      rospy.sleep(2)
    extended_trajectory(0.06)
    # rospy.sleep(2)
    # extended_trajectory(0.1, 'up')
      # if interpolated_path_down(0.06):
      #   rospy.sleep(1)
      #   if manually_interpolated_down():
      #     set_gripper(False)
      #     if manually_interpolated_up():
      #       rospy.sleep(2)
      #       if goto_cartesian_state(0.4, 0.3, 0.3, 270):
      #         rospy.sleep(2)
      #         raw_input()
      #         #-------------------place ----------------------------
      #         if goto_nic_position():
      #           rospy.sleep(2)
      #           if interpolated_path_down(0.06):
      #             rospy.sleep(1)
      #             if manually_interpolated_down():
      #               set_gripper(True)
      #               if manually_interpolated_up():
      #                 rospy.sleep(1)
      #                 if goto_cartesian_state(0.4, 0.2, 0.11, 270):
      #                   rospy.sleep(2)
    print "=============Sequence complete============="
  except rospy.ROSInterruptException:
    return
  except KeyboardInterrupt:
    return

if __name__ == '__main__':
  main()
