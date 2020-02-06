// Generated by gencpp from file iiwa_msgs/MoveToJointPositionGoal.msg
// DO NOT EDIT!


#ifndef IIWA_MSGS_MESSAGE_MOVETOJOINTPOSITIONGOAL_H
#define IIWA_MSGS_MESSAGE_MOVETOJOINTPOSITIONGOAL_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <iiwa_msgs/JointPosition.h>

namespace iiwa_msgs
{
template <class ContainerAllocator>
struct MoveToJointPositionGoal_
{
  typedef MoveToJointPositionGoal_<ContainerAllocator> Type;

  MoveToJointPositionGoal_()
    : joint_position()  {
    }
  MoveToJointPositionGoal_(const ContainerAllocator& _alloc)
    : joint_position(_alloc)  {
  (void)_alloc;
    }



   typedef  ::iiwa_msgs::JointPosition_<ContainerAllocator>  _joint_position_type;
  _joint_position_type joint_position;





  typedef boost::shared_ptr< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> const> ConstPtr;

}; // struct MoveToJointPositionGoal_

typedef ::iiwa_msgs::MoveToJointPositionGoal_<std::allocator<void> > MoveToJointPositionGoal;

typedef boost::shared_ptr< ::iiwa_msgs::MoveToJointPositionGoal > MoveToJointPositionGoalPtr;
typedef boost::shared_ptr< ::iiwa_msgs::MoveToJointPositionGoal const> MoveToJointPositionGoalConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace iiwa_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'geometry_msgs': ['/opt/ros/kinetic/share/geometry_msgs/cmake/../msg'], 'actionlib_msgs': ['/opt/ros/kinetic/share/actionlib_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'iiwa_msgs': ['/home/workcell/Desktop/iiwa_stack_ws/src/iiwa_stack/iiwa_msgs/msg', '/home/workcell/Desktop/iiwa_stack_ws/devel/.private/iiwa_msgs/share/iiwa_msgs/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "291db5d11cb9e1304763b006078fa381";
  }

  static const char* value(const ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x291db5d11cb9e130ULL;
  static const uint64_t static_value2 = 0x4763b006078fa381ULL;
};

template<class ContainerAllocator>
struct DataType< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "iiwa_msgs/MoveToJointPositionGoal";
  }

  static const char* value(const ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n\
# Goal\n\
iiwa_msgs/JointPosition joint_position\n\
\n\
\n\
================================================================================\n\
MSG: iiwa_msgs/JointPosition\n\
Header header\n\
JointQuantity position\n\
================================================================================\n\
MSG: std_msgs/Header\n\
# Standard metadata for higher-level stamped data types.\n\
# This is generally used to communicate timestamped data \n\
# in a particular coordinate frame.\n\
# \n\
# sequence ID: consecutively increasing ID \n\
uint32 seq\n\
#Two-integer timestamp that is expressed as:\n\
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n\
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n\
# time-handling sugar is provided by the client library\n\
time stamp\n\
#Frame this data is associated with\n\
# 0: no frame\n\
# 1: global frame\n\
string frame_id\n\
\n\
================================================================================\n\
MSG: iiwa_msgs/JointQuantity\n\
float32 a1\n\
float32 a2\n\
float32 a3\n\
float32 a4\n\
float32 a5\n\
float32 a6\n\
float32 a7\n\
";
  }

  static const char* value(const ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.joint_position);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct MoveToJointPositionGoal_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::iiwa_msgs::MoveToJointPositionGoal_<ContainerAllocator>& v)
  {
    s << indent << "joint_position: ";
    s << std::endl;
    Printer< ::iiwa_msgs::JointPosition_<ContainerAllocator> >::stream(s, indent + "  ", v.joint_position);
  }
};

} // namespace message_operations
} // namespace ros

#endif // IIWA_MSGS_MESSAGE_MOVETOJOINTPOSITIONGOAL_H