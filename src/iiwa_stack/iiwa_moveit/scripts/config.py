#!/usr/bin/env python

import numpy as np 
import math

GLOBAL_OFFSET = (-0.021, 0.05)
Z_OFFSET = 0.20
THETA_OFFSET = 0
HEATSINK_Z_OFFSET = 0.3

NIC_OFFSET = (0.076, -0.08, 0.14) #x, y, z
HEATSINK_OFFSET = (-0.106, -0.04, 0.2)
PATH_CONSTRAINT_TOLERANCE = 0.001
NUM_JOINTS = 7
MIN_JOINT_LIMITS_DEG = [-169, -119, -169, -119, -169, -119, -174]
MAX_JOINT_LIMITS_DEG = [169, 119, 169, 119, 169, 119, 174]
# NIC_SEED_STATE = [-1.097929835319519, -0.6288679838180542, 2.453058958053589, -1.1540085077285767, 0.38478365540504456, 1.4823733568191528, -0.15152356028556824] #APRIL 27
NIC_SEED_STATE = [1.987323522567749, 1.4358184337615967, -1.9114866256713867, -1.036642074584961, 1.578827142715454, 1.9280040264129639, -1.9716582298278809]
HDD_SEED_STATE = [0.4520516097545624, 0.9477099180221558, -2.3023149967193604, 2.0533716678619385, 2.569415330886841, -0.9975131750106812, 1.196797490119934]
#TODO: find / decide seed state to use
HEATSINK_SEED_STATE = [-2.3611752224604667, -1.404261191226993, -0.7302048468113553, -1.762417586918243, -1.5633125905151535, 1.9439532527527876, -0.9330501636422028]

MANUAL_STEP = 0.002
PLANNER_ID = 'RRTConnectkConfigDefault'
NIC_ROTATION = lambda sin_angle, cos_angle: [[sin_angle, -1*cos_angle, 0], 
                                            [-1*cos_angle, -1*sin_angle, 0], 
                                            [0, 0, -1]]
# HEATSINK_ROTATION = lambda sin_angle, cos_angle: [[sin_angle, -1*cos_angle, 0],
#                                                  [-1*(math.sqrt(3)/2)*cos_angle, -1*(math.sqrt(3)/2)*sin_angle, 0.5],
#                                                  [-0.5*cos_angle, -0.5*sin_angle, -1*math.sqrt(3)/2]]
HEATSINK_ROTATION = lambda sin_angle, cos_angle: [[sin_angle, -1*(math.sqrt(3)/2)*cos_angle, 0.5*cos_angle],
                                                 [-1*cos_angle, -1*(math.sqrt(3)/2)*sin_angle, 0.5*sin_angle],
                                                 [0, -0.5, -1*math.sqrt(3)/2]]

HDD_ROTATION = lambda sin_angle, cos_angle: [[sin_angle, -1*(math.sqrt(3)/2)*cos_angle, -0.5*cos_angle],
                                                 [-1*cos_angle, -1*(math.sqrt(3)/2)*sin_angle, -0.5*sin_angle],
                                                 [0, 0.5, -1*math.sqrt(3)/2]]

HEATSINK_TRANSFORM = np.array([[1, 0, 0], [0, (math.sqrt(3)/2), -0.5], [0, 0.5, math.sqrt(3)/2]])
HDD_TRANFORM = np.array([[1, 0, 0], [0, (math.sqrt(3)/2), 0.5], [0, -0.5, (math.sqrt(3)/2)]])

HOME_STATE = np.array([1.2799978256225586, 1.096759557723999, -2.089806079864502, -1.8478130102157593, 0.9433833956718445, 1.875718355178833, -1.608567237854004])
