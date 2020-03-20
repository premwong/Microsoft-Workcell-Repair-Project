#!/usr/bin/env python

from urdf_parser_py.urdf import URDF
from pykdl_utils.kdl_parser import kdl_tree_from_urdf_model

robot = URDF.from_parameter_server(key='iiwa/robot_description')
print robot
tree = kdl_tree_from_urdf_model(robot)
print tree
base_link = robot.get_root()

#print tree.getNrOfSegments()
chain = tree.getChain(base_link, 'tool_link_ee')
print chain.getNrOfJoints()