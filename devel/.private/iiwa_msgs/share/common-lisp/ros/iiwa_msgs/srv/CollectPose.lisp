; Auto-generated. Do not edit!


(cl:in-package iiwa_msgs-srv)


;//! \htmlinclude CollectPose-request.msg.html

(cl:defclass <CollectPose-request> (roslisp-msg-protocol:ros-message)
  ((flag
    :reader flag
    :initarg :flag
    :type cl:fixnum
    :initform 0))
)

(cl:defclass CollectPose-request (<CollectPose-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <CollectPose-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'CollectPose-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name iiwa_msgs-srv:<CollectPose-request> is deprecated: use iiwa_msgs-srv:CollectPose-request instead.")))

(cl:ensure-generic-function 'flag-val :lambda-list '(m))
(cl:defmethod flag-val ((m <CollectPose-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-srv:flag-val is deprecated.  Use iiwa_msgs-srv:flag instead.")
  (flag m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <CollectPose-request>) ostream)
  "Serializes a message object of type '<CollectPose-request>"
  (cl:let* ((signed (cl:slot-value msg 'flag)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 65536) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <CollectPose-request>) istream)
  "Deserializes a message object of type '<CollectPose-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'flag) (cl:if (cl:< unsigned 32768) unsigned (cl:- unsigned 65536))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<CollectPose-request>)))
  "Returns string type for a service object of type '<CollectPose-request>"
  "iiwa_msgs/CollectPoseRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CollectPose-request)))
  "Returns string type for a service object of type 'CollectPose-request"
  "iiwa_msgs/CollectPoseRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<CollectPose-request>)))
  "Returns md5sum for a message object of type '<CollectPose-request>"
  "a9485893dad130c910b7cc6b86bb0941")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'CollectPose-request)))
  "Returns md5sum for a message object of type 'CollectPose-request"
  "a9485893dad130c910b7cc6b86bb0941")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<CollectPose-request>)))
  "Returns full string definition for message of type '<CollectPose-request>"
  (cl:format cl:nil "int16 flag~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'CollectPose-request)))
  "Returns full string definition for message of type 'CollectPose-request"
  (cl:format cl:nil "int16 flag~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <CollectPose-request>))
  (cl:+ 0
     2
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <CollectPose-request>))
  "Converts a ROS message object to a list"
  (cl:list 'CollectPose-request
    (cl:cons ':flag (flag msg))
))
;//! \htmlinclude CollectPose-response.msg.html

(cl:defclass <CollectPose-response> (roslisp-msg-protocol:ros-message)
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

(cl:defclass CollectPose-response (<CollectPose-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <CollectPose-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'CollectPose-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name iiwa_msgs-srv:<CollectPose-response> is deprecated: use iiwa_msgs-srv:CollectPose-response instead.")))

(cl:ensure-generic-function 'position_x-val :lambda-list '(m))
(cl:defmethod position_x-val ((m <CollectPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-srv:position_x-val is deprecated.  Use iiwa_msgs-srv:position_x instead.")
  (position_x m))

(cl:ensure-generic-function 'position_y-val :lambda-list '(m))
(cl:defmethod position_y-val ((m <CollectPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-srv:position_y-val is deprecated.  Use iiwa_msgs-srv:position_y instead.")
  (position_y m))

(cl:ensure-generic-function 'position_z-val :lambda-list '(m))
(cl:defmethod position_z-val ((m <CollectPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-srv:position_z-val is deprecated.  Use iiwa_msgs-srv:position_z instead.")
  (position_z m))

(cl:ensure-generic-function 'orientation_w-val :lambda-list '(m))
(cl:defmethod orientation_w-val ((m <CollectPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-srv:orientation_w-val is deprecated.  Use iiwa_msgs-srv:orientation_w instead.")
  (orientation_w m))

(cl:ensure-generic-function 'orientation_x-val :lambda-list '(m))
(cl:defmethod orientation_x-val ((m <CollectPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-srv:orientation_x-val is deprecated.  Use iiwa_msgs-srv:orientation_x instead.")
  (orientation_x m))

(cl:ensure-generic-function 'orientation_y-val :lambda-list '(m))
(cl:defmethod orientation_y-val ((m <CollectPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-srv:orientation_y-val is deprecated.  Use iiwa_msgs-srv:orientation_y instead.")
  (orientation_y m))

(cl:ensure-generic-function 'orientation_z-val :lambda-list '(m))
(cl:defmethod orientation_z-val ((m <CollectPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader iiwa_msgs-srv:orientation_z-val is deprecated.  Use iiwa_msgs-srv:orientation_z instead.")
  (orientation_z m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <CollectPose-response>) ostream)
  "Serializes a message object of type '<CollectPose-response>"
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
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <CollectPose-response>) istream)
  "Deserializes a message object of type '<CollectPose-response>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<CollectPose-response>)))
  "Returns string type for a service object of type '<CollectPose-response>"
  "iiwa_msgs/CollectPoseResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CollectPose-response)))
  "Returns string type for a service object of type 'CollectPose-response"
  "iiwa_msgs/CollectPoseResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<CollectPose-response>)))
  "Returns md5sum for a message object of type '<CollectPose-response>"
  "a9485893dad130c910b7cc6b86bb0941")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'CollectPose-response)))
  "Returns md5sum for a message object of type 'CollectPose-response"
  "a9485893dad130c910b7cc6b86bb0941")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<CollectPose-response>)))
  "Returns full string definition for message of type '<CollectPose-response>"
  (cl:format cl:nil "float32 position_x~%float32 position_y~%float32 position_z~%float32 orientation_w~%float32 orientation_x~%float32 orientation_y~%float32 orientation_z~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'CollectPose-response)))
  "Returns full string definition for message of type 'CollectPose-response"
  (cl:format cl:nil "float32 position_x~%float32 position_y~%float32 position_z~%float32 orientation_w~%float32 orientation_x~%float32 orientation_y~%float32 orientation_z~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <CollectPose-response>))
  (cl:+ 0
     4
     4
     4
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <CollectPose-response>))
  "Converts a ROS message object to a list"
  (cl:list 'CollectPose-response
    (cl:cons ':position_x (position_x msg))
    (cl:cons ':position_y (position_y msg))
    (cl:cons ':position_z (position_z msg))
    (cl:cons ':orientation_w (orientation_w msg))
    (cl:cons ':orientation_x (orientation_x msg))
    (cl:cons ':orientation_y (orientation_y msg))
    (cl:cons ':orientation_z (orientation_z msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'CollectPose)))
  'CollectPose-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'CollectPose)))
  'CollectPose-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CollectPose)))
  "Returns string type for a service object of type '<CollectPose>"
  "iiwa_msgs/CollectPose")