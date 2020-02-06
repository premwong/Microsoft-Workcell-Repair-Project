;; Auto-generated. Do not edit!


(when (boundp 'iiwa_msgs::AddTwoInts)
  (if (not (find-package "IIWA_MSGS"))
    (make-package "IIWA_MSGS"))
  (shadow 'AddTwoInts (find-package "IIWA_MSGS")))
(unless (find-package "IIWA_MSGS::ADDTWOINTS")
  (make-package "IIWA_MSGS::ADDTWOINTS"))
(unless (find-package "IIWA_MSGS::ADDTWOINTSREQUEST")
  (make-package "IIWA_MSGS::ADDTWOINTSREQUEST"))
(unless (find-package "IIWA_MSGS::ADDTWOINTSRESPONSE")
  (make-package "IIWA_MSGS::ADDTWOINTSRESPONSE"))

(in-package "ROS")





(defclass iiwa_msgs::AddTwoIntsRequest
  :super ros::object
  :slots (_A _B ))

(defmethod iiwa_msgs::AddTwoIntsRequest
  (:init
   (&key
    ((:A __A) 0)
    ((:B __B) 0)
    )
   (send-super :init)
   (setq _A (round __A))
   (setq _B (round __B))
   self)
  (:A
   (&optional __A)
   (if __A (setq _A __A)) _A)
  (:B
   (&optional __B)
   (if __B (setq _B __B)) _B)
  (:serialization-length
   ()
   (+
    ;; int64 _A
    8
    ;; int64 _B
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int64 _A
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _A (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _A) (= (length (_A . bv)) 2)) ;; bignum
              (write-long (ash (elt (_A . bv) 0) 0) s)
              (write-long (ash (elt (_A . bv) 1) -1) s))
             ((and (class _A) (= (length (_A . bv)) 1)) ;; big1
              (write-long (elt (_A . bv) 0) s)
              (write-long (if (>= _A 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _A s)(write-long (if (>= _A 0) 0 #xffffffff) s)))
     ;; int64 _B
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _B (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _B) (= (length (_B . bv)) 2)) ;; bignum
              (write-long (ash (elt (_B . bv) 0) 0) s)
              (write-long (ash (elt (_B . bv) 1) -1) s))
             ((and (class _B) (= (length (_B . bv)) 1)) ;; big1
              (write-long (elt (_B . bv) 0) s)
              (write-long (if (>= _B 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _B s)(write-long (if (>= _B 0) 0 #xffffffff) s)))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int64 _A
#+(or :alpha :irix6 :x86_64)
      (setf _A (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _A (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; int64 _B
#+(or :alpha :irix6 :x86_64)
      (setf _B (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _B (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;;
   self)
  )

(defclass iiwa_msgs::AddTwoIntsResponse
  :super ros::object
  :slots (_Sum ))

(defmethod iiwa_msgs::AddTwoIntsResponse
  (:init
   (&key
    ((:Sum __Sum) 0)
    )
   (send-super :init)
   (setq _Sum (round __Sum))
   self)
  (:Sum
   (&optional __Sum)
   (if __Sum (setq _Sum __Sum)) _Sum)
  (:serialization-length
   ()
   (+
    ;; int64 _Sum
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int64 _Sum
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _Sum (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _Sum) (= (length (_Sum . bv)) 2)) ;; bignum
              (write-long (ash (elt (_Sum . bv) 0) 0) s)
              (write-long (ash (elt (_Sum . bv) 1) -1) s))
             ((and (class _Sum) (= (length (_Sum . bv)) 1)) ;; big1
              (write-long (elt (_Sum . bv) 0) s)
              (write-long (if (>= _Sum 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _Sum s)(write-long (if (>= _Sum 0) 0 #xffffffff) s)))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int64 _Sum
#+(or :alpha :irix6 :x86_64)
      (setf _Sum (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _Sum (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;;
   self)
  )

(defclass iiwa_msgs::AddTwoInts
  :super ros::object
  :slots ())

(setf (get iiwa_msgs::AddTwoInts :md5sum-) "713e5cf1444846805670f946f08bfc96")
(setf (get iiwa_msgs::AddTwoInts :datatype-) "iiwa_msgs/AddTwoInts")
(setf (get iiwa_msgs::AddTwoInts :request) iiwa_msgs::AddTwoIntsRequest)
(setf (get iiwa_msgs::AddTwoInts :response) iiwa_msgs::AddTwoIntsResponse)

(defmethod iiwa_msgs::AddTwoIntsRequest
  (:response () (instance iiwa_msgs::AddTwoIntsResponse :init)))

(setf (get iiwa_msgs::AddTwoIntsRequest :md5sum-) "713e5cf1444846805670f946f08bfc96")
(setf (get iiwa_msgs::AddTwoIntsRequest :datatype-) "iiwa_msgs/AddTwoIntsRequest")
(setf (get iiwa_msgs::AddTwoIntsRequest :definition-)
      "int64 A
int64 B
---
int64 Sum

")

(setf (get iiwa_msgs::AddTwoIntsResponse :md5sum-) "713e5cf1444846805670f946f08bfc96")
(setf (get iiwa_msgs::AddTwoIntsResponse :datatype-) "iiwa_msgs/AddTwoIntsResponse")
(setf (get iiwa_msgs::AddTwoIntsResponse :definition-)
      "int64 A
int64 B
---
int64 Sum

")



(provide :iiwa_msgs/AddTwoInts "713e5cf1444846805670f946f08bfc96")


