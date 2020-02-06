; Auto-generated. Do not edit!


(cl:in-package iiwa_msgs-msg)


;//! \htmlinclude WorkcellCartesian.msg.html

(cl:defclass <WorkcellCartesian> (roslisp-msg-protocol:ros-message)
  ((position_x
    :reader position_x
    :initarg :position_x
    :type cl:float
    :initform 0.0)
   (position_y
    :reader position_y
    :initarg :position_y
    :type cl:float
    :initform 0.0)
   (position_z
    :reader position_z
    :initarg :position_z
    :type cl:float
    :initform 0.0)
   (orientation_w
    :reader orientation_w
    :initarg :orientation_w
    :type cl:float
    :initform 0.0)
   (orientation_x
    :reader orientation_x
    :initarg :orientation_x
    :type cl:float
    :initform 0.0)
   (orientation_y
    :reader orientation_y
    :initarg :orientation_y
    :type cl:float
    :initform 0.0)
   (orientation_z
    :reader orientation_z
    :initarg :orientation_z
    :type cl:float
    :initform 0.0))
)

(cl:defclass WorkcellCartesian (<WorkcellCartesian>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <WorkcellCartesian>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'WorkcellCartesian)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name iiwa_msgs-msg:<WorkcellCartesian> is deprecated: use iiwa_msgs-msg:WorkcellCartesian instead.")))

(cl:ensure-generic-function 'position_x-val :lambda-list '(m))
(cl:defmethod position_x-val ((m <WorkcellCartesian>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-msg:position_x-val is deprecated.  Use iiwa_msgs-msg:position_x instead.")
  (position_x m))

(cl:ensure-generic-function 'position_y-val :lambda-list '(m))
(cl:defmethod position_y-val ((m <WorkcellCartesian>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-msg:position_y-val is deprecated.  Use iiwa_msgs-msg:position_y instead.")
  (position_y m))

(cl:ensure-generic-function 'position_z-val :lambda-list '(m))
(cl:defmethod position_z-val ((m <WorkcellCartesian>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-msg:position_z-val is deprecated.  Use iiwa_msgs-msg:position_z instead.")
  (position_z m))

(cl:ensure-generic-function 'orientation_w-val :lambda-list '(m))
(cl:defmethod orientation_w-val ((m <WorkcellCartesian>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-msg:orientation_w-val is deprecated.  Use iiwa_msgs-msg:orientation_w instead.")
  (orientation_w m))

(cl:ensure-generic-function 'orientation_x-val :lambda-list '(m))
(cl:defmethod orientation_x-val ((m <WorkcellCartesian>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-msg:orientation_x-val is deprecated.  Use iiwa_msgs-msg:orientation_x instead.")
  (orientation_x m))

(cl:ensure-generic-function 'orientation_y-val :lambda-list '(m))
(cl:defmethod orientation_y-val ((m <WorkcellCartesian>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-msg:orientation_y-val is deprecated.  Use iiwa_msgs-msg:orientation_y instead.")
  (orientation_y m))

(cl:ensure-generic-function 'orientation_z-val :lambda-list '(m))
(cl:defmethod orientation_z-val ((m <WorkcellCartesian>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-msg:orientation_z-val is deprecated.  Use iiwa_msgs-msg:orientation_z instead.")
  (orientation_z m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <WorkcellCartesian>) ostream)
  "Serializes a message object of type '<WorkcellCartesian>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'position_x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'position_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'position_z))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'orientation_w))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'orientation_x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'orientation_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'orientation_z))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <WorkcellCartesian>) istream)
  "Deserializes a message object of type '<WorkcellCartesian>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'position_x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'position_y) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'position_z) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'orientation_w) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'orientation_x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'orientation_y) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'orientation_z) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<WorkcellCartesian>)))
  "Returns string type for a message object of type '<WorkcellCartesian>"
  "iiwa_msgs/WorkcellCartesian")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'WorkcellCartesian)))
  "Returns string type for a message object of type 'WorkcellCartesian"
  "iiwa_msgs/WorkcellCartesian")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<WorkcellCartesian>)))
  "Returns md5sum for a message object of type '<WorkcellCartesian>"
  "c04cda0aa82523820ae4ce5601f32ae5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'WorkcellCartesian)))
  "Returns md5sum for a message object of type 'WorkcellCartesian"
  "c04cda0aa82523820ae4ce5601f32ae5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<WorkcellCartesian>)))
  "Returns full string definition for message of type '<WorkcellCartesian>"
  (cl:format cl:nil "float32 position_x~%float32 position_y~%float32 position_z~%float32 orientation_w~%float32 orientation_x~%float32 orientation_y~%float32 orientation_z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'WorkcellCartesian)))
  "Returns full string definition for message of type 'WorkcellCartesian"
  (cl:format cl:nil "float32 position_x~%float32 position_y~%float32 position_z~%float32 orientation_w~%float32 orientation_x~%float32 orientation_y~%float32 orientation_z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <WorkcellCartesian>))
  (cl:+ 0
     4
     4
     4
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <WorkcellCartesian>))
  "Converts a ROS message object to a list"
  (cl:list 'WorkcellCartesian
    (cl:cons ':position_x (position_x msg))
    (cl:cons ':position_y (position_y msg))
    (cl:cons ':position_z (position_z msg))
    (cl:cons ':orientation_w (orientation_w msg))
    (cl:cons ':orientation_x (orientation_x msg))
    (cl:cons ':orientation_y (orientation_y msg))
    (cl:cons ':orientation_z (orientation_z msg))
))
