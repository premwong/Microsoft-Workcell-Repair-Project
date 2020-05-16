#!/usr/bin/env python

"""
@Author: Nano Premvuti @premwong
University of Washington 2020
Department of Electrical & Computer Engineering

This is the control module for the left workcell iiwa arm
"""
import yaml
import os
import PyKDL
import sys
import time
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from iiwa_msgs.msg import WorkcellCartesian, GripperState
from moveit_commander.conversions import pose_to_list
from iiwa_msgs.srv import *
from moveit_msgs.msg import RobotState, Constraints, OrientationConstraint
from trajectory_msgs.msg import JointTrajectoryPoint
import transforms3d
import numpy as np 
import math
from urdf_parser_py.urdf import URDF
from pykdl_utils.kdl_parser import kdl_tree_from_urdf_model
from config import *

#TODO: calculate HDD rotation 
current_theta = 0

class Component(object):
  """helper class for components"""
  def __init__(self, component_name, component_offset, seed_state, rotation_function, tray_pose, angle_offset=0, component_id=None):
    super(Component, self).__init__()
    self.component_name = component_name
    self.component_a_offset = component_offset[0] # x offset from on-server fiducial 
    self.component_b_offset = component_offset[1] # y offset from on-server fiducial
    self.component_z_offset = component_offset[2]
    self.component_id = component_id
    self.seed_state = seed_state
    self.rotation_function = rotation_function
    self.tray_pose = tray_pose
    self.angle_offset = angle_offset
  def get_relative_position(self, theta):
    x = (math.cos(theta) * self.component_a_offset) + (-1 * math.sin(theta) * self.component_b_offset)
    y = (math.sin(theta) * self.component_a_offset) + (math.cos(theta) * self.component_b_offset)
    return x, y

  #w, x, y, z-------------------
    super(MoveGroupLeftArm, self).__init__()
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('iiwa_move_to_ee_pose', anonymous=True)
    self.robot = moveit_commander.RobotCommander()
  def convert_theta_to_quaternion(self, theta):
    cos_angle = math.cos(theta + math.radians(self.angle_offset))
    sin_angle = math.sin(theta + math.radians(self.angle_offset))
    rotation_mat_array = np.array(self.rotation_function(sin_angle, cos_angle))
    quat = transforms3d.quaternions.mat2quat(rotation_mat_array)
    return quat.tolist()

  def get_seed_state(self):
    return self.seed_state

  def get_z_offset(self):
    return self.component_z_offset

  def get_rotation_function(self):
    return self.rotation_function

