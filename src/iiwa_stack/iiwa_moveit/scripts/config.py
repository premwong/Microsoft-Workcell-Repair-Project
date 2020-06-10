#!/usr/bin/env python

import numpy as np 
import math

GLOBAL_OFFSET = (-0.015, -0.04)
Z_OFFSET = 0.13
THETA_OFFSET = 0
HEATSINK_Z_OFFSET = 0.3

NIC_OFFSET = (0.065, -0.05, 0.113) #x, y, z
# NIC_OFFSET = (0, 0, 0.14)
HEATSINK_OFFSET = (-0.237,0.06, 0.2)
HEATSINK_PLACE_OFFSET = (-0.249, 0.08, 0.2)
HDD_OFFSET = (-0.488,0.11, 0.2)
RAM_OFFSET = (-0.116, -0.065, 0.2)

TIME_SCALE = 0.5

PATH_CONSTRAINT_TOLERANCE = 0.001
NUM_JOINTS = 7
MIN_JOINT_LIMITS_DEG = [-169, -119, -169, -119, -169, -115, -174]
MAX_JOINT_LIMITS_DEG = [169, 119, 169, 119, 169, 115, 174]
NIC_SEED_STATE = [-1.097929835319519, -0.6288679838180542, 2.453058958053589, -1.1540085077285767, 0.38478365540504456, 1.4823733568191528, -0.15152356028556824] #APRIL 27
# NIC_SEED_STATE = [1.987323522567749, 1.4358184337615967, -1.9114866256713867, -1.036642074584961, 1.578827142715454, 1.9280040264129639, -1.9716582298278809] #good one for now
# NIC_SEED_STATE = [1.557648777961731, 1.1192528009414673, -2.0074729919433594, -1.7809964418411255, 1.5245822668075562, 1.8033620119094849, -0.6167297959327698]


NIC_BIN_SEED_STATE = [-1.4139928817749023, 0.33902448415756226, 0.11167170107364655, -1.264603853225708, -0.04450586438179016, 1.520429015159607, 3.0194315910339355] #NIC Seed state for tray 

# NIC_SEED_STATE = [-2.457632064819336, -0.9867644906044006, -1.4544497728347778, -1.4214571714401245, -0.9698165059089661, 1.7759943008422852, 1.3991572856903076]
HDD_SEED_STATE = [0.4520516097545624, 0.9477099180221558, -2.3023149967193604, 2.0533716678619385, 2.569415330886841, -0.9975131750106812, 1.196797490119934]
#TODO: find / decide seed state to use
# HEATSINK_SEED_STATE = [-2.3611752224604667, -1.404261191226993, -0.7302048468113553, -1.762417586918243, -1.5633125905151535, 1.9439532527527876, -0.9330501636422028]


HEATSINK_SEED_STATE = [2.094787120819092, 1.5185761451721191, 0.8504869937896729, 1.2178930044174194, -1.0015379190444946, 1.9052773714065552, -2.20597243309021]

HEATSINK_BIN_SEED_STATE = [1.4840437173843384, -0.492412805557251, -0.3248025178909302, 1.490195631980896, -2.4500184059143066, 1.4281922578811646, 2.5577869415283203]

HEATSINK_TRAY_SEED =[-1.9187335968017578, -1.222485899925232, 1.6233899593353271, -1.7386283874511719, 1.5734597444534302, 0.9163234233856201, -2.1677651405334473]

MANUAL_STEP = 0.002
PLANNER_ID = 'RRTConnectkConfigDefault'
RAM_ROTATION = lambda sin_angle, cos_angle: [[1, 0, 0],
                                            [0, 0, -1],
                                            [0, 1, 0]]

NIC_ROTATION = lambda sin_angle, cos_angle: [[sin_angle, -1*cos_angle, 0], 
                                            [-1*cos_angle, -1*sin_angle, 0], 
                                            [0, 0, -1]]


HEATSINK_ROTATION = lambda sin_angle, cos_angle: [[sin_angle, -1*(math.sqrt(3)/2)*cos_angle, 0.5*cos_angle],
                                                 [-1*cos_angle, -1*(math.sqrt(3)/2)*sin_angle, 0.5*sin_angle],
                                                 [0, -0.5, -1*math.sqrt(3)/2]]

HDD_ROTATION = lambda sin_angle, cos_angle: [[sin_angle, -1*(math.sqrt(3)/2)*cos_angle, -0.5*cos_angle],
                                                 [-1*cos_angle, -1*(math.sqrt(3)/2)*sin_angle, -0.5*sin_angle],
                                                 [0, 0.5, -1*math.sqrt(3)/2]]

HEATSINK_TRANSFORM = np.array([[1, 0, 0], [0, (math.sqrt(3)/2), -0.5], [0, 0.5, math.sqrt(3)/2]])
HDD_TRANFORM = np.array([[1, 0, 0], [0, (math.sqrt(3)/2), 0.5], [0, -0.5, (math.sqrt(3)/2)]])

HOME_STATE = np.array([1.2799978256225586, 1.096759557723999, -2.089806079864502, -1.8478130102157593, 0.9433833956718445, 1.875718355178833, -1.608567237854004])

RAM_SEED_STATE = [1.669561505317688, -0.6548308730125427, 0.6364870667457581, 1.7189745903015137, 0.6630995273590088, 1.0921908617019653, -2.2323319911956787]


VELOCITY_SCALE = 0.4



