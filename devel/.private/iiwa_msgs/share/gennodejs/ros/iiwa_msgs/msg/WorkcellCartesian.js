// Auto-generated. Do not edit!

// (in-package iiwa_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class WorkcellCartesian {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.position_x = null;
      this.position_y = null;
      this.position_z = null;
      this.orientation_w = null;
      this.orientation_x = null;
      this.orientation_y = null;
      this.orientation_z = null;
    }
    else {
      if (initObj.hasOwnProperty('position_x')) {
        this.position_x = initObj.position_x
      }
      else {
        this.position_x = 0.0;
      }
      if (initObj.hasOwnProperty('position_y')) {
        this.position_y = initObj.position_y
      }
      else {
        this.position_y = 0.0;
      }
      if (initObj.hasOwnProperty('position_z')) {
        this.position_z = initObj.position_z
      }
      else {
        this.position_z = 0.0;
      }
      if (initObj.hasOwnProperty('orientation_w')) {
        this.orientation_w = initObj.orientation_w
      }
      else {
        this.orientation_w = 0.0;
      }
      if (initObj.hasOwnProperty('orientation_x')) {
        this.orientation_x = initObj.orientation_x
      }
      else {
        this.orientation_x = 0.0;
      }
      if (initObj.hasOwnProperty('orientation_y')) {
        this.orientation_y = initObj.orientation_y
      }
      else {
        this.orientation_y = 0.0;
      }
      if (initObj.hasOwnProperty('orientation_z')) {
        this.orientation_z = initObj.orientation_z
      }
      else {
        this.orientation_z = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type WorkcellCartesian
    // Serialize message field [position_x]
    bufferOffset = _serializer.float32(obj.position_x, buffer, bufferOffset);
    // Serialize message field [position_y]
    bufferOffset = _serializer.float32(obj.position_y, buffer, bufferOffset);
    // Serialize message field [position_z]
    bufferOffset = _serializer.float32(obj.position_z, buffer, bufferOffset);
    // Serialize message field [orientation_w]
    bufferOffset = _serializer.float32(obj.orientation_w, buffer, bufferOffset);
    // Serialize message field [orientation_x]
    bufferOffset = _serializer.float32(obj.orientation_x, buffer, bufferOffset);
    // Serialize message field [orientation_y]
    bufferOffset = _serializer.float32(obj.orientation_y, buffer, bufferOffset);
    // Serialize message field [orientation_z]
    bufferOffset = _serializer.float32(obj.orientation_z, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type WorkcellCartesian
    let len;
    let data = new WorkcellCartesian(null);
    // Deserialize message field [position_x]
    data.position_x = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [position_y]
    data.position_y = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [position_z]
    data.position_z = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [orientation_w]
    data.orientation_w = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [orientation_x]
    data.orientation_x = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [orientation_y]
    data.orientation_y = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [orientation_z]
    data.orientation_z = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 28;
  }

  static datatype() {
    // Returns string type for a message object
    return 'iiwa_msgs/WorkcellCartesian';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'c04cda0aa82523820ae4ce5601f32ae5';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 position_x
    float32 position_y
    float32 position_z
    float32 orientation_w
    float32 orientation_x
    float32 orientation_y
    float32 orientation_z
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new WorkcellCartesian(null);
    if (msg.position_x !== undefined) {
      resolved.position_x = msg.position_x;
    }
    else {
      resolved.position_x = 0.0
    }

    if (msg.position_y !== undefined) {
      resolved.position_y = msg.position_y;
    }
    else {
      resolved.position_y = 0.0
    }

    if (msg.position_z !== undefined) {
      resolved.position_z = msg.position_z;
    }
    else {
      resolved.position_z = 0.0
    }

    if (msg.orientation_w !== undefined) {
      resolved.orientation_w = msg.orientation_w;
    }
    else {
      resolved.orientation_w = 0.0
    }

    if (msg.orientation_x !== undefined) {
      resolved.orientation_x = msg.orientation_x;
    }
    else {
      resolved.orientation_x = 0.0
    }

    if (msg.orientation_y !== undefined) {
      resolved.orientation_y = msg.orientation_y;
    }
    else {
      resolved.orientation_y = 0.0
    }

    if (msg.orientation_z !== undefined) {
      resolved.orientation_z = msg.orientation_z;
    }
    else {
      resolved.orientation_z = 0.0
    }

    return resolved;
    }
};

module.exports = WorkcellCartesian;