class MoveGroupLeftArm(object):
  def __init__(self):
    #----------------control init begin-----------------------------------------------
    super(MoveGroupLeftArm, self).__init__()
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('iiwa_move_to_ee_pose', anonymous=True)
    self.robot = moveit_commander.RobotCommander()
    self.scene = moveit_commander.PlanningSceneInterface()
    group_name = "manipulator"
    self.group = moveit_commander.MoveGroupCommander(group_name)
    #group.set_max_velocity_scaling_factor(0.15)
    self.group.set_max_acceleration_scaling_factor(0.1)
    if self.group.set_planner_id(PLANNER_ID): 
      print "Using planner: %s" % PLANNER_ID
    self.group.set_num_planning_attempts(100)
    self.group.set_planning_time(3)
    self.group.set_start_state_to_current_state()
    self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)
    self.gripper_io_publisher = rospy.Publisher('command/GripperState', iiwa_msgs.msg.GripperState, queue_size=10)
    self.upright_constraints = Constraints()
    try:
      rospy.wait_for_service('configuration/setSmartServoLimits', 1)
    except:
      print 'Service call timeout'
    try:
      self.set_speed_limits = rospy.ServiceProxy('configuration/setSmartServoLimits', SetSmartServoJointSpeedLimits)
      response = self.set_speed_limits(VELOCITY_SCALE, 0.1, -1)
      print 'Velocity limit set'
      print response
    except rospy.ServiceException, e:
      print "service call failed: %s"%e
    #----------------kinematics init begin---------------------------------------------
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
    self.component_map = {}

  def load_component_map(self, components):
    """declare and load components here"""
    for component in components:
      self.component_map[component.component_name] = component
    return self.component_map

  def __inverse_kinematics(self, position, orientation=None, seed=None):
    """inverse kinematic solver using PyKDL"""
    _inverse_kin_position_kdl = PyKDL.ChainIkSolverPos_NR_JL(self.iiwa_chain, self.min_limits, self.max_limits, 
      self.forward_kin_position_kdl, self.inverse_kin_velocity_kdl)
    ik = PyKDL.ChainIkSolverVel_pinv(self.iiwa_chain)
    pos = PyKDL.Vector(position[0], position[1], position[2])
    if orientation != None:
      rot = PyKDL.Rotation()
      #PyKDL uses w, x, y, z instead of x, y, z, w
      rot = rot.Quaternion(orientation[1], orientation[2], orientation[3], orientation[0])
    seed_array = PyKDL.JntArray(NUM_JOINTS)
    if seed != None:
      seed_array.resize(len(seed))
      for idx, jnt in enumerate(seed):
        seed_array[idx] = jnt
    else:
      joint_vals = self.group.get_current_joint_values()
      for idx, jnt in enumerate(joint_vals):
        seed_array[idx] = joint_vals[idx]
    if orientation:
      goal_pose = PyKDL.Frame(rot, pos)
    else:
      goal_pose = PyKDL.Frame(pos)
    result_angles = PyKDL.JntArray(NUM_JOINTS)
    if _inverse_kin_position_kdl.CartToJnt(seed_array, goal_pose, result_angles) >= 0:
      result = np.array(result_angles)
      return result
    else:
      print 'No IK Solution Found'
      return None

  def query_pose_and_check_ik(self):
    response = self.query_pose()
    theta_rad = response.orientation_theta
    return self.check_ik_validity([response.position_x + GLOBAL_OFFSET[0], response.position_y + GLOBAL_OFFSET[1]], theta_rad)

  def check_ik_validity(self, server_position, server_orientation): 
    """checks server pose for IK validity for all components"""
    failed_components = []
    for component in self.component_map:
      component_position = self.component_map[component].get_relative_position(server_orientation)
      component_z_offset = self.component_map[component].get_z_offset()
      component_quaternion = self.component_map[component].convert_theta_to_quaternion(server_orientation)
      if self.__inverse_kinematics([server_position[0] + component_position[0] + GLOBAL_OFFSET[0], 
      server_position[1] + component_position[1] + GLOBAL_OFFSET[1], component_z_offset],
       component_quaternion, self.component_map[component].get_seed_state()) == None:
        failed_components.append(self.component_map[component].component_name)
    return failed_components

  def query_pose(self, query=True):
    global current_theta
    print 'Waiting for service...'
    rospy.wait_for_service('collect_pose')
    if (query):
      try:
        collect_pose = rospy.ServiceProxy('collect_pose', CollectPose)
        return collect_pose(1)
      except rospy.ServiceException, e:
        print "Service call failed: %s"%e

  def goto_fiducial_position(self):
    global current_theta
    response = self.query_pose()
    print 'Pose collected.'
    print response
    theta_rad = response.orientation_theta
    current_theta = theta_rad
    print math.degrees(current_theta)
    goal_quaternion = self.component_map['nic'].convert_theta_to_quaternion(current_theta)
    return self.goto_goal_state(response.position_x + GLOBAL_OFFSET[0], response.position_y + GLOBAL_OFFSET[1], Z_OFFSET, 
    goal_quaternion, self.component_map['nic'].get_seed_state())

  def goto_component_position(self, component_name, scale=1):
    global current_theta
    response = self.query_pose() 
    print 'Pose collected.'
    print response
    theta_rad = response.orientation_theta
    print theta_rad
    current_theta = theta_rad + THETA_OFFSET
    coord_offset = self.component_map[component_name].get_relative_position(current_theta)
    goal_quaternion = self.component_map[component_name].convert_theta_to_quaternion(current_theta)
    goal_x = response.position_x + GLOBAL_OFFSET[0] + coord_offset[0]
    goal_y = response.position_y + GLOBAL_OFFSET[1] + coord_offset[1]
    return self.goto_goal_state(goal_x, goal_y, Z_OFFSET, 
      goal_quaternion, self.component_map[component_name].get_seed_state())

  def goto_component_tray(self, component_name):
    component = self.component_map[component_name]
    goal_x = component.tray_pose[0]
    goal_y = component.tray_pose[1]
    goal_quaternion = component.convert_theta_to_quaternion(component.tray_pose[2])
    return self.goto_goal_state(goal_x, goal_y, 0.14, goal_quaternion, self.component_map[component_name].get_seed_state())

  def goto_joint_state(self, joint_vals, save_name=None):
    joint_goal = self.group.get_current_joint_values()
    joint_goal_degrees = self.group.get_current_joint_values()
    for idx, joint in enumerate(joint_vals.tolist()):
      joint_goal[idx] = joint
      joint_goal_degrees[idx] = math.degrees(joint)
    if save_name != None:
      self.group.set_joint_value_target(joint_goal)
      plan = self.group.plan()
      self.__save_trajectory(plan, save_name)
      return plan
    else:
      start_time = time.time()
      print 'joint goal %s' % joint_goal_degrees
      plan = self.group.go(joint_goal, wait=True)
      self.group.stop()
      print 'goto joint state%s'%self.group.get_current_pose().pose
      end_time = time.time()
      rospy.sleep((end_time - start_time) * 0.5)
      print '----------------------'
      return plan

  def goto_home_state(self):
    self.goto_joint_state(HOME_STATE)

  def goto_goal_state(self, x, y, z, quat, seed_state, radians=False, save_name=None):
    joint_goal = self.__inverse_kinematics([x, y, z], quat, seed_state)
    joint_list = joint_goal.tolist()
    joint_7 = joint_list[6]
    joint_list[6] = joint_7 + math.radians(0)
    print 'joint7%s'% math.degrees(joint_7)
    joint_goal = np.array(joint_list)
    return self.goto_joint_state(joint_goal, save_name)

  #For testing only. Do not use on final version
  def goto_cartesian_state(self, goal_x, goal_y, goal_z, goal_theta, component_name='nic', radians=False):
    goal_quaternion = self.component_map[component_name].convert_theta_to_quaternion(math.radians(goal_theta))
    return self.goto_goal_state(goal_x, goal_y, goal_z, 
      goal_quaternion, self.component_map[component_name].get_seed_state())

  def goto_cartesian_state_save(self, goal_x, goal_y, goal_z, goal_theta, plan_name='plan', component_name='nic'):
    goal_quaternion = self.component_map[component_name].convert_theta_to_quaternion(math.radians(goal_theta))
    return self.goto_goal_state(goal_x, goal_y, goal_z,
      goal_quaternion, self.component_map[component_name].get_seed_state(), save_name=plan_name)

  def execute_trajectory_from_file(self, plan_name):
    file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'saved_trajectories', plan_name + '.yaml')
    with open(file_path, 'r') as file_open:
      loaded_plan = yaml.load(file_open)
      self.group.execute(loaded_plan[1])

  def interpolated_trajectory(self, travel_distance, step=0.004):
    try:
      cur_pose = self.group.get_current_pose().pose
      seed_state = self.group.get_current_joint_values()
      cur_z = cur_pose.position.z
      for i in range(0, int(abs(travel_distance) / step)):
        self.goto_goal_state(cur_pose.position.x, cur_pose.position.y, cur_z,
        [cur_pose.orientation.w, cur_pose.orientation.x, cur_pose.orientation.y, cur_pose.orientation.z],
        seed_state)
        cur_z += np.sign(travel_distance) * step
        rospy.sleep(0.01)
      return True
    except KeyboardInterrupt:
      return

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
    orientation_constraint.absolute_x_axis_tolerance = PATH_CONSTRAINT_TOLERANCE
    orientation_constraint.absolute_y_axis_tolerance = PATH_CONSTRAINT_TOLERANCE
    orientation_constraint.absolute_z_axis_tolerance = PATH_CONSTRAINT_TOLERANCE
    orientation_constraint.weight = 0.01
    self.upright_constraints.orientation_constraints.append(orientation_constraint)
    self.group.set_path_constraints(self.upright_constraints)

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
    print "Robot Groups:", self.robot.get_group_names()
    print "Printing robot state"
    print self.robot.get_current_state()
    print "Robot Joint values"
    print self.group.get_current_joint_values()
    print ""

  def __save_trajectory(self, plan, plan_name='plan'):
    file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'saved_trajectories', plan_name + '.yaml')
    open(file_path, 'a').close()
    with open(file_path, 'w') as file_save:
      yaml.dump(plan, file_save, default_flow_style=True)


  ####DO NOT USE BY ITSELF, NEED TO GOTO JOINT GOAL FIRST. THIS FUNCTION IGNORES COLLISION CHECKS SO USE WITH CAUTION! ####
  def extend_trajectory(self, travel_distance):
    cur_pose = self.group.get_current_pose().pose
    print 'extend_trajectory'
    print cur_pose
    z_state = cur_pose.position.z
    waypoints = []
    wpose = copy.deepcopy(cur_pose)
    wpose.position.z += 0.0001
    waypoints.append(wpose)
    print waypoints
    (plan, fraction) = self.group.compute_cartesian_path(waypoints, 0.03, 0.0)
    if self.__extend_trajectory_helper(plan, copy.deepcopy(wpose), travel_distance) == None:
      print "extend_trajectory failed"
      return None
    print plan
    self.group.execute(plan, wait=True)
    return plan
      
  def __extend_trajectory_helper(self, plan, start_pose, travel_distance, step=0.002, time_step=0.05):
    traj = plan.joint_trajectory.points
    cur_pose_z = start_pose.position.z 
    start_time = plan.joint_trajectory.points[-1].time_from_start
    for i in range(0, int(abs(travel_distance) / step)):
      point = JointTrajectoryPoint()
      print i
      joint_goal = self.__inverse_kinematics([start_pose.position.x, start_pose.position.y, cur_pose_z + (np.sign(travel_distance) * step)], 
        [start_pose.orientation.w, start_pose.orientation.x, start_pose.orientation.y, start_pose.orientation.z], NIC_SEED_STATE)
      if joint_goal == None:
        print "No IK on extend trajectory found"
        return None
      joint_list = []
      for idx, jnt in enumerate(joint_goal.tolist()):
        joint_list.append(jnt)
      point.positions = joint_list
      print joint_list
      point.velocities = [0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]
      point.accelerations = [0,0,0,0,0,0,0]
      time = rospy.Duration.from_sec(start_time.to_sec() + time_step)
      start_time += rospy.Duration.from_sec(time_step)
      point.time_from_start = time
      traj.append(point)
      cur_pose_z += np.sign(travel_distance) * step
    return plan

