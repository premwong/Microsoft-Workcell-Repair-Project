
"use strict";

let SetSmartServoLinSpeedLimits = require('./SetSmartServoLinSpeedLimits.js')
let SetEndpointFrame = require('./SetEndpointFrame.js')
let TimeToDestination = require('./TimeToDestination.js')
let SetWorkpiece = require('./SetWorkpiece.js')
let SetPTPJointSpeedLimits = require('./SetPTPJointSpeedLimits.js')
let AddTwoInts = require('./AddTwoInts.js')
let ConfigureControlMode = require('./ConfigureControlMode.js')
let SetSmartServoJointSpeedLimits = require('./SetSmartServoJointSpeedLimits.js')
let SetPTPCartesianSpeedLimits = require('./SetPTPCartesianSpeedLimits.js')
let SetSpeedOverride = require('./SetSpeedOverride.js')
let CollectPose = require('./CollectPose.js')

module.exports = {
  SetSmartServoLinSpeedLimits: SetSmartServoLinSpeedLimits,
  SetEndpointFrame: SetEndpointFrame,
  TimeToDestination: TimeToDestination,
  SetWorkpiece: SetWorkpiece,
  SetPTPJointSpeedLimits: SetPTPJointSpeedLimits,
  AddTwoInts: AddTwoInts,
  ConfigureControlMode: ConfigureControlMode,
  SetSmartServoJointSpeedLimits: SetSmartServoJointSpeedLimits,
  SetPTPCartesianSpeedLimits: SetPTPCartesianSpeedLimits,
  SetSpeedOverride: SetSpeedOverride,
  CollectPose: CollectPose,
};
