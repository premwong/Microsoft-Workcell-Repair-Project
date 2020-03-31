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


X_OFFSET = -0.021
Y_OFFSET = 0.0055
Z_OFFSET = 0.14
THETA_OFFSET = 1

HEATSINK_Z_OFFSET = 0.3
# A_OFFSET = 0.155
# B_OFFSET = -0.026
NIC_A = 0.076
NIC_B = -0.08

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
HEATSINK_ROTATION = [[1, 0, 0], [0, 0, 1], [0, -1, 0]]

MANUAL_STEP = 0.002

PLANNER_ID = 'RRTConnectkConfigDefault'


current_theta = 0

class MoveGroupLeftArm(object):
  def __init__(self):
    super(MoveGroupLeftArm, self).__init__()
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('iiwa_move_to_ee_pose', anonymous=True)
    self.robot = moveit_commander.RobotCommander()
    self.scene = moveit_commander.PlanningSceneInterface()
    group_name = "manipulator"
    self.group = moveit_commander.MoveGroupCommander(group_name)
    #group.set_max_velocity_scaling_factor(0.15)
    self.group.set_max_acceleration_scaling_factor(0.1)
    print self.group.set_planner_id(PLANNER_ID)
    self.group.set_num_planning_attempts(100)
    self.group.set_planning_time(3)
    self.group.set_start_state_to_current_state()
    self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)
    self.gripper_io_publisher = rospy.Publisher('command/GripperState', iiwa_msgs.msg.GripperState, queue_size=10)
    self.rate_long = rospy.Rate(RATE_LONG)
    self.upright_constraints = Constraints()
    try:
      rospy.wait_for_service('configuration/setSmartServoLimits', 1)
    except:
      print 'timeout'
    try:
      print 'trying'
      self.set_speed_limits = rospy.ServiceProxy('configuration/setSmartServoLimits', SetSmartServoJointSpeedLimits)
      response = self.set_speed_limits(0.2, 0.2, -1)
      print 'speed limit set'
      print response
    except rospy.ServiceException, e:
      print "service call failed: %s"%e
    _iiwa_URDF = URDF.from_parameter_server(key='robot_description')

    _iiwa_kdl_tree = kdl_tree_from_urdf_model(_iiwa_URDF)
    _iiwa_base_link = _iiwa_URDF.get_root()
    self.iiwa_chain = _iiwa_kdl_tree.getChain(_iiwa_base_link, 'tool_link_ee')

    self.forward_kin_position_kdl = PyKDL.ChainFkSolverPos_recursive(self.iiwa_chain)
    _forward_kin_velocity_kdl = PyKDL.ChainFkSolverVel_recursive(self.iiwa_chain)  
    self.inverse_kin_velocity_kdl = PyKDL.ChainIkSolverVel_pinv(self.iiwa_chain)
    self.min_limits = PyKDL.JntArray(NUM_JOINTS)
    self.max_limits = PyKDL.JntArray(NUM_JOINTS)
    for idx, jnt in enumerate(MIN_JOINT_LIMITS_DEG):
      self.min_limits[idx] = math.radians(jnt)
    for idx, jnt in enumerate(MAX_JOINT_LIMITS_DEG):
      self.max_limits[idx] = math.radians(jnt)
    # self.inverse_kin_position_kdl = PyKDL.ChainIkSolverPos_NR_JL(self.iiwa_chain, min_limits, max_limits, _forward_kin_position_kdl, _inverse_kin_velocity_kdl)

  def inverse_kinematics(self, position, orientation=None, seed=None):
    _inverse_kin_position_kdl = PyKDL.ChainIkSolverPos_NR_JL(self.iiwa_chain, self.min_limits, self.max_limits, self.forward_kin_position_kdl, self.inverse_kin_velocity_kdl)
    ik = PyKDL.ChainIkSolverVel_pinv(self.iiwa_chain)
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
      joint_vals = self.group.get_current_joint_values()
      for idx, jnt in enumerate(joint_vals):
        seed_array[idx] = joint_vals[idx]
    # Make IK Call
    if orientation:
      goal_pose = PyKDL.Frame(rot, pos)
    else:
      goal_pose = PyKDL.Frame(pos)
    result_angles = PyKDL.JntArray(NUM_JOINTS)
    print seed_array
    print goal_pose
    print result_angles
    if _inverse_kin_position_kdl.CartToJnt(seed_array, goal_pose, result_angles) >= 0:
      result = np.array(result_angles).tolist()
      return result
    else:
      print 'No IK Solution Found'
      return None

  def relative_position(self, a, b, theta):
    x = (math.cos(theta) * a) + (-1 * math.sin(theta) * b)
    y = (math.sin(theta) * a) + (math.cos(theta) * b)
    return x, y

  def nic_convert_to_quaternion_orientation(self, theta):
    cos_angle = math.cos(theta)
    sin_angle = math.sin(theta)
    rotation_mat = np.array([[sin_angle, -1 * cos_angle, 0], [-1 * cos_angle, -1 * sin_angle, 0], [0, 0, -1]])
    quat = transforms3d.quaternions.mat2quat(rotation_mat)
    return quat

  def goto_nic_position(self, query=True, scale=1):
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
        coord_offset = self.relative_position(NIC_A, NIC_B, theta_rad + math.radians(THETA_OFFSET))
        return self.goto_cartesian_state((response.position_x + X_OFFSET) + coord_offset[0], (response.position_y + Y_OFFSET) + coord_offset[1], 
          Z_OFFSET, theta_rad + math.radians(THETA_OFFSET), 'nic', True)
      except rospy.ServiceException, e:
        print "service call failed: %s"%e

  def goto_joint_state(self, joint_vals):
    joint_goal = self.group.get_current_joint_values()
    for idx, joint in enumerate(joint_vals):
      joint_goal[idx] = joint
    print joint_goal
    plan = self.group.go(joint_goal, wait=True)
    self.group.stop()
    return plan

  def goto_cartesian_state(self, x, y, z, theta, type='nic', radians=False):
    if type == 'nic':
      if radians:
        quat = self.nic_convert_to_quaternion_orientation(theta).tolist()
      else:
        quat = self.nic_convert_to_quaternion_orientation(math.radians(theta)).tolist()
      joint_goal = self.inverse_kinematics([x, y, z], [ quat[1], quat[2], quat[3], quat[0]], NIC_SEED_STATE)
      return self.goto_joint_state(joint_goal)
    elif type == 'heatsink':
      if radians:
        quat = self.heatsink_convert_to_quaternion_orientation(theta).tolist()
      else:
        quat = self.heatsink_convert_to_quaternion_orientation(math.radians(theta)).tolist()
      joint_goal = self.inverse_kinematics([x, y, z], [ quat[1], quat[2], quat[3], quat[0]], HEATSINK_SEED_STATE)
      return self.goto_joint_state(joint_goal)


  def set_gripper(self, state):
    rospy.sleep(0.5)
    gripper_state = GripperState()
    gripper_state.open = state
    rate = rospy.Rate(10)
    self.gripper_io_publisher.publish(gripper_state)
    rate.sleep()
    self.gripper_io_publisher.publish(gripper_state)
    rospy.sleep(0.5)

  def print_state(self):
    planning_frame = self.group.get_planning_frame()
    print "Reference frame: %s" % planning_frame
    eef_link = self.group.get_end_effector_link()
    print "End effector: %s" % eef_link
    group_names = self.robot.get_group_names()
    print "Robot Groups:", self.robot.get_group_names()
    print "Printing robot state"
    print self.robot.get_current_state()
    print "Robot Joint values"
    print self.group.get_current_joint_values()
    print ""

  def extend_trajectory(self, travel_distance):
    cur_pose = self.group.get_current_pose().pose
    z_state = cur_pose.position.z
    waypoints = []
    wpose = copy.deepcopy(cur_pose)
    wpose.position.z += 0.0001
    waypoints.append(wpose)
    print waypoints
    (plan, fraction) = self.group.compute_cartesian_path(waypoints, 0.03, 0.0)
    self.extend_trajectory_helper(plan, copy.deepcopy(wpose), travel_distance)
    print plan
    self.group.execute(plan, wait=True)
    return plan

  def manually_interpolated_down(count=13, theta=None):
    global current_theta
    new_theta = theta
    if new_theta == None:
      new_theta = current_theta
    cur_pose = self.group.get_current_pose().pose
    cur_z = cur_pose.position.z
    for i in range(0, count):
      goto_cartesian_state(cur_pose.position.x, cur_pose.position.y, cur_z - MANUAL_STEP, new_theta)
      cur_z -= 0.002
      rospy.sleep(0.01)
    return True


  def remove_path_constraints(self):
    print 'Constraint removed: ' + str(self.upright_constraints.orientation_constraints.pop())
    self.group.set_path_constraints(self.upright_constraints)

  def init_path_constraints(self):
    self.upright_constraints.name = 'upright'
    orientation_constraint = OrientationConstraint()    
    current_pose = self.group.get_current_pose().pose
    planning_frame = self.group.get_planning_frame()
    orientation_constraint.header.frame_id = planning_frame
    orientation_constraint.link_name = self.group.get_end_effector_link()
    print 'Constraint initialized: ' + str(orientation_constraint.link_name)
    orientation_constraint.orientation = current_pose.orientation    
    orientation_constraint.absolute_x_axis_tolerance = 0.001
    orientation_constraint.absolute_y_axis_tolerance = 0.001
    orientation_constraint.absolute_z_axis_tolerance = 0.001
    orientation_constraint.weight = 0.01
    self.upright_constraints.orientation_constraints.append(orientation_constraint)
    self.group.set_path_constraints(self.upright_constraints)


  def extend_trajectory_helper(self, plan, start_pose, travel_distance, step=0.005, time_step=0.004):
    traj = plan.joint_trajectory.points
    cur_pose_z = start_pose.position.z 
    start_time = plan.joint_trajectory.points[-1].time_from_start
    for i in range(0, int(abs(travel_distance) / step)):
      point = JointTrajectoryPoint()
      print i
      joint_goal = self.inverse_kinematics([start_pose.position.x, start_pose.position.y, cur_pose_z + (np.sign(travel_distance) * step)], 
        [start_pose.orientation.x, start_pose.orientation.y, start_pose.orientation.z, start_pose.orientation.w], NIC_SEED_STATE)
      joint_list = []
      for idx, jnt in enumerate(joint_goal):
        joint_list.append(jnt)
      point.positions = joint_list
      print joint_list
      point.velocities = [0.0, 0.01, 0.01, 0.01, 0.01, 0.01, 0.0]
      point.accelerations = [0,0,0,0,0,0,0]
      time = rospy.Duration.from_sec(start_time.to_sec() + time_step)
      start_time += rospy.Duration.from_sec(time_step)
      point.time_from_start = time
      traj.append(point)
      cur_pose_z += np.sign(travel_distance) * step
    return plan


def main():
  myLeftArm = MoveGroupLeftArm()
  # myLeftArm.init_path_constraints()
  myLeftArm.print_state()
  try:
    print " Press to start sequence"
    raw_input()
    # myLeftArm.goto_cartesian_state(0.4, 0.3, 0.3, 270)
    myLeftArm.extend_trajectory(-0.06)

  except rospy.ROSInterruptException:
    return
  except KeyboardInterrupt:
    return

if __name__ == '__main__':
  main()
