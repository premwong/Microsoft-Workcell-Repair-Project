;; Auto-generated. Do not edit!


(when (boundp 'iiwa_msgs::CollectPose)
  (if (not (find-package "IIWA_MSGS"))
    (make-package "IIWA_MSGS"))
  (shadow 'CollectPose (find-package "IIWA_MSGS")))
(unless (find-package "IIWA_MSGS::COLLECTPOSE")
  (make-package "IIWA_MSGS::COLLECTPOSE"))
(unless (find-package "IIWA_MSGS::COLLECTPOSEREQUEST")
  (make-package "IIWA_MSGS::COLLECTPOSEREQUEST"))
(unless (find-package "IIWA_MSGS::COLLECTPOSERESPONSE")
  (make-package "IIWA_MSGS::COLLECTPOSERESPONSE"))

(in-package "ROS")





(defclass iiwa_msgs::CollectPoseRequest
  :super ros::object
  :slots (_flag ))

(defmethod iiwa_msgs::CollectPoseRequest
  (:init
   (&key
    ((:flag __flag) 0)
    )
   (send-super :init)
   (setq _flag (round __flag))
   self)
  (:flag
   (&optional __flag)
   (if __flag (setq _flag __flag)) _flag)
  (:serialization-length
   ()
   (+
    ;; int16 _flag
    2
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int16 _flag
       (write-word _flag s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int16 _flag
     (setq _flag (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(defclass iiwa_msgs::CollectPoseResponse
  :super ros::object
  :slots (_position_x _position_y _position_z _orientation_w _orientation_x _orientation_y _orientation_z ))

(defmethod iiwa_msgs::CollectPoseResponse
  (:init
   (&key
    ((:position_x __position_x) 0.0)
    ((:position_y __position_y) 0.0)
    ((:position_z __position_z) 0.0)
    ((:orientation_w __orientation_w) 0.0)
    ((:orientation_x __orientation_x) 0.0)
    ((:orientation_y __orientation_y) 0.0)
    ((:orientation_z __orientation_z) 0.0)
    )
   (send-super :init)
   (setq _position_x (float __position_x))
   (setq _position_y (float __position_y))
   (setq _position_z (float __position_z))
   (setq _orientation_w (float __orientation_w))
   (setq _orientation_x (float __orientation_x))
   (setq _orientation_y (float __orientation_y))
   (setq _orientation_z (float __orientation_z))
   self)
  (:position_x
   (&optional __position_x)
   (if __position_x (setq _position_x __position_x)) _position_x)
  (:position_y
   (&optional __position_y)
   (if __position_y (setq _position_y __position_y)) _position_y)
  (:position_z
   (&optional __position_z)
   (if __position_z (setq _position_z __position_z)) _position_z)
  (:orientation_w
   (&optional __orientation_w)
   (if __orientation_w (setq _orientation_w __orientation_w)) _orientation_w)
  (:orientation_x
   (&optional __orientation_x)
   (if __orientation_x (setq _orientation_x __orientation_x)) _orientation_x)
  (:orientation_y
   (&optional __orientation_y)
   (if __orientation_y (setq _orientation_y __orientation_y)) _orientation_y)
  (:orientation_z
   (&optional __orientation_z)
   (if __orientation_z (setq _orientation_z __orientation_z)) _orientation_z)
  (:serialization-length
   ()
   (+
    ;; float32 _position_x
    4
    ;; float32 _position_y
    4
    ;; float32 _position_z
    4
    ;; float32 _orientation_w
    4
    ;; float32 _orientation_x
    4
    ;; float32 _orientation_y
    4
    ;; float32 _orientation_z
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _position_x
       (sys::poke _position_x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _position_y
       (sys::poke _position_y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _position_z
       (sys::poke _position_z (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _orientation_w
       (sys::poke _orientation_w (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _orientation_x
       (sys::poke _orientation_x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _orientation_y
       (sys::poke _orientation_y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _orientation_z
       (sys::poke _orientation_z (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _position_x
     (setq _position_x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _position_y
     (setq _position_y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _position_z
     (setq _position_z (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _orientation_w
     (setq _orientation_w (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _orientation_x
     (setq _orientation_x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _orientation_y
     (setq _orientation_y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _orientation_z
     (setq _orientation_z (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(defclass iiwa_msgs::CollectPose
  :super ros::object
  :slots ())

(setf (get iiwa_msgs::CollectPose :md5sum-) "a9485893dad130c910b7cc6b86bb0941")
(setf (get iiwa_msgs::CollectPose :datatype-) "iiwa_msgs/CollectPose")
(setf (get iiwa_msgs::CollectPose :request) iiwa_msgs::CollectPoseRequest)
(setf (get iiwa_msgs::CollectPose :response) iiwa_msgs::CollectPoseResponse)

(defmethod iiwa_msgs::CollectPoseRequest
  (:response () (instance iiwa_msgs::CollectPoseResponse :init)))

(setf (get iiwa_msgs::CollectPoseRequest :md5sum-) "a9485893dad130c910b7cc6b86bb0941")
(setf (get iiwa_msgs::CollectPoseRequest :datatype-) "iiwa_msgs/CollectPoseRequest")
(setf (get iiwa_msgs::CollectPoseRequest :definition-)
      "int16 flag
---
float32 position_x
float32 position_y
float32 position_z
float32 orientation_w
float32 orientation_x
float32 orientation_y
float32 orientation_z

")

(setf (get iiwa_msgs::CollectPoseResponse :md5sum-) "a9485893dad130c910b7cc6b86bb0941")
(setf (get iiwa_msgs::CollectPoseResponse :datatype-) "iiwa_msgs/CollectPoseResponse")
(setf (get iiwa_msgs::CollectPoseResponse :definition-)
      "int16 flag
---
float32 position_x
float32 position_y
float32 position_z
float32 orientation_w
float32 orientation_x
float32 orientation_y
float32 orientation_z

")



(provide :iiwa_msgs/CollectPose "a9485893dad130c910b7cc6b86bb0941")


